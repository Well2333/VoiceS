from typing import Union, List
from ..config import config

from pypinyin import pinyin, Style
from pathlib import Path


class Slice:
    """Slice 对象包含了时间信息与对应歌词，用于切片及生成输出文件"""

    start: Union[int, float]
    """开始时间"""
    end: Union[int, float]
    """结束时间"""
    dur: Union[int, float]
    """持续时间"""
    lyrics_dict: dict[str, List[str]]
    """歌词"""

    def __init__(
        self, start: Union[int, float], end: Union[int, float], lyrics_text: str
    ):
        # check slice duration
        dur = end - start
        if dur < config.Slice_min_sec or dur > config.Slice_max_sec:
            raise ValueError(
                f"切片时长必须在 {config.Slice_min_sec} 至 {config.Slice_max_sec} 秒之间, 而不是为 {dur:.2f} 秒"
            )

        # init param
        self.start = start
        self.end = end
        self.dur = dur
        self.lyrics_dict = {}

        for x in lyrics_text:
            if x in [" "]:
                continue
            elif x.isascii():
                self.lyrics_dict[x] = x
            else:
                self.lyrics_dict[x] = pinyin(
                    x,
                    heteronym=config.pinyin_heteronym_check,
                    style=Style.NORMAL,
                )[0]

    def _interactive(self, audio: Path):
        pass

    def get_lyrics(self, audio: Path):
        if config.pinyin_interactive_check:
            return self._interactive(audio), []
        lys = []
        excp = []
        for han in self.lyrics_dict:
            pin = self.lyrics_dict[han]
            lys.append(pin[0])
            if len(pin) > 1:
                excp.append(f"{han} -> {pin}")

        return " ".join(lys), excp
