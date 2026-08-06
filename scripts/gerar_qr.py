"""Gera os QR Codes do protótipo. Uso: python scripts/gerar_qr.py URL_BASE"""
from pathlib import Path
from urllib.parse import urlencode
import sys
import qrcode

base_url = sys.argv[1].rstrip("?") if len(sys.argv) > 1 else "http://localhost:8000/"
output = Path(__file__).resolve().parents[1] / "assets" / "qr"
output.mkdir(parents=True, exist_ok=True)

for chapter in (27, 34, 43, 56, 62, 68, 75, 82, 91, 104, 113, 121, 132, 138, 147, 154, 159, 171, 176, 188, 201, 219, 228, 238, 245, 263, 276, 289, 297, 314):
    separator = "&" if "?" in base_url else "?"
    url = f"{base_url}{separator}{urlencode({'capitulo': chapter})}"
    qr = qrcode.QRCode(version=None, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=16, border=4)
    qr.add_data(url)
    qr.make(fit=True)
    qr.make_image(fill_color="#090a0c", back_color="white").save(output / f"capitulo-{chapter}.png")
    print(f"{chapter}: {url}")
