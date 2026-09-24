#!/usr/bin/env python3
"""Copia las fotos del archivo a fotos/archivo como JPEG de web (lado máx. 1600 px)."""

from pathlib import Path

from PIL import Image, ImageOps

ROOT = Path(__file__).parent
SRC = ROOT / "fotos"
OUT = SRC / "archivo"
MAX_SIDE = 1600
QUALITY = 76
SKIP_DIRS = {"archivo"}
EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".webp", ".bmp"}


def dest_for(src: Path) -> Path:
    rel = src.relative_to(SRC)
    stem = "__".join(rel.with_suffix("").parts)
    safe = "".join(ch if ch.isalnum() or ch in "._- " else "_" for ch in stem).strip()
    safe = "_".join(safe.split())
    if len(safe) > 120:
        safe = safe[:120]
    return OUT / f"{safe}.jpg"


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    used = {}
    written = 0
    skipped = 0
    for src in SRC.rglob("*"):
        if not src.is_file():
            continue
        if SKIP_DIRS.intersection(src.relative_to(SRC).parts):
            continue
        if src.suffix.lower() not in EXTS:
            skipped += 1
            continue
        dest = dest_for(src)
        n = used.get(dest.name, 0)
        if n:
            dest = dest.with_name(f"{dest.stem}_{n}{dest.suffix}")
        used[dest_for(src).name] = n + 1
        if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
            written += 1
            continue
        try:
            with Image.open(src) as im:
                im = ImageOps.exif_transpose(im)
                im.thumbnail((MAX_SIDE, MAX_SIDE))
                if im.mode not in ("RGB", "L"):
                    im = im.convert("RGB")
                elif im.mode == "L":
                    im = im.convert("RGB")
                im.save(dest, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        except Exception as exc:
            print("omitida:", src.name, exc)
            skipped += 1
            continue
        written += 1
        if written % 50 == 0:
            print("fotos:", written)
    total = sum(p.stat().st_size for p in OUT.glob("*.jpg"))
    print(f"listas: {written}  omitidas: {skipped}  MB: {total / 1024 / 1024:.1f}")


if __name__ == "__main__":
    main()
