#!/usr/bin/env python3
"""Small Zotero helper for long-term Codex-assisted workflows.

Stores the Zotero Web API key in macOS Keychain and uses the official Zotero
Web API for writes such as creating group collections.
"""

from __future__ import annotations

import argparse
import getpass
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request
import uuid


API_BASE = "https://api.zotero.org"
KEYCHAIN_SERVICE = "codex-zotero-web-api-key"
KEYCHAIN_ACCOUNT = os.environ.get("USER", "zotero")


class ZoteroError(RuntimeError):
    pass


def run_security(args: list[str], input_text: str | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["security", *args],
        input=input_text,
        text=True,
        capture_output=True,
        check=False,
    )


def save_keychain_key(api_key: str) -> None:
    result = run_security(
        [
            "add-generic-password",
            "-a",
            KEYCHAIN_ACCOUNT,
            "-s",
            KEYCHAIN_SERVICE,
            "-w",
            api_key,
            "-U",
        ]
    )
    if result.returncode != 0:
        raise ZoteroError(result.stderr.strip() or "Failed to save API key to Keychain")


def get_keychain_key() -> str | None:
    result = run_security(
        [
            "find-generic-password",
            "-a",
            KEYCHAIN_ACCOUNT,
            "-s",
            KEYCHAIN_SERVICE,
            "-w",
        ]
    )
    if result.returncode == 0:
        return result.stdout.strip()
    return None


def get_api_key(required: bool = True) -> str | None:
    api_key = get_keychain_key() or os.environ.get("ZOTERO_API_KEY")
    if required and not api_key:
        raise ZoteroError(
            "No Zotero API key found in macOS Keychain service "
            f"{KEYCHAIN_SERVICE!r}. Run `python3 scripts/zotero_tool.py setup-key-from-clipboard` first."
        )
    return api_key


def request_json(
    method: str,
    path: str,
    *,
    api_key: str | None = None,
    payload: object | None = None,
    extra_headers: dict[str, str] | None = None,
) -> tuple[object, dict[str, str], int]:
    url = path if path.startswith("http") else f"{API_BASE}{path}"
    body = None
    headers = {
        "Zotero-API-Version": "3",
        "User-Agent": "codex-zotero-tool/1.0",
    }
    if api_key:
        headers["Zotero-API-Key"] = api_key
    if payload is not None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        headers["Content-Type"] = "application/json"
    if method in {"POST", "PUT", "PATCH", "DELETE"}:
        headers["Zotero-Write-Token"] = uuid.uuid4().hex
    if extra_headers:
        headers.update(extra_headers)

    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            raw = response.read()
            text = raw.decode("utf-8") if raw else ""
            data: object
            if text:
                content_type = response.headers.get("Content-Type", "")
                data = json.loads(text) if "json" in content_type else text
            else:
                data = None
            return data, dict(response.headers.items()), response.status
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise ZoteroError(f"HTTP {exc.code} {exc.reason}: {detail}") from exc
    except urllib.error.URLError as exc:
        raise ZoteroError(f"Network error: {exc.reason}") from exc


def parse_next_link(link_header: str | None) -> str | None:
    if not link_header:
        return None
    for part in link_header.split(","):
        section = part.strip()
        if 'rel="next"' not in section:
            continue
        if section.startswith("<") and ">" in section:
            return section[1 : section.index(">")]
    return None


def request_all(path: str, *, api_key: str) -> list[dict]:
    results: list[dict] = []
    next_path: str | None = path
    while next_path:
        data, headers, _ = request_json("GET", next_path, api_key=api_key)
        if not isinstance(data, list):
            raise ZoteroError(f"Unexpected paginated response for {path}")
        results.extend(data)
        next_path = parse_next_link(headers.get("Link"))
    return results


def current_key_info(api_key: str) -> dict:
    data, _, _ = request_json("GET", "/keys/current", api_key=api_key)
    if not isinstance(data, dict):
        raise ZoteroError("Unexpected response from /keys/current")
    return data


def get_user_id(api_key: str) -> int:
    info = current_key_info(api_key)
    user_id = info.get("userID")
    if not isinstance(user_id, int):
        raise ZoteroError("API key response did not include userID")
    return user_id


def list_groups(api_key: str) -> list[dict]:
    user_id = get_user_id(api_key)
    return request_all(f"/users/{user_id}/groups?limit=100", api_key=api_key)


def find_group(api_key: str, name: str) -> dict:
    matches = [group for group in list_groups(api_key) if group.get("data", {}).get("name") == name]
    if not matches:
        raise ZoteroError(f"No Zotero group named {name!r} was found for this API key")
    if len(matches) > 1:
        ids = ", ".join(str(group.get("id")) for group in matches)
        raise ZoteroError(f"Multiple groups named {name!r} found: {ids}")
    return matches[0]


def list_group_collections(api_key: str, group_id: int) -> list[dict]:
    encoded = "/groups/%s/collections?limit=100" % group_id
    return request_all(encoded, api_key=api_key)


def create_group_collection(
    api_key: str,
    group_name: str,
    collection_name: str,
    *,
    parent_collection: str | bool = False,
) -> dict:
    group = find_group(api_key, group_name)
    group_id = int(group["id"])
    existing = list_group_collections(api_key, group_id)
    for collection in existing:
        data = collection.get("data", {})
        if data.get("name") == collection_name and data.get("parentCollection", False) == parent_collection:
            return {
                "created": False,
                "group": group_name,
                "groupID": group_id,
                "collection": data,
                "message": "Collection already exists",
            }

    payload = [{"name": collection_name, "parentCollection": parent_collection}]
    data, headers, status = request_json(
        "POST",
        f"/groups/{group_id}/collections",
        api_key=api_key,
        payload=payload,
    )
    created_key = None
    if isinstance(data, dict):
        success_keys = data.get("success")
        if isinstance(success_keys, dict) and isinstance(success_keys.get("0"), str):
            created_key = success_keys["0"]
        successful = data.get("successful")
        if created_key is None and isinstance(successful, dict):
            first_success = successful.get("0")
            if isinstance(first_success, dict):
                created_key = first_success.get("key")
    if isinstance(headers.get("Location"), str):
        created_key = headers["Location"].rstrip("/").split("/")[-1]
    return {
        "created": status in (200, 201),
        "group": group_name,
        "groupID": group_id,
        "collectionKey": created_key,
        "response": data,
    }


def get_group_collection(api_key: str, group_id: int, collection_key: str) -> dict:
    data, _, _ = request_json(
        "GET",
        f"/groups/{group_id}/collections/{collection_key}",
        api_key=api_key,
    )
    if not isinstance(data, dict):
        raise ZoteroError(f"No collection found for key {collection_key!r}")
    return data


def delete_group_collection(api_key: str, group_name: str, collection_key: str) -> dict:
    group = find_group(api_key, group_name)
    group_id = int(group["id"])
    collection = get_group_collection(api_key, group_id, collection_key)
    version = collection.get("version")
    if not isinstance(version, int):
        raise ZoteroError(f"Collection {collection_key!r} did not include a version")

    _, _, status = request_json(
        "DELETE",
        f"/groups/{group_id}/collections/{collection_key}",
        api_key=api_key,
        extra_headers={"If-Unmodified-Since-Version": str(version)},
    )
    return {
        "deleted": status in (200, 204),
        "group": group_name,
        "groupID": group_id,
        "collection": collection.get("data", {}),
    }


def print_json(value: object) -> None:
    print(json.dumps(value, ensure_ascii=False, indent=2))


def redact_key_info(info: dict) -> dict:
    cleaned = dict(info)
    if isinstance(cleaned.get("key"), str):
        key = cleaned["key"]
        cleaned["key"] = f"{key[:4]}...{key[-4:]}" if len(key) > 8 else "***"
    return cleaned


def cmd_setup_key(_: argparse.Namespace) -> None:
    print("Paste your Zotero Web API key. Input is hidden and will be saved to macOS Keychain.")
    api_key = getpass.getpass("Zotero API key: ").strip()
    if not api_key:
        raise ZoteroError("API key was empty")
    save_keychain_key(api_key)
    info = current_key_info(api_key)
    print_json({"saved": True, "key": {"userID": info.get("userID"), "username": info.get("username")}})


def cmd_setup_key_from_clipboard(_: argparse.Namespace) -> None:
    result = subprocess.run(["pbpaste"], text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise ZoteroError(result.stderr.strip() or "Failed to read clipboard")
    api_key = result.stdout.strip()
    if not api_key:
        raise ZoteroError("Clipboard is empty. Copy the Zotero API key first.")
    save_keychain_key(api_key)
    info = current_key_info(api_key)
    print_json({"saved": True, "key": {"userID": info.get("userID"), "username": info.get("username")}})


def cmd_key_status(_: argparse.Namespace) -> None:
    api_key = get_api_key(required=False)
    if not api_key:
        print_json({"configured": False})
        return
    info = current_key_info(api_key)
    print_json({"configured": True, "key": redact_key_info(info)})


def cmd_groups(_: argparse.Namespace) -> None:
    api_key = get_api_key()
    groups = list_groups(api_key)
    simplified = [
        {
            "id": group.get("id"),
            "name": group.get("data", {}).get("name"),
            "numItems": group.get("meta", {}).get("numItems"),
        }
        for group in groups
    ]
    print_json(simplified)


def cmd_collections(args: argparse.Namespace) -> None:
    api_key = get_api_key()
    group = find_group(api_key, args.group)
    collections = list_group_collections(api_key, int(group["id"]))
    simplified = [
        {
            "key": collection.get("key"),
            "name": collection.get("data", {}).get("name"),
            "parentCollection": collection.get("data", {}).get("parentCollection"),
            "numItems": collection.get("meta", {}).get("numItems"),
        }
        for collection in collections
    ]
    print_json({"group": args.group, "groupID": group.get("id"), "collections": simplified})


def cmd_create_collection(args: argparse.Namespace) -> None:
    api_key = get_api_key()
    result = create_group_collection(api_key, args.group, args.name)
    print_json(result)


def cmd_delete_collection(args: argparse.Namespace) -> None:
    if not args.yes:
        raise ZoteroError("Deletion requires --yes")
    api_key = get_api_key()
    result = delete_group_collection(api_key, args.group, args.key)
    print_json(result)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Zotero Web API helper using macOS Keychain")
    sub = parser.add_subparsers(dest="command", required=True)

    setup_key = sub.add_parser("setup-key", help="Save a Zotero API key to macOS Keychain")
    setup_key.set_defaults(func=cmd_setup_key)

    setup_clipboard = sub.add_parser(
        "setup-key-from-clipboard",
        help="Save the Zotero API key currently copied to the clipboard",
    )
    setup_clipboard.set_defaults(func=cmd_setup_key_from_clipboard)

    key_status = sub.add_parser("key-status", help="Check the saved Zotero API key")
    key_status.set_defaults(func=cmd_key_status)

    groups = sub.add_parser("groups", help="List Zotero groups available to this key")
    groups.set_defaults(func=cmd_groups)

    collections = sub.add_parser("collections", help="List collections in a Zotero group")
    collections.add_argument("--group", required=True, help="Exact Zotero group name")
    collections.set_defaults(func=cmd_collections)

    create = sub.add_parser("create-collection", help="Create a top-level collection in a Zotero group")
    create.add_argument("--group", required=True, help="Exact Zotero group name")
    create.add_argument("--name", required=True, help="Collection name to create")
    create.set_defaults(func=cmd_create_collection)

    delete = sub.add_parser("delete-collection", help="Delete a Zotero group collection by key")
    delete.add_argument("--group", required=True, help="Exact Zotero group name")
    delete.add_argument("--key", required=True, help="Zotero collection key to delete")
    delete.add_argument("--yes", action="store_true", help="Confirm deletion")
    delete.set_defaults(func=cmd_delete_collection)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
        return 0
    except ZoteroError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
