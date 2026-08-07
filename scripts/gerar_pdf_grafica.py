from __future__ import annotations

import csv
import random
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject
from reportlab.lib.colors import HexColor, white
from reportlab.lib.pagesizes import landscape
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "output" / "pdf"
TEMP_PDF = OUTPUT_DIR / "Paginas_da_Vida_100_cartoes_temp.pdf"
FINAL_PDF = OUTPUT_DIR / "Paginas_da_Vida_100_cartoes_grafica.pdf"
MANIFEST = OUTPUT_DIR / "Paginas_da_Vida_100_cartoes_conferencia.csv"

CHAPTERS = [27, 34, 43, 56, 62, 68, 75, 82, 91, 104, 113, 121, 132, 138, 147,
            154, 159, 171, 176, 188, 201, 219, 228, 238, 245, 263, 276, 289, 297, 314]
SEED = 270104219

TRIM_W, TRIM_H = 85 * mm, 55 * mm
BLEED = 3 * mm
SLUG = 3 * mm
PAGE_W, PAGE_H = TRIM_W + 2 * (BLEED + SLUG), TRIM_H + 2 * (BLEED + SLUG)
TRIM_X = TRIM_Y = BLEED + SLUG
BLEED_X = BLEED_Y = SLUG

INK = HexColor("#090A0C")
PANEL = HexColor("#17181D")
PAPER = HexColor("#EEE8DC")
MUTED = HexColor("#AAA49A")
GOLD = HexColor("#B99A62")


def build_distribution() -> tuple[list[int], set[int]]:
    rng = random.Random(SEED)
    four_copies = set(rng.sample(CHAPTERS, 10))
    records = [chapter for chapter in CHAPTERS for _ in range(4 if chapter in four_copies else 3)]
    for _ in range(10000):
        rng.shuffle(records)
        if len(set(records[:5])) == 5:
            break
    assert len(records) == 100
    assert len(set(records[:5])) == 5
    return records, four_copies


def tracking(c: canvas.Canvas, text: str, x: float, y: float, font: str, size: float,
             color, spacing: float = 1.0, align: str = "left") -> None:
    widths = [stringWidth(char, font, size) for char in text]
    total = sum(widths) + spacing * max(0, len(text) - 1)
    if align == "right":
        x -= total
    elif align == "center":
        x -= total / 2
    c.setFont(font, size)
    c.setFillColor(color)
    for char, width in zip(text, widths):
        c.drawString(x, y, char)
        x += width + spacing


def crop_marks(c: canvas.Canvas) -> None:
    c.setStrokeColor(HexColor("#111111"))
    c.setLineWidth(0.18)
    gap = 0.7 * mm
    length = 2.1 * mm
    left, right = TRIM_X, TRIM_X + TRIM_W
    bottom, top = TRIM_Y, TRIM_Y + TRIM_H
    for x in (left, right):
        c.line(x, 0, x, length)
        c.line(x, PAGE_H - length, x, PAGE_H)
    for y in (bottom, top):
        c.line(0, y, length, y)
        c.line(PAGE_W - length, y, PAGE_W, y)
    c.setFillColor(HexColor("#333333"))
    c.setFont("Helvetica", 3.8)
    c.drawCentredString(PAGE_W / 2, 1.0 * mm, c._pageNumberLabel)


def draw_card(c: canvas.Canvas, chapter: int, page_number: int) -> None:
    c._pageNumberLabel = f"PÁGINA {page_number:03d}  |  CAPÍTULO {chapter}"
    c.setFillColor(white)
    c.rect(0, 0, PAGE_W, PAGE_H, fill=1, stroke=0)
    c.setFillColor(INK)
    c.rect(BLEED_X, BLEED_Y, TRIM_W + 2 * BLEED, TRIM_H + 2 * BLEED, fill=1, stroke=0)
    c.setFillColor(PANEL)
    c.circle(TRIM_X + TRIM_W * .5, TRIM_Y + TRIM_H * .72, 29 * mm, fill=1, stroke=0)

    c.setStrokeColor(GOLD)
    c.setLineWidth(0.25 * mm)
    c.rect(TRIM_X + 1.2 * mm, TRIM_Y + 1.2 * mm, TRIM_W - 2.4 * mm, TRIM_H - 2.4 * mm,
           fill=0, stroke=1)

    left = TRIM_X + 6 * mm
    right = TRIM_X + TRIM_W - 6 * mm
    top = TRIM_Y + TRIM_H - 6 * mm
    logo = ImageReader(str(ROOT / "assets" / "brand" / "jso-logo-gold.png"))
    c.drawImage(logo, left, top - 3.2 * mm, width=11 * mm, height=3.95 * mm,
                mask="auto", preserveAspectRatio=True, anchor="sw")
    tracking(c, "PÁGINAS DA VIDA", left + 13 * mm, top - 2.2 * mm,
             "Helvetica-Bold", 4.4, GOLD, .55)
    tracking(c, "ATO I", right, top - 2.2 * mm, "Helvetica-Bold", 4.4, GOLD, .7, "right")

    qr_outer = 27 * mm
    qr_inner = 23 * mm
    qr_x = right - qr_outer
    qr_y = TRIM_Y + 14 * mm
    c.setFillColor(white)
    c.rect(qr_x, qr_y, qr_outer, qr_outer, fill=1, stroke=0)
    c.drawImage(ImageReader(str(ROOT / "assets" / "qr" / f"capitulo-{chapter}.png")),
                qr_x + 2 * mm, qr_y + 2 * mm, width=qr_inner, height=qr_inner,
                preserveAspectRatio=True, mask="auto")

    tracking(c, "CAPÍTULO", left, TRIM_Y + 35.5 * mm, "Helvetica-Bold", 5.1, MUTED, .9)
    c.setFillColor(PAPER)
    c.setFont("Times-Roman", 31)
    c.drawString(left, TRIM_Y + 20.2 * mm, str(chapter))

    line_y = TRIM_Y + 8.2 * mm
    c.setStrokeColor(GOLD)
    c.setLineWidth(.2 * mm)
    c.line(left, line_y, left + 13 * mm, line_y)
    c.line(left + 39 * mm, line_y, qr_x - 3 * mm, line_y)
    tracking(c, "NÃO LEIA ATÉ O", left + 26 * mm, line_y + 1.1 * mm,
             "Helvetica-Bold", 4.7, PAPER, .48, "center")
    tracking(c, "MOMENTO INDICADO.", left + 26 * mm, line_y - 1.7 * mm,
             "Helvetica-Bold", 4.7, PAPER, .42, "center")
    crop_marks(c)
    c.showPage()


def apply_page_boxes() -> None:
    reader = PdfReader(str(TEMP_PDF))
    writer = PdfWriter()
    trim = RectangleObject([TRIM_X, TRIM_Y, TRIM_X + TRIM_W, TRIM_Y + TRIM_H])
    bleed = RectangleObject([BLEED_X, BLEED_Y, PAGE_W - BLEED_X, PAGE_H - BLEED_Y])
    for page in reader.pages:
        page.trimbox = trim
        page.bleedbox = bleed
        page.cropbox = RectangleObject([0, 0, PAGE_W, PAGE_H])
        writer.add_page(page)
    writer.add_metadata({
        "/Title": "Paginas da Vida - 100 cartoes para grafica",
        "/Author": "JSO - Juventude Superando Obstaculos",
        "/Subject": "Cartoes com QR Codes - 85 x 55 mm, sangria de 3 mm",
    })
    with FINAL_PDF.open("wb") as stream:
        writer.write(stream)
    TEMP_PDF.unlink()


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    records, four_copies = build_distribution()
    c = canvas.Canvas(str(TEMP_PDF), pagesize=(PAGE_W, PAGE_H), pageCompression=1)
    c.setTitle("Paginas da Vida - 100 cartoes para grafica")
    for page_number, chapter in enumerate(records, 1):
        draw_card(c, chapter, page_number)
    c.save()
    apply_page_boxes()

    with MANIFEST.open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream, delimiter=";")
        writer.writerow(["pagina_pdf", "capitulo", "quantidade_total_capitulo", "url"])
        for page_number, chapter in enumerate(records, 1):
            writer.writerow([page_number, chapter, 4 if chapter in four_copies else 3,
                             f"https://jso-paginasdavida.pages.dev/?capitulo={chapter}"])
    print(FINAL_PDF)
    print(MANIFEST)


if __name__ == "__main__":
    main()
