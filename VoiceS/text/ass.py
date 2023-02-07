from .slice import Slice
from typing import List


def _time_to_sec(t: str):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def load(ass: str):
    ls: List[Slice] = []
    for l in ass.split("\n"):
        if not l.startswith("Dialogue: "):
            continue
        i = l[10:].strip().split(",", 9)
        s = Slice(
            start=_time_to_sec(i[1]), end=_time_to_sec(i[2]), lyrics_text=i[-1]
        )
        ls.append(s)
    return ls
