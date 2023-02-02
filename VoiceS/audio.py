from tempfile import mkstemp
import librosa
import soundfile as sf
from typing import List
from pathlib import Path

from .text import Slice


def lab(audio: Path, slices: List[Slice], out_path: Path):
    excp = []
    with sf.SoundFile(audio, "r") as f:
        data = f.read()
        for n, slice in enumerate(slices, start=0):
            # write .lab
            out_path.joinpath(f"{audio.stem}_{n:02d}.lab").write_text(
                slice.lyrics, encoding="utf-8"
            )
            # write .wav
            s = int(slice.start * f.samplerate)
            e = int(slice.end * f.samplerate)
            out_path.joinpath(f"{audio.stem}_{n:02d}.wav")
            _, tf = mkstemp(suffix=".wav")
            sf.write(tf, data[s:e], samplerate=f.samplerate)  # 一次转码
            y, sr = librosa.load(tf, sr=16000, mono=True)  # 重采样
            sf.write(out_path.joinpath(f"{audio.stem}_{n:02d}.wav"), y, sr)  # 二次转码
            # layout expection
            excp.append(
                f'  {out_path.joinpath(f"{audio.stem}_{n:02d}")}.lab\n    '
                + "\n    ".join(slice.exception)
                + "\n"
            )
    return excp
