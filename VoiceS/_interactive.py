from .text import Slice, Lyrics
from pathlib import Path
import threading

from noneprompt import ListPrompt, Choice, ConfirmPrompt
from click import secho

from .config import config


def play_audio(audio: Path):
    if not config.pinyin_interactive_play_audio:
        secho("未启用播放音频的功能!", fg="bright_red")
        ConfirmPrompt("回车以返回上级菜单...")
        return main_page(slice, audio)
    import wave
    import pyaudio

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


def main_page(slice: Slice, audio: Path):
    secho(f"===== 切片 <{audio.absolute()}> 中包含多音字 =====", fg="bright_red")
    secho(f"原文: {' '.join([ly.han for ly in slice.lyrics_ls])}")
    edit = "❌" if any([ly._warning for ly in slice.lyrics_ls]) else "⭕"
    choices = [
        Choice("[🎵]播放音频"),
    ]
    for ly in slice.lyrics_ls:
        if ly._warning:
            choices.append(
                Choice(
                    f"{ly.index}-修改: {ly.han}({ly.pinyin[ly._choice]}) => {' '.join(ly.pinyin)}"
                )
            )
    choices.append(Choice(f"[{edit}]完成编辑"))
    choice = ListPrompt(
        "请选择您要进行的操作:", choices=choices, annotation="使用键盘的 ↑ 和 ↓ 来选择, 按回车确认"
    ).prompt()
    if choices[-1] == choice:
        return
    elif choices[0] == choice:
        threading.Thread(target=play_audio,args=(audio,)).start()
        return main_page(slice, audio)
    else:
        ly: Lyrics = slice.lyrics_ls[int(choice.name.split("-", maxsplit=1)[0])]
        pin = ListPrompt(
            "您要将 {} 的拼音修改为?",
            choices=[Choice(pin) for pin in ly.pinyin],
            annotation="使用键盘的 ↑ 和 ↓ 来选择, 按回车确认",
        ).prompt()
        ly.change_by_pinyin(pin.name)
        return main_page(slice, audio)
