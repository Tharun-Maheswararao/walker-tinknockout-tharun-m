"""Render GDD.md to GDD.pdf with headless Chrome: python tools/gdd/build_pdf.py [--html OUT.html]

Needs the `markdown` package (pip install markdown) and Google Chrome (override the path with
CHROME=...). The Markdown file stays the source; this only adds print styling, a cover page and
figure captions (a paragraph that starts with "Figure N." right under an image).
"""
import os, re, subprocess, sys, tempfile
from pathlib import Path
import markdown

ROOT = Path(__file__).resolve().parents[2]
CHROME = os.environ.get("CHROME", "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")

CSS = """
@page { size: Letter; margin: 0.6in 0.65in 0.7in;
  @bottom-center { content: "Tin Knockout  \\00B7  Game Design Document  \\00B7  " counter(page);
                   font: 8pt "Helvetica Neue", Helvetica, Arial, sans-serif; color: #8a8a8a; } }
@page :first { @bottom-center { content: none; } }
* { box-sizing: border-box; }
html { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font: 10pt/1.45 "Helvetica Neue", Helvetica, Arial, sans-serif; color: #1E1A16; background: #fff; margin: 0; }
a { color: #8E2A22; text-decoration: none; }
h1, h2, h3, h4 { break-after: avoid; line-height: 1.2; }
h2 { color: #8E2A22; font-size: 19pt; margin: 26pt 0 8pt; padding-bottom: 4pt; border-bottom: 2.5pt solid #C9962B; }
h3 { color: #1B2438; font-size: 13pt; margin: 16pt 0 6pt; }
h4 { color: #6B4A12; font-size: 11pt; margin: 12pt 0 4pt; }
p, li { orphans: 3; widows: 3; }
hr { border: 0; height: 0; margin: 6pt 0; }
code { font: 8.6pt Menlo, monospace; background: #F3EEE2; padding: 0.5pt 3pt; border-radius: 3pt; }
pre { background: #1B2438; color: #F2E6C4; padding: 9pt 11pt; border-radius: 6pt; break-inside: avoid; }
pre code { background: none; color: inherit; padding: 0; font-size: 8.2pt; }
blockquote { margin: 10pt 0; padding: 8pt 12pt; background: #FAF3E0; border-left: 4pt solid #C9962B; border-radius: 4pt; }
blockquote p { margin: 0; }
table { width: 100%; border-collapse: collapse; margin: 8pt 0 12pt; font-size: 8.6pt; line-height: 1.35; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
th { background: #1B2438; color: #F2E6C4; text-align: left; padding: 5pt 6pt; font-weight: 700; }
td { padding: 4.5pt 6pt; border-bottom: 0.6pt solid #E2DACB; vertical-align: top; }
tbody tr:nth-child(even) td { background: #FBF8F1; }
table.kv td:first-child { width: 22%; font-weight: 700; color: #1B2438; }
figure { margin: 10pt 0 14pt; break-inside: avoid; text-align: center; }
figure img { max-width: 100%; max-height: 8.2in; border-radius: 5pt; }
figure img[src*="prop_room"] { max-width: 62%; }
figure img[src*="contact-sheet"], figure img[src*="screens-grid"] { max-height: 5.4in; }
figure img[src*="style-this"] { max-width: 86%; }
figcaption { font-size: 8.4pt; color: #5a5a5a; font-style: italic; margin-top: 4pt; text-align: left; }
.cover { break-after: page; padding-top: 0.35in; }
.cover h1 { font-size: 50pt; letter-spacing: 1pt; color: #8E2A22; margin: 0 0 4pt; }
.cover h3 { font-size: 14pt; color: #6B4A12; font-weight: 600; margin: 0 0 16pt; }
.cover figure img { border: 2pt solid #C9962B; }
.cover table.kv { font-size: 9.4pt; margin-top: 14pt; }
.cover blockquote { font-size: 9.2pt; }
"""


def build_html() -> str:
    md = (ROOT / "GDD.md").read_text()
    body = markdown.markdown(md, extensions=["tables", "toc", "fenced_code", "sane_lists"])
    # image + "Figure N." paragraph -> <figure> with a caption; a lone image -> <figure>
    body = re.sub(r'<p>(<img [^>]+>)</p>\s*<p><em>(Figure \d+\.[\s\S]*?)</em></p>',
                  r'<figure>\1<figcaption>\2</figcaption></figure>', body)
    body = re.sub(r'<p>(<img [^>]+>)</p>', r'<figure>\1</figure>', body)
    # key/value tables written with an empty header row ("| | |") -> no header, bold first column
    body = re.sub(r'<table>\s*<thead>\s*<tr>\s*(<th></th>\s*)+</tr>\s*</thead>', '<table class="kv">', body)
    # images resolve against the repository root, so the HTML can live anywhere
    body = re.sub(r'src="(?!https?:|file:)([^"]+)"', lambda m: f'src="{(ROOT / m.group(1)).as_uri()}"', body)
    head, sep, rest = body.partition("<h2")
    body = f'<section class="cover">{head}</section>{sep}{rest}'
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<title>Tin Knockout · Game Design Document</title><style>{CSS}</style></head>'
            f'<body>{body}</body></html>')


def main() -> None:
    html = build_html()
    keep = sys.argv[sys.argv.index("--html") + 1] if "--html" in sys.argv else None
    with tempfile.TemporaryDirectory() as tmp:
        page = Path(keep) if keep else Path(tmp) / "GDD.html"
        page.write_text(html)
        out = ROOT / "GDD.pdf"
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={out}", page.resolve().as_uri()],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("wrote", out)


if __name__ == "__main__":
    main()
