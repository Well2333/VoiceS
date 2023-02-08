import json
from typing import List

from click import secho

from ..config import config

"""{
    "的":{
        "de":1,
        "di":0
    },"行":{
        "hang":1,
        "xing":0
    }
}"""

TRACKER_PATH = config.tracker_path
if not (TRACKER_PATH.exists() and TRACKER_PATH.is_file()):
    secho(f"{TRACKER_PATH} 不存在或不为文件! 在此位置创建空白文件!", fg="bright_red")
    TRACKER_PATH.touch(0o755, exist_ok=True)
    TRACKER_PATH.write_text("{}", encoding="utf-8")

tracker: dict[str, dict[str, int]] = json.loads(
    TRACKER_PATH.read_text(encoding="utf-8")
)


def get_freq(word: str, pinyin: List[str]):
    w = tracker.get(word)
    try:
        return sorted(pinyin, key=lambda x: w.get(x, 0), reverse=True), w
    except Exception:
        return pinyin, w


def log_freq(word: str, pinyin: str):
    global tracker
    w = tracker.get(word)
    # if no record
    if not w:
        tracker[word] = {pinyin: 1}
    # if no pinyin
    elif not w.get(pinyin):
        w[pinyin] = 1
        tracker[word] = w
    else:
        w[pinyin] += 1
        tracker[word] = w
    TRACKER_PATH.write_text(json.dumps(tracker, ensure_ascii=False), encoding="utf-8")
