from typing import Union, List
from ..config import config

from pypinyin import pinyin, Style


class Slice:
    """Slice 对象包含了时间信息与对应歌词，用于切片及生成输出文件"""

    start: Union[int, float]
    """开始时间"""
    end: Union[int, float]
    """结束时间"""
    dur: Union[int, float]
    """持续时间"""
    lyrics: str
    """歌词拼音"""
    exception: set[str]

    @classmethod
    def load(cls, start: Union[int, float], end: Union[int, float], lyrics_text: str):
        s = Slice()
        excp = []
        # check slice duration
        dur = end - start
        if dur < config.Slice_warning_min_sec or dur > config.Slice_warning_max_sec:
            raise ValueError(
                f"切片时长 **必须** 在 {config.Slice_warning_min_sec} 至 {config.Slice_warning_max_sec} 秒之间, 而不是为 {dur:.2f} 秒"
            )
        elif (
            dur < config.Slice_recommand_min_sec or dur > config.Slice_recommand_max_sec
        ):
            excp.append(
                f"切片时长过{'长' if dur > config.Slice_recommand_max_sec else '短'}"
            )
        s.start: Union[int, float] = start
        s.end: Union[int, float] = end
        s.dur: Union[int, float] = dur

        # trans text to pinyin
        
        lyrics = []
        for i,char in enumerate(pinyin(
            lyrics_text, heteronym=config.pinyin_heteronym_check, style=Style.NORMAL
        )):
            if char == [" "]:
                continue
            if len(char) > 1:
                excp.append(f"歌词中出现多音字 {lyrics_text[i]} -> {char}")
            lyrics.append(char[0])
        s.lyrics = " ".join(lyrics)
        s.exception = set(excp)

        return s
