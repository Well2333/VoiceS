import threading
import time
from pathlib import Path

from click import secho
from noneprompt import Choice, ListPrompt,CancelledError

import wave

import pyaudio

from ..config import config
from ..text import Lyrics, Slice
from .tracker import get_freq, log_freq


class LyricsChoice(Choice):
    lyrics: Lyrics

    @classmethod
    def create(cls, lyrics: Lyrics):
        lyrics.pinyin, s = get_freq(lyrics.han, lyrics.pinyin)
        lc = cls(
            f"[{s}]{lyrics.index:>2}: {lyrics.han}({lyrics.pinyin[lyrics._choice]}) => {' '.join(lyrics.pinyin)}"
        )
        lc.lyrics = lyrics
        return lc

    def change_pinyin(self):
        pin = ListPrompt(
            f"您要将 {self.lyrics.han} 的拼音修改为?",
            choices=[Choice(pin) for pin in self.lyrics.pinyin],
            annotation="使用键盘的 ↑ 和 ↓ 来选择, 按回车确认",
        ).prompt()
        self.lyrics.change_by_pinyin(pin.name)
        self.log_freq()

    def log_freq(self):
        log_freq(self.lyrics.han, self.lyrics.pinyin[self.lyrics._choice])


def play_audio(audio: Path):
    try:
        with wave.open(str(audio.absolute()), "rb") as wf:
            p = pyaudio.PyAudio()
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )
            while len(data := wf.readframes(1024)):
                stream.write(data)
            stream.close()
            p.terminate()
    except Exception as e:
        raise RuntimeError("此设备无法正常播放音频") from e


def main_page(slice: Slice, audio: Path):
    secho(f"===== 切片 <{audio.absolute()}> 中包含多音字 =====", fg="bright_red")
    secho(f"原文: {' '.join([ly.han for ly in slice.lyrics_ls])}")
    choices = [
        Choice("[🎵]播放音频"),
    ]
    # append choices
    choices.extend(LyricsChoice.create(ly) for ly in slice.lyrics_ls if ly._warning)
    choices.append(Choice("[🎉]完成编辑"))
    try:
        choice = ListPrompt(
            "请选择您要进行的操作:", choices=choices, annotation="使用 ↑ ↓ 选择, 回车确认 ⚪数据不足 🔴重点校对 🟡优先校对 🟢一般校对"
        ).prompt()
    except CancelledError:
        raise KeyboardInterrupt
    # finish
    if choices[-1] == choice:
        if len(choices) == 2:
            return
        for choice in choices[1:-1]:
            choice: LyricsChoice
            choice.log_freq()
    # play audio
    elif choices[0] == choice:
        threading.Thread(target=play_audio, args=(audio,)).start()
        time.sleep(0.5)
        return main_page(slice, audio)
    # change pinyin
    else:
        choice: LyricsChoice
        choice.change_pinyin()
        return main_page(slice, audio)
