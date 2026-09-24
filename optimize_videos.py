#!/usr/bin/env python3
"""Prepara vídeos de menos de 90 MB en videos/web para poder subirlos a GitHub."""

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "videos"
OUT = SRC / "web"
FFMPEG = Path(
    r"C:\Users\Guillermo\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.exe"
)
FFPROBE = FFMPEG.with_name("ffprobe.exe")
LIMIT = 90 * 1024 * 1024

# Los de 516 MB y el de 2 GB duran lo mismo que copias ya más pequeñas.
JOBS = [
    ("GRUPO JUDAS de Miranda de Ebro-Burgos-España.mp4", "grupo-judas.mp4", False),
    ("Grupo Judas y Amador Izquierdo-Miranda de Ebro-Burgos-España.mp4", "judas-amador.mp4", False),
    ("videoplayback.mp4", "actuacion.mp4", False),
    ("videoplayback (2).mp4", "actuacion-2.mp4", False),
    ("Grupo JUDAS de Miranda de Ebro y su Have You Ever Seen The Rain.mp4", "have-you-ever-seen-the-rain.mp4", False),
    ("JUDAS MP41 (1).MP4", "mp41.mp4", False),
    ("JUDAS (2).MP4", "archivo.mp4", True),
    ("JUDAS 50 aniversario (11 enero 2025).mp4", "50-aniversario.mp4", True),
    ("Judas en directo.mp4", "en-directo.mp4", True),
    ("Judas Leon de Oro (25 febrero 2025).mp4", "leon-de-oro.mp4", True),
    ("WhatsApp Video 2026-07-29 at 19.37.15.mp4", "whatsapp-2026-07-29.mp4", True),
]


def duration(path: Path) -> float:
    out = subprocess.check_output(
        [str(FFPROBE), "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(out.strip())


def transcode(src: Path, dest: Path) -> None:
    seconds = max(duration(src), 1)
    target_bits = 82 * 1024 * 1024 * 8
    video_bps = max(280_000, int(target_bits / seconds) - 96_000)
    cmd = [
        str(FFMPEG), "-y", "-i", str(src),
        "-vf", "scale='min(1280,iw)':-2",
        "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p",
        "-b:v", str(video_bps), "-maxrate", str(int(video_bps * 1.2)), "-bufsize", str(video_bps * 2),
        "-c:a", "aac", "-b:a", "96k",
        "-movflags", "+faststart",
        str(dest),
    ]
    subprocess.check_call(cmd)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for source_name, dest_name, force in JOBS:
        src = SRC / source_name
        dest = OUT / dest_name
        if dest.exists() and dest.stat().st_size < LIMIT and dest.stat().st_mtime >= src.stat().st_mtime:
            print("ya lista:", dest_name)
            continue
        if not force and src.stat().st_size < LIMIT:
            shutil.copy2(src, dest)
            print("copiada:", dest_name, f"{dest.stat().st_size / 1024 / 1024:.1f} MB")
            continue
        print("comprimiendo:", source_name)
        transcode(src, dest)
        size = dest.stat().st_size
        print("  ->", dest_name, f"{size / 1024 / 1024:.1f} MB")
        if size >= 100 * 1024 * 1024:
            raise SystemExit(f"{dest_name} sigue por encima de 100 MB")
    total = sum(p.stat().st_size for p in OUT.glob("*.mp4"))
    print(f"vídeos listos: {total / 1024 / 1024:.1f} MB")


if __name__ == "__main__":
    main()
