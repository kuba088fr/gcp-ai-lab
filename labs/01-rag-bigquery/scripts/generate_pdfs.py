"""Generate the synthetic test PDFs for lab 01 from test_data/documents.yaml.

Usage (from the repo root):
    python labs/01-rag-bigquery/scripts/generate_pdfs.py [--font PATH] [--font-bold PATH]

Output: labs/01-rag-bigquery/data/*.pdf (gitignored - the YAML is the source of truth).
"""

from __future__ import annotations

import argparse
import io
import random
import re
import textwrap
from pathlib import Path

import yaml
from fpdf import FPDF
from PIL import Image, ImageDraw, ImageFilter, ImageFont

LAB_DIR = Path(__file__).resolve().parents[1]
DOCS_YAML = LAB_DIR / "test_data" / "documents.yaml"
OUT_DIR = LAB_DIR / "data"

# Built-in PDF fonts are Latin-1 only, so Polish characters need an embedded TTF font.
DEFAULT_FONT = Path("C:/Windows/Fonts/arial.ttf")
DEFAULT_FONT_BOLD = Path("C:/Windows/Fonts/arialbd.ttf")

PAGE_LABEL = {"pl": "Strona {page} z {{nb}}", "en": "Page {page} of {{nb}}"}
PESEL_WEIGHTS = (1, 3, 7, 9, 1, 3, 7, 9, 1, 3)


def assert_fake_pesels(raw_yaml: str) -> None:
    """Fail if any 11-digit number in the corpus is a checksum-valid PESEL."""
    for number in re.findall(r"\b\d{11}\b", raw_yaml):
        digits = [int(d) for d in number]
        check = (10 - sum(w * d for w, d in zip(PESEL_WEIGHTS, digits)) % 10) % 10
        if check == digits[10]:
            raise ValueError(f"{number} is a valid PESEL - use an invalid checksum for fake data")


class CompanyPDF(FPDF):
    """A4 document with a company header and page-numbered footer."""

    def __init__(self, company: dict, doc: dict) -> None:
        super().__init__(format="A4")
        self.company = company
        self.doc = doc
        self.set_margins(20, 20, 20)
        self.set_auto_page_break(auto=True, margin=20)

    def header(self) -> None:
        self.set_font("Body", "", 8)
        self.set_text_color(110)
        self.cell(0, 5, self.company["name"], new_x="LMARGIN")
        self.cell(0, 5, self.doc["id"], align="R", new_x="LMARGIN", new_y="NEXT")
        self.line(20, self.get_y() + 1, 190, self.get_y() + 1)
        self.ln(6)
        self.set_text_color(0)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Body", "", 8)
        self.set_text_color(110)
        label = PAGE_LABEL[self.doc["language"]].format(page=self.page_no())
        self.cell(0, 5, label, align="C")


def render_text_pdf(company: dict, doc: dict, fonts: tuple[Path, Path]) -> FPDF:
    pdf = CompanyPDF(company, doc)
    pdf.add_font("Body", "", str(fonts[0]))
    pdf.add_font("Body", "B", str(fonts[1]))
    pdf.set_title(doc["title"])
    pdf.set_author(company["name"])
    pdf.add_page()

    pdf.set_font("Body", "B", 16)
    pdf.multi_cell(0, 8, doc["title"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Body", "", 9)
    pdf.set_text_color(90)
    pdf.multi_cell(0, 5, doc["meta"], new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(0)
    pdf.ln(4)

    for section in doc["sections"]:
        pdf.set_font("Body", "B", 12)
        pdf.multi_cell(0, 7, section["heading"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1)
        for block in section["blocks"]:
            render_block(pdf, block)
        pdf.ln(2)
    return pdf


def render_block(pdf: FPDF, block: dict) -> None:
    pdf.set_font("Body", "", 10.5)
    if "p" in block:
        pdf.multi_cell(0, 5.5, block["p"], new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
    elif "ul" in block or "ol" in block:
        items = block.get("ul") or block.get("ol")
        for i, item in enumerate(items, start=1):
            bullet = f"{i}." if "ol" in block else "•"
            pdf.set_x(pdf.l_margin + 4)
            pdf.cell(6, 5.5, bullet)
            pdf.multi_cell(0, 5.5, item, new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
    elif "table" in block:
        table = block["table"]
        pdf.set_font("Body", "", 9.5)
        with pdf.table(col_widths=table["widths"], line_height=6) as t:
            for row in [table["columns"], *table["rows"]]:
                r = t.row()
                for value in row:
                    r.cell(str(value))
        pdf.ln(3)
    else:
        raise ValueError(f"Unknown block type: {block}")


def render_scan_pdf(company: dict, doc: dict, fonts: tuple[Path, Path], seed: int) -> FPDF:
    """Draw the document onto an image (A4 @ 150 dpi) so the PDF has no text layer."""
    rng = random.Random(seed)
    width, height = 1240, 1754
    img = Image.new("L", (width, height), color=238)
    draw = ImageDraw.Draw(img)
    body = ImageFont.truetype(str(fonts[0]), 28)
    bold = ImageFont.truetype(str(fonts[1]), 34)

    y = 140
    lines: list[tuple[str, ImageFont.FreeTypeFont, int]] = [
        (company["name"], body, 0),
        (doc["meta"], body, 30),
        (doc["title"], bold, 30),
    ]
    for section in doc["sections"]:
        lines.append((section["heading"], bold, 20))
        for block in section["blocks"]:
            for line in textwrap.wrap(block["p"], width=72):
                lines.append((line, body, 0))
            lines.append(("", body, 10))

    for text, font, gap_before in lines:
        y += gap_before
        draw.text((120, y), text, fill=30, font=font)
        y += font.size + 14
    if y > height - 120:
        raise ValueError(f"{doc['id']}: scanned memo does not fit on one page")

    # Imitate a cheap scanner: speckles, slight skew and blur.
    for _ in range(4000):
        draw.point((rng.randrange(width), rng.randrange(height)), fill=rng.randrange(150, 220))
    img = img.rotate(0.7, fillcolor=238, resample=Image.BICUBIC)
    img = img.filter(ImageFilter.GaussianBlur(0.7))

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    pdf = FPDF(format="A4")
    pdf.set_title(doc["title"])
    pdf.add_page()
    pdf.image(buf, x=0, y=0, w=210, h=297)
    return pdf


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--font", type=Path, default=DEFAULT_FONT)
    parser.add_argument("--font-bold", type=Path, default=DEFAULT_FONT_BOLD)
    args = parser.parse_args()
    fonts = (args.font, args.font_bold)

    raw_yaml = DOCS_YAML.read_text(encoding="utf-8")
    assert_fake_pesels(raw_yaml)
    corpus = yaml.safe_load(raw_yaml)

    OUT_DIR.mkdir(exist_ok=True)
    for i, doc in enumerate(corpus["documents"]):
        if doc["render"] == "scan":
            pdf = render_scan_pdf(corpus["company"], doc, fonts, seed=i)
        else:
            pdf = render_text_pdf(corpus["company"], doc, fonts)
        out = OUT_DIR / doc["file"]
        pdf.output(str(out))
        print(f"{out.name:40} {pdf.pages_count} page(s)  {out.stat().st_size / 1024:6.1f} KiB")


if __name__ == "__main__":
    main()
