import json
import time
from pathlib import Path
from sys import platform
from typing import List

import soundfile as sf
from click import secho
from noneprompt import ConfirmPrompt
from soundfile import _formats

from .config import config
from .text import Slice, load_text


def lab(audio: Path, slices: List[Slice], des: Path):
    excp = {}
    with sf.SoundFile(audio, "r") as f:
        data = f.read()
        for n, slice in enumerate(slices, start=0):
            # write .wav
            s = int(slice.start * f.samplerate)
            e = int(slice.end * f.samplerate)
            if (
                des.joinpath(f"{audio.stem}_{n:02d}.lab").exists()
                and config.skip_exist_slice
            ):
                secho(f"切片 {audio.stem}_{n:02d} 已存在, 跳过此切片", fg="black")
                continue
            sf.write(
                des.joinpath(f"{audio.stem}_{n:02d}.wav"),
                data[s:e],
                samplerate=f.samplerate,
            )
            # layout lyrics expection
            lyrics, excp_ = slice.get_lyrics(des.joinpath(f"{audio.stem}_{n:02d}.wav"))
            if excp_:
                excp[f'{des.absolute().joinpath(f"{audio.stem}_{n:02d}")}.lab'] = excp_
            # write .lab with lyrics
            des.joinpath(f"{audio.stem}_{n:02d}.lab").write_text(
                lyrics, encoding="utf-8"
            )
    return excp


def main(src: Path, des: Path, subtype: str):
    excp = []
    st = time.time()
    des.mkdir(0o755, parents=True, exist_ok=True)
    filels = sorted(set(src.rglob(f"*.{subtype}")), key=lambda f: f.name, reverse=True)
    for i, ass_file in enumerate(filels):
        secho(
            f"[{i:3}/{len(filels):3}]{int(time.time()-st):5}s: 正在处理 {ass_file}",
            fg="bright_green",
        )
        # check Chinese char
        if (
            platform == "win32"
            and any("\u4e00" <= ch <= "\u9fff" for ch in ass_file.stem)
            and ConfirmPrompt(
                f"{ass_file} 的文件名中包含中文, 强行制作数据集可能会出现错误, 是否跳过该文件?",
                default_choice=True,
            ).prompt()
        ):
            continue
        ass = load_text(ass_file.read_text(encoding="utf-8"), subtype)
        if not ass:
            continue
        for audio_file in ass_file.parent.rglob(f"{ass_file.stem}.*"):
            if audio_file.suffix.upper()[1:] not in _formats.keys():
                continue
            if e := lab(audio_file, ass, des):
                excp.append(e)
            break
    des.joinpath("exception.json").write_text(
        json.dumps(excp, ensure_ascii=False), encoding="utf-8"
    )
