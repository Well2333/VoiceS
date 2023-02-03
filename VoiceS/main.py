from pathlib import Path
from sys import platform

from soundfile import _formats

import time

from .audio import *
from .text import load_text




def main(src: Path = Path("data"), des: Path = Path("data/output")):
    st = time.time()
    des.mkdir(0o755, parents=True, exist_ok=True)
    with open(des.joinpath("excp_file.txt"), "w", encoding="utf-8") as f:
        filels = set(src.rglob("*.ass"))
        for i,ass_file in enumerate(filels):
            print(f"[{i:3}/{len(filels):3}]{int(time.time()-st):5}s: 正在处理 {ass_file}")
            # check Chinese char
            if platform == "win32" and any('\u4e00' <= ch <= '\u9fff' for ch in ass_file.stem):
                print(f"{ass_file} 的文件名中包含中文，跳过该文件...")
                continue
            ass = load_text(ass_file.read_text(encoding="utf-8"), "ass")
            if not ass:
                continue
            for audio_file in ass_file.parent.rglob(f"{ass_file.stem}.*"):
                if audio_file.suffix.upper()[1:] not in _formats.keys():
                    continue
                f.write("\n".join(lab(audio_file, ass, des)))
                f.write("\n\n")
                break
