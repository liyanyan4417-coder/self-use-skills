---
name: zotero-web-api
description: Reliable Zotero automation using the official Zotero Web API and a macOS Keychain API key stored as service codex-zotero-web-api-key. Use when the user asks Codex to create, list, delete, or manage Zotero group collections/folders, especially in the yanyan group; move or organize Zotero items; perform repeat Zotero write operations; or asks for convenient Zotero workflows without repeated login. Do not look for a Zotero API key in environment variables first; do not use Zotero local API for writes; do not direct-edit zotero.sqlite except emergency recovery.
---

# Zotero Web API

Use this skill for repeatable Zotero work where writes must be reliable and sync-safe.

## Core Rule

- Use the bundled script `scripts/zotero_tool.py` for Zotero Web API reads/writes.
- Use Zotero Desktop local API only for read-only local inspection when useful.
- Do not create Zotero collections by directly editing `zotero.sqlite` unless the user explicitly asks for emergency recovery and accepts the risk.
- Do not try multiple routes first. Start with the Web API tool.
- Do not check environment variables first. The API key is intentionally stored in macOS Keychain.

## Authentication

The script stores the Zotero API key in macOS Keychain under service:

```text
codex-zotero-web-api-key
```

Check whether the key is configured:

```bash
python3 scripts/zotero_tool.py key-status
```

If Codex is not running from this skill directory, use the installed absolute path:

```bash
python3 /Users/xixi/.codex/skills/zotero-web-api/scripts/zotero_tool.py key-status
```

If no key is configured, ask the user to create a Zotero API key at:

```text
https://www.zotero.org/settings/keys/new
```

The key needs library access, write access, and group access for the target group. Prefer asking the user to copy the key to the clipboard, then run:

```bash
python3 scripts/zotero_tool.py setup-key-from-clipboard
```

Do not ask the user to paste API keys into chat.

## Common Workflows

List groups:

```bash
python3 scripts/zotero_tool.py groups
```

List collections in `yanyan`:

```bash
python3 scripts/zotero_tool.py collections --group yanyan
```

Create a top-level folder in `yanyan`:

```bash
python3 scripts/zotero_tool.py create-collection --group yanyan --name 文件夹名
```

The create command is idempotent for top-level folders. If the same folder already exists, it reports the existing collection instead of creating a duplicate.

Delete a group folder by collection key only when the user explicitly asks to delete it:

```bash
python3 scripts/zotero_tool.py delete-collection --group yanyan --key COLLECTIONKEY --yes
```

Before deleting, prefer confirming the target collection key and name. Deleting a collection removes the folder, not the underlying Zotero items.

## Response Style

Report the group name, collection name, and Zotero collection key. Keep security details brief and never print the full API key.
