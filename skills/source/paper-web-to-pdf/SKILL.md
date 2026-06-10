---
name: paper-web-to-pdf
description: Use when the user wants to convert an accessible article, paper webpage, blog post, documentation page, or publisher page into a clean PDF with ads/navigation removed, especially for academic paper previews or web articles. Also use when the user asks to scrape/capture a paper webpage, clean useless webpage information, create a readable PDF, or optionally attach the PDF to Zotero. This skill must respect access controls and must not bypass paywalls, login gates, DRM, or publisher download restrictions.
---

# Paper Web To PDF

Convert accessible paper/article webpages into clean, readable PDFs.

## Rules

- Respect access controls. Do not bypass paywalls, JSTOR/library login gates, DRM, CAPTCHA, or publisher download restrictions.
- If the page only exposes a preview, convert only the accessible preview.
- If the user has logged in and content is normally visible/downloadable, use that authorized view.
- Prefer official PDF downloads when legally accessible. Otherwise, create a cleaned PDF from the accessible webpage.
- For Zotero work, attach only real PDFs or clearly label unavailable PDFs as `no-pdf`.

## Workflow

1. Identify the URL and output goal.
2. Run `scripts/paper_web_to_pdf.py` with the URL.
3. If login is needed, rerun in interactive mode and let the user complete login in the browser.
4. Validate the PDF exists and is non-empty.
5. If requested, attach the generated PDF to Zotero as an attachment.

## Command

Basic:

```bash
python3 ~/.codex/skills/paper-web-to-pdf/scripts/paper_web_to_pdf.py "https://example.com/article"
```

With explicit output:

```bash
python3 ~/.codex/skills/paper-web-to-pdf/scripts/paper_web_to_pdf.py "https://example.com/article" --out ./paper.pdf
```

Interactive/login-aware:

```bash
python3 ~/.codex/skills/paper-web-to-pdf/scripts/paper_web_to_pdf.py "https://example.com/article" --interactive
```

## Output

The script writes:

- A clean Markdown/HTML intermediate in `/private/tmp/paper-web-to-pdf/`
- A final PDF at the requested output path or the current directory

## Dependencies

The script uses:

- Chrome headless for PDF rendering
- `web2md` if installed; otherwise it tries `npx web2md`
- Python stdlib for orchestration

If `web2md` is unavailable, use the installed `web-to-markdown` skill instructions to install it or run with `--raw-print`, which prints the accessible webpage as-is with Chrome.
