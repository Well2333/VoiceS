from tempfile import mkstemp
import librosa
import soundfile as sf
from typing import List
from pathlib import Path

from .text import Slice
from .config import config


def lab(audio: Path, slices: List[Slice], des: Path):
    excp = {}
    with sf.SoundFile(audio, "r") as f:
        data = f.read()
        for n, slice in enumerate(slices, start=0):
            # write .wav
            s = int(slice.start * f.samplerate)
            e = int(slice.end * f.samplerate)
            des.joinpath(f"{audio.stem}_{n:02d}.wav")
            _, tf = mkstemp(suffix=".wav")
            sf.write(tf, data[s:e], samplerate=f.samplerate)  # 一次转码
            y, sr = librosa.load(tf, sr=16000, mono=True)  # 重采样
            sf.write(des.joinpath(f"{audio.stem}_{n:02d}.wav"), y, sr)  # 二次转码
            # layout lyrics expection
            lyrics, excp_ = slice.get_lyrics(des.joinpath(f"{audio.stem}_{n:02d}.wav"))
            if excp_:
                excp[f'{des.absolute().joinpath(f"{audio.stem}_{n:02d}")}.lab'] = excp_
            # write .lab with lyrics
            des.joinpath(f"{audio.stem}_{n:02d}.lab").write_text(
                    lyrics, encoding="utf-8"
                )
    return excp
