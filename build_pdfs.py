#!/usr/bin/env python3
"""Turn docs/week*.md into pdfs/week*.pdf.

The website links to pdfs/weekN.pdf. The real source is docs/weekN.md, which
is plain text and easy to edit. Edit the Markdown, run this script, and the
PDFs the site serves are regenerated.

    python3 build_pdfs.py

Requires only Python 3 and Google Chrome (already on this Mac). No pip install.

A small Markdown subset is supported -- exactly what the week files use:
headings, paragraphs, pipe tables, bullet and numbered lists, fenced code,
horizontal rules, and inline bold / italic / code.
"""

import html
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
PDFS = ROOT / "pdfs"

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

INLINE_CODE = re.compile(r"`([^`]+)`")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*]+)\*(?!\*)")


def inline(text: str) -> str:
    """Escape HTML first, then apply inline markup."""
    out = html.escape(text)
    out = INLINE_CODE.sub(r"<code>\1</code>", out)
    out = BOLD.sub(r"<strong>\1</strong>", out)
    out = ITALIC.sub(r"<em>\1</em>", out)
    return out


def split_row(line: str) -> list:
    return [c.strip() for c in line.strip().strip("|").split("|")]


def convert(md: str) -> str:
    lines = md.split("\n")
    out = []
    i, n = 0, len(lines)

    while i < n:
        stripped = lines[i].strip()

        # fenced code
        if stripped.startswith("```"):
            i += 1
            body = []
            while i < n and not lines[i].strip().startswith("```"):
                body.append(html.escape(lines[i]))
                i += 1
            i += 1
            out.append("<pre>" + "\n".join(body) + "</pre>")
            continue

        if not stripped:
            i += 1
            continue

        if re.fullmatch(r"-{3,}", stripped):
            out.append("<hr>")
            i += 1
            continue

        # pipe table: header row followed by a dashed separator row
        if (stripped.startswith("|") and i + 1 < n
                and re.fullmatch(r"\|[\s:|-]+\|", lines[i + 1].strip())):
            head = split_row(stripped)
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append(split_row(lines[i].strip()))
                i += 1
            t = ["<table><thead><tr>"]
            t += [f"<th>{inline(c)}</th>" for c in head]
            t.append("</tr></thead><tbody>")
            for r in rows:
                t.append("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>")
            t.append("</tbody></table>")
            out.append("".join(t))
            continue

        m = re.match(r"(#{1,4})\s+(.*)", stripped)
        if m:
            lvl = len(m.group(1))
            out.append(f"<h{lvl}>{inline(m.group(2))}</h{lvl}>")
            i += 1
            continue

        # lists -- one or two digits only, so a wrapped line starting
        # "2026. Something" is not mistaken for a numbered item
        if re.match(r"[-*]\s+", stripped) or re.match(r"\d{1,2}\.\s+", stripped):
            ordered = bool(re.match(r"\d{1,2}\.\s+", stripped))
            tag = "ol" if ordered else "ul"
            items = []
            while i < n:
                s = lines[i].strip()
                m2 = re.match(r"(?:[-*]|\d{1,2}\.)\s+(.*)", s)
                if m2:
                    items.append(m2.group(1))
                    i += 1
                elif s and lines[i].startswith(("  ", "\t")) and items:
                    items[-1] += " " + s
                    i += 1
                else:
                    break
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue

        # paragraph
        body = []
        while i < n and lines[i].strip() and not re.match(
                r"(#{1,4}\s|[-*]\s|\d{1,2}\.\s|\||```|-{3,}$)", lines[i].strip()):
            body.append(lines[i].strip())
            i += 1
        if body:
            out.append("<p>" + inline(" ".join(body)) + "</p>")
        else:
            i += 1

    return "\n".join(out)


# Purple theme matching style.css, so the PDFs look like the website.
CSS = """
@page { size: A4; margin: 16mm 15mm 14mm; }
* { box-sizing: border-box; }
body {
  margin: 0;
  font-family: 'Poppins', 'Helvetica Neue', Helvetica, Arial, sans-serif;
  font-size: 10pt;
  line-height: 1.5;
  color: #333;
}
h1 {
  font-size: 19pt;
  color: #4c1d95;
  margin: 0 0 4px;
  padding-bottom: 8px;
  border-bottom: 3px solid #6d28d9;
  line-height: 1.2;
}
h2 {
  font-size: 13pt;
  color: #6a0dad;
  margin: 20px 0 7px;
  padding-bottom: 4px;
  border-bottom: 1px solid #ddc9f7;
  page-break-after: avoid;
}
h3 { font-size: 10.8pt; color: #7c3aed; margin: 13px 0 5px; page-break-after: avoid; }
h4 { font-size: 10pt; color: #5b21b6; margin: 11px 0 4px; }
p  { margin: 0 0 8px; }
ul, ol { margin: 0 0 9px; padding-left: 20px; }
li { margin-bottom: 4px; }
strong { color: #4c1d95; }
code {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 8.8pt;
  background: #f3eaff;
  border: 1px solid #e3d3fb;
  border-radius: 3px;
  padding: 0 3px;
  color: #4c1d95;
}
pre {
  font-family: 'SF Mono', Menlo, Consolas, monospace;
  font-size: 8.5pt;
  line-height: 1.45;
  background: #faf6ff;
  border: 1px solid #e3d3fb;
  border-left: 3px solid #6d28d9;
  border-radius: 6px;
  padding: 10px 12px;
  margin: 0 0 10px;
  white-space: pre-wrap;
  page-break-inside: avoid;
  color: #3b0a63;
}
table {
  width: 100%;
  border-collapse: collapse;
  font-size: 9pt;
  margin: 0 0 11px;
  page-break-inside: avoid;
}
th {
  text-align: left;
  font-size: 8pt;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  color: #fff;
  background: #6d28d9;
  padding: 6px 8px;
}
td {
  padding: 5px 8px;
  border-bottom: 1px solid #e9e2f5;
  vertical-align: top;
}
tbody tr:nth-child(even) { background: #faf6ff; }
hr { border: none; border-top: 1px solid #e3d3fb; margin: 14px 0; }
"""


def find_chrome() -> str:
    for path in CHROME_CANDIDATES:
        if Path(path).exists():
            return path
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    sys.exit("Could not find Chrome. Install Google Chrome, or open the "
             "generated .html files and print to PDF from the browser.")


def main() -> None:
    chrome = find_chrome()
    PDFS.mkdir(exist_ok=True)
    sources = sorted(DOCS.glob("week*.md"))
    if not sources:
        sys.exit(f"No week*.md files found in {DOCS}")

    for md_path in sources:
        md = md_path.read_text(encoding="utf-8")
        title = md.split("\n", 1)[0].lstrip("# ").strip()
        page = (
            "<!doctype html><html lang='en'><head><meta charset='utf-8'>"
            f"<title>{html.escape(title)}</title>"
            "<link rel='preconnect' href='https://fonts.googleapis.com'>"
            "<link href='https://fonts.googleapis.com/css2?family=Poppins:"
            "wght@400;600;700&display=swap' rel='stylesheet'>"
            f"<style>{CSS}</style></head><body>{convert(md)}</body></html>"
        )
        html_path = PDFS / (md_path.stem + ".html")
        pdf_path = PDFS / (md_path.stem + ".pdf")
        html_path.write_text(page, encoding="utf-8")

        subprocess.run(
            [chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
             f"--print-to-pdf={pdf_path}", str(html_path)],
            check=True, capture_output=True,
        )
        html_path.unlink()  # the HTML is only an intermediate step
        size_kb = pdf_path.stat().st_size / 1024
        print(f"  {md_path.name:14s} -> {pdf_path.name:12s} ({size_kb:6.1f} KB)")

    print(f"\nDone. {len(sources)} PDFs written to {PDFS}")


if __name__ == "__main__":
    main()
