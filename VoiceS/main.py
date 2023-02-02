from pathlib import Path

from soundfile import _formats

from .audio import *
from .text import load_text


def main(src: Path = Path("data"), des: Path = Path("data/output")):
    des.mkdir(0o755, parents=True, exist_ok=True)
    with open(des.joinpath("excp_file.txt"), "w", encoding="utf-8") as f:
        filels = set(src.rglob("*.ass"))
        for i,ass_file in enumerate(filels):
            print(f"[{i}/{len(filels)}] 正在处理 {ass_file}")
            ass = load_text(ass_file.read_text(encoding="utf-8"), "ass")
            if not ass:
                continue
            for audio_file in ass_file.parent.rglob(f"{ass_file.stem}.*"):
                if audio_file.suffix.upper()[1:] not in _formats.keys():
                    continue
                f.write("\n".join(lab(audio_file, ass, des)))
                f.write("\n\n")
                break
