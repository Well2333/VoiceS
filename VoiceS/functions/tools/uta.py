from pathlib import Path
from typing import List, Union

import yaml
import sys


def get_time(ms: int):
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    return "%01d:%02d:%02d.%02d" % (h, m, s, ms // 10)


class Note:
    def __init__(
        self,
        position: Union[float, int],
        duration: Union[float, int],
        lyric: str,
        mspt: Union[float, int] = 1,
    ) -> None:
        self.start: Union[float, int] = position * mspt
        self.dur: Union[float, int] = duration * mspt
        self.end: Union[float, int] = self.start + self.dur
        self.lyric: str = " " if lyric in {"AP", "SP"} else lyric

    def __add__(self, other):
        """append current note"""
        return Note(self.start, other.start + other.dur - self.start, self.lyric)


class UtA:
    def __init__(
        self,
        src_proj: str,
        track_name: str = "",
        lyrics: str = "",
        perset: int = 0,
        offset: int = 0,
    ):
        """Generate ASS subtitle files

        Args:
            src_proj (str): [ustx file]
            track_name (str, optional): [ustx track name]. Defaults to None.
            lyrics (str, optional): [lyrics file]. Defaults to "".
            perset (int, optional): [perset of line]. Defaults to 0.
            offset (int, optional): [offset of line]. Defaults to 0.
        """ """"""
        self.src = yaml.load(src_proj, Loader=yaml.FullLoader)
        self.perset = perset
        self.offset = offset
        self.track_name = track_name

        self.perfix = self.get_k_word(int(self.perset // 10), "") if self.perset else ""
        self.suffix = self.get_k_word(int(self.offset // 10), "") if self.offset else ""
        self.mspt = 60000 / (self.src["bpm"] * self.src["resolution"])

        self.out = []
        self.index = -1
        self.get_tracks()
        self.get_lyrics_line(lyrics) if lyrics else self.get_ustx_line()

    @staticmethod
    def get_time(ms: Union[float, int]):
        s, ms = divmod(ms, 1000)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return "%01d:%02d:%02d.%02d" % (h, m, s, ms // 10)

    @staticmethod
    def get_k_word(ktime: Union[int, str], word: str):
        return r"{\k" + str(ktime) + "}" + word

    def get_tracks(self):
        for track in self.src["voice_parts"]:
            if (self.track_name and track["name"] == self.track_name) or (
                not self.track_name
            ):
                break
        else:
            print(f"There is no track named {self.track_name}")
            sys.exit(1)
        notes: List[Note] = []
        for raw_note in track["notes"]:
            note = Note(
                raw_note["position"],
                raw_note["duration"],
                raw_note["lyric"],
                self.mspt,
            )
            if note.lyric in ["+"]:
                note = notes.pop() + note
            notes.append(note)
        self.notes = notes

    def get_ustx_line(self):
        """Generate subtitles directly from ustx files"""
        text = self.perfix
        start = 0
        note = self.notes[0]
        for index, note in enumerate(self.notes):
            # check is empty
            if note.lyric == " " and text == self.perfix:
                continue
            # get start time
            if not start:
                start = note.start - self.perset
            # check is new line
            if (
                index > 0
                and note.start > self.notes[index - 1].end + 1  # prevent float error
            ):
                self.out.append(
                    f"Dialogue: 0,{self.get_time(start)},{self.get_time(self.notes[index-1].end+self.offset)},Default,{self.track_name},0,0,0,,{text+self.suffix}"
                )
                start = note.start - self.perset
                text = self.perfix
                if note.lyric == " ":
                    start = 0
                    continue
            text += self.get_k_word(int(note.dur // 10), note.lyric)
        self.out.append(
            f"Dialogue: 0,{self.get_time(start)},{self.get_time(note.end+self.offset)},Default,{self.track_name},0,0,0,,{text+self.suffix}"
        )

    @staticmethod
    def _lyrics_gener(lyrics: str):
        for w in lyrics:
            if w in [" ", ",", "，", ".", "。", ";", "；"]:
                continue
            yield w

    def get_lyrics_line(self, lyrics: str):
        """Generate subtitles from lyrics files and mark the time using ustx files"""
        lyrics_gen = self._lyrics_gener(lyrics)
        text = self.perfix
        start = 0
        end = 0
        for index, note in enumerate(self.notes):
            # check is empty
            if note.lyric == " ":
                if text == self.perfix:
                    continue
                word = " "
            else:
                word = next(lyrics_gen)
            # get start time
            if not start:
                start = note.start - self.perset
            # fill break time
            if (
                index > 0
                and text != self.perfix
                and note.start > self.notes[index - 1].end + 1  # prevent float error
            ):
                text += self.get_k_word(
                    int((note.start - self.notes[index - 1].end) // 10), ""
                )
            # check is new line
            if word == "\n":
                text = text.rstrip(r"{}\k1234567890 ")
                self.out.append(
                    f"Dialogue: 0,{self.get_time(start)},{self.get_time(end)},Default,{self.track_name},0,0,0,,{text+self.suffix}"
                )
                start = note.start - self.perset
                text = self.perfix
                if note.lyric == " ":
                    start = 0
                    continue
                word = next(lyrics_gen)

            text += self.get_k_word(int(note.dur // 10), word)
            end = note.end + self.offset if word != " " else end
        text = text.rstrip(r"{}\k1234567890 ")
        self.out.append(
            f"Dialogue: 0,{self.get_time(start)},{self.get_time(end)},Default,{self.track_name},0,0,0,,{text+self.suffix}"
        )

    def write(self, des: Path):
        des.parent.mkdir(0o755, parents=True, exist_ok=True)
        des.write_text(
            "\n".join(
                [
                    "[Script Info]",
                    "; Script generated by Aegisub 3.2.2",
                    "; http://www.aegisub.org/",
                    "Title: Default Aegisub file",
                    "ScriptType: v4.00+",
                    "WrapStyle: 0",
                    "ScaledBorderAndShadow: yes",
                    "YCbCr Matrix: None\n",
                    "[Events]",
                    "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
                ]
                + self.out
            ),
            "utf-8",
        )


# just for test
# UtA(
#     Path(r"C:\Users\Well404\Desktop\铃芽之旅.ustx").read_text("utf-8"),
#     lyrics = Path(r"C:\Users\Well404\Desktop\铃芽之旅.txt").read_text("utf-8"),
#     perset=150
# ).write(Path(r"C:\Users\Well404\Desktop\铃芽之旅.ass"))
