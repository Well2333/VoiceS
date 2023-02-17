from typing import Union, List
from ..config import config

from pypinyin import pinyin, Style
from pathlib import Path


class Lyrics:
    index: int
    han: str
    pinyin: List[str]
    _choice: int = 0
    _warning: bool = True

    def __init__(self, index: int, han: str, pinyin: List[str]) -> None:
        self.index: int = index
        self.han: str = han
        self.pinyin: List[str] = pinyin
        if len(pinyin) == 1:
            self._warning = False

    def get(self):
        return self.pinyin[self._choice], self._warning

    def change_by_choice(self, choice: int):
        if choice < len(self.pinyin):
            self._choice = choice
            self._warning = False

    def change_by_pinyin(self, pinyin: str):
        try:
            self._choice = self.pinyin.index(pinyin)
            self._warning = False
        except ValueError:
            return


class Slice:
    """Slice 对象包含了时间信息与对应歌词，用于切片及生成输出文件"""

    start: Union[int, float]
    """开始时间"""
    end: Union[int, float]
    """结束时间"""
    dur: Union[int, float]
    """持续时间"""
    lyrics_ls: List[Lyrics]
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
        self.lyrics_ls = []
        i = 0
        is_ascii = False
        for x in lyrics_text:
            if x in [" "]:
                is_ascii = False
            elif x.isascii():
                if not is_ascii:
                    self.lyrics_ls.append(Lyrics(i, x, [x]))
                    i += 1
                    is_ascii = True
                else:
                    ly = self.lyrics_ls.pop()
                    ly.han += x
                    ly.pinyin = [ly.han]
                    self.lyrics_ls.append(ly)
            else:
                is_ascii = False
                self.lyrics_ls.append(
                    Lyrics(
                        i,
                        x,
                        pinyin(
                            x,
                            heteronym=config.pinyin_heteronym_check,
                            style=Style.NORMAL,
                        )[0],
                    )
                )
                i += 1
    

    def get_lyrics(self, audio: Path):
        if config.pinyin_interactive_check and any(lyrics._warning for lyrics in self.lyrics_ls):
            from .._interactive import main_page

            main_page(self, audio)

        lys = []
        excp = []
        for lyrics in self.lyrics_ls:
            pinyin, warning = lyrics.get()
            lys.append(pinyin)
            if warning:
                excp.append(f"{lyrics.han} -> {lyrics.pinyin}")

        return " ".join(lys), excp
