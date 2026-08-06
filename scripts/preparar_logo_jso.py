from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / ".tools"))
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path(r"C:\Users\Lucas\.codex\generated_images\019fd34f-1be2-7190-bfe2-ed72b7b46dae\exec-de3ab95d-eb72-44cf-af35-4e112815df48.png")
OUTPUT = ROOT / "assets" / "brand"


def main():
    source = Image.open(SOURCE).convert("RGB")
    alpha = Image.new("L", source.size)
    alpha.putdata([
        max(0, min(255, int((min(r, g, b) - 170) * 3)))
        for r, g, b in source.getdata()
    ])

    bbox = alpha.getbbox()
    if not bbox:
        raise RuntimeError("A marca não foi encontrada na imagem de origem.")

    left, top, right, bottom = bbox
    padding = 36
    bbox = (
        max(0, left - padding),
        max(0, top - padding),
        min(source.width, right + padding),
        min(source.height, bottom + padding),
    )
    alpha = alpha.crop(bbox)

    OUTPUT.mkdir(parents=True, exist_ok=True)
    colors = {
        "jso-logo-white.png": (240, 234, 223),
        "jso-logo-gold.png": (185, 154, 98),
        "jso-logo-navy.png": (27, 41, 56),
    }
    for filename, color in colors.items():
        logo = Image.new("RGBA", alpha.size, (*color, 0))
        logo.putalpha(alpha)
        logo.save(OUTPUT / filename, optimize=True)

    favicon = Image.new("RGBA", alpha.size, (240, 234, 223, 0))
    favicon.putalpha(alpha)
    favicon.thumbnail((256, 256), Image.Resampling.LANCZOS)
    favicon.save(OUTPUT / "jso-favicon.png", optimize=True)


if __name__ == "__main__":
    main()
