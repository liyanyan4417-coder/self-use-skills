#!/usr/bin/env python3
"""Convert an accessible paper/article webpage to a cleaned PDF.

This script does not bypass access controls. It uses web2md/Readability when
available to remove navigation and ads, then prints the cleaned article HTML to
PDF with Chrome.
"""

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path


TMP_ROOT = Path("/private/tmp/paper-web-to-pdf")
CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]


def slugify(text):
    text = re.sub(r"https?://", "", text)
    text = re.sub(r"[^A-Za-z0-9._-]+", "-", text).strip("-")
    return (text[:80] or "paper-webpage") + ".pdf"


def find_chrome():
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    found = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chrome")
    if found:
        return found
    raise RuntimeError("Chrome/Chromium not found")


def run(cmd, cwd=None, input_text=None, timeout=180):
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input_text,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def web2md_command():
    direct = shutil.which("web2md")
    if direct:
        return [direct]
    if shutil.which("npx"):
        return ["npx", "-y", "web2md"]
    return None


def convert_to_markdown(url, out_md, interactive=False, wait_ms=2000):
    cmd_base = web2md_command()
    if not cmd_base:
        return False, "web2md/npx not available"

    cmd = cmd_base + [
        url,
        "--out",
        str(out_md),
        "--wait-until",
        "networkidle2",
        "--wait-ms",
        str(wait_ms),
    ]
    if interactive:
        profile = TMP_ROOT / "interactive-profile"
        profile.mkdir(parents=True, exist_ok=True)
        cmd.extend(["--interactive", "--user-data-dir", str(profile)])

    result = run(cmd, timeout=300)
    if result.returncode != 0:
        return False, (result.stderr or result.stdout or "web2md failed").strip()
    if not out_md.exists() or out_md.stat().st_size == 0:
        return False, "web2md produced no Markdown"
    return True, ""


def markdown_to_html(md_path, html_path, source_url):
    md = md_path.read_text(encoding="utf-8", errors="replace")
    title = "Clean Article"
    for line in md.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
            break

    blocks = []
    in_list = False
    for raw in md.splitlines():
        line = raw.rstrip()
        if not line:
            if in_list:
                blocks.append("</ul>")
                in_list = False
            continue
        if line.startswith("# "):
            if in_list:
                blocks.append("</ul>")
                in_list = False
            blocks.append(f"<h1>{html.escape(line[2:].strip())}</h1>")
        elif line.startswith("## "):
            if in_list:
                blocks.append("</ul>")
                in_list = False
            blocks.append(f"<h2>{html.escape(line[3:].strip())}</h2>")
        elif line.startswith("### "):
            if in_list:
                blocks.append("</ul>")
                in_list = False
            blocks.append(f"<h3>{html.escape(line[4:].strip())}</h3>")
        elif line.startswith(("- ", "* ")):
            if not in_list:
                blocks.append("<ul>")
                in_list = True
            blocks.append(f"<li>{html.escape(line[2:].strip())}</li>")
        else:
            if in_list:
                blocks.append("</ul>")
                in_list = False
            escaped = html.escape(line)
            escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
            blocks.append(f"<p>{escaped}</p>")
    if in_list:
        blocks.append("</ul>")

    doc = f"""<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
@page {{ size: A4; margin: 22mm 20mm; }}
body {{
  font-family: -apple-system, BlinkMacSystemFont, "Helvetica Neue", Arial, sans-serif;
  color: #222;
  line-height: 1.55;
  font-size: 11.5pt;
}}
main {{ max-width: 780px; margin: 0 auto; }}
h1 {{ font-size: 24pt; line-height: 1.18; margin: 0 0 14pt; }}
h2 {{ font-size: 16pt; margin: 22pt 0 8pt; }}
h3 {{ font-size: 13pt; margin: 16pt 0 6pt; }}
p {{ margin: 0 0 9pt; }}
ul {{ margin: 0 0 9pt 20pt; padding: 0; }}
li {{ margin-bottom: 4pt; }}
.source {{ color: #666; font-size: 9pt; border-bottom: 1px solid #ddd; padding-bottom: 8pt; margin-bottom: 16pt; }}
a {{ color: #1565c0; text-decoration: none; }}
</style>
</head>
<body>
<main>
<div class="source">Source: {html.escape(source_url)}</div>
{chr(10).join(blocks)}
</main>
</body>
</html>"""
    html_path.write_text(doc, encoding="utf-8")


def print_html_to_pdf(html_path, out_pdf, chrome):
    user_data_dir = TMP_ROOT / "chrome-print-profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    url = html_path.resolve().as_uri()
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        f"--user-data-dir={user_data_dir}",
        f"--print-to-pdf={out_pdf}",
        url,
    ]
    result = run(cmd, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "Chrome print failed")
    if not Path(out_pdf).exists() or Path(out_pdf).stat().st_size < 1024:
        raise RuntimeError("PDF was not created or is too small")


def raw_print_url_to_pdf(url, out_pdf, chrome):
    user_data_dir = TMP_ROOT / "chrome-raw-profile"
    user_data_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        chrome,
        "--headless",
        "--disable-gpu",
        "--no-first-run",
        f"--user-data-dir={user_data_dir}",
        f"--print-to-pdf={out_pdf}",
        url,
    ]
    result = run(cmd, timeout=180)
    if result.returncode != 0:
        raise RuntimeError(result.stderr or result.stdout or "Chrome raw print failed")
    if not Path(out_pdf).exists() or Path(out_pdf).stat().st_size < 1024:
        raise RuntimeError("Raw PDF was not created or is too small")


def main():
    parser = argparse.ArgumentParser(description="Clean an accessible paper webpage and print it to PDF.")
    parser.add_argument("url")
    parser.add_argument("--out", default=None)
    parser.add_argument("--interactive", action="store_true")
    parser.add_argument("--raw-print", action="store_true", help="Print webpage as-is without Readability cleanup")
    parser.add_argument("--wait-ms", type=int, default=2000)
    args = parser.parse_args()

    if not args.url.startswith(("http://", "https://")):
        print("URL must start with http:// or https://", file=sys.stderr)
        return 2

    TMP_ROOT.mkdir(parents=True, exist_ok=True)
    out_pdf = Path(args.out or slugify(args.url)).resolve()
    chrome = find_chrome()

    if args.raw_print:
        raw_print_url_to_pdf(args.url, out_pdf, chrome)
        print(str(out_pdf))
        return 0

    md_path = TMP_ROOT / "article.md"
    html_path = TMP_ROOT / "article.html"
    ok, error = convert_to_markdown(args.url, md_path, interactive=args.interactive, wait_ms=args.wait_ms)
    if not ok:
        print(f"Readability conversion failed: {error}", file=sys.stderr)
        print("Tip: rerun with --interactive for login pages or --raw-print for visible-page PDF.", file=sys.stderr)
        return 1

    markdown_to_html(md_path, html_path, args.url)
    print_html_to_pdf(html_path, out_pdf, chrome)
    print(str(out_pdf))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
