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

# tracker 是可以被导入的外置词典, 权重较低
tracker: dict[str, dict[str, int]] = json.loads(
    TRACKER_PATH.read_text(encoding="utf-8")
)
# tracker 是仅内存的内置词典, 权重较高, 更能反映当前用户的选择倾向
tracker_local: dict[str, dict[str, int]] = {}


def get_freq(word: str, pinyin: List[str]):
    w_ = tracker.get(word)
    w = tracker_local.get(word) or w_
    
    total = sum(w_.values())
    # 若总数不大于 5 则白色
    if total < 5:
        
        s = "⚪"
    # 若两词典的最大值不统一则红色
    elif (
        sorted(w_.keys(), key=lambda x: w_[x], reverse=True)[0]
        != sorted(w.keys(), key=lambda x: w[x], reverse=True)[0]
    ):
        s = "🔴"
    
    # 若最大值选项占比大于 97% 则绿色, 反之黄色
    else:
        s = "🟢" if any(x / total > 0.97 for x in w_.values()) else "🟡"

    

    try:
        return sorted(pinyin, key=lambda x: w.get(x, 0), reverse=True), s
    except Exception:
        return pinyin, w


def log_freq(word: str, pinyin: str):
    global tracker
    global tracker_local
    for t in (tracker, tracker_local):
        w = t.get(word)
        # if no record
        if not w:
            t[word] = {pinyin: 1}
        # if no pinyin
        elif not w.get(pinyin):
            w[pinyin] = 1
            t[word] = w
        else:
            w[pinyin] += 1
            t[word] = w
    TRACKER_PATH.write_text(json.dumps(tracker, ensure_ascii=False), encoding="utf-8")
