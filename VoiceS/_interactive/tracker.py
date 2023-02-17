import json
from typing import List

from click import secho

from pathlib import Path

from ..config import config


TRACKER_PATH = Path(config.tracker_path)
if not (TRACKER_PATH.exists() and TRACKER_PATH.is_file()):
    if config.tracker_download:
        secho(
            f"{TRACKER_PATH} 不存在或不为文件! 将尝试从 {config.tracker_download} 下载此文件!",
            fg="bright_red",
        )
        import urllib.request

        try:
            urllib.request.urlretrieve(config.tracker_download, TRACKER_PATH)
            TRACKER_PATH.chmod(0o755)
            secho("下载成功!", fg="bright_green")
        except Exception as e:
            secho(f"下载失败! 错误原因: {e}", fg="bright_red")
            secho("自动在此位置创建空白文件!", fg="bright_red")
            TRACKER_PATH.touch(0o755, exist_ok=True)
            TRACKER_PATH.write_text("{}", encoding="utf-8")
    else:
        secho(f"{TRACKER_PATH} 不存在或不为文件! 将自动在此位置创建空白文件!", fg="bright_red")
        TRACKER_PATH.touch(0o755, exist_ok=True)
        TRACKER_PATH.write_text("{}", encoding="utf-8")

# tracker 是可以被导入的外置词典, 权重较低
tracker: dict[str, dict[str, int]] = json.loads(
    TRACKER_PATH.read_text(encoding="utf-8")
)
# tracker_local 是仅内存的内置词典, 权重较高, 更能反映当前用户的选择倾向
tracker_local: dict[str, dict[str, int]] = {}


def get_freq(word: str, pinyin: List[str]):
    w_ = tracker.get(word) or {}
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
