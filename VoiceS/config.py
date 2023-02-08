from pathlib import Path
import os

class Config:

    """Slice Setting"""

    Slice_min_sec: int = 2
    Slice_max_sec: int = 20

    """pinyin setting"""
    pinyin_heteronym_check: bool = True
    pinyin_interactive_check: bool = False
    pinyin_interactive_play_audio: bool = False
    
    """tracker setting"""
    tracker_path: Path = Path("tracker.json")


config: Config = Config()


print("请选择以下功能是否开启, 开启请输入任意字符后回车, 不开启请直接回车.")
config.pinyin_heteronym_check = bool(input("是否开启多音字检查:"))
config.pinyin_interactive_check = (
    bool(input("是否开启 **交互式** 多音字检查:")) if config.pinyin_heteronym_check else False
)
config.pinyin_interactive_play_audio = (
    bool(input("是否在 **交互式** 多音字检查中开启音频播放:"))
    if config.pinyin_interactive_check
    else False
)

packages = []
if config.pinyin_interactive_check:
    try:
        import noneprompt
    except ImportError:
        packages.append("noneprompt")

if config.pinyin_interactive_play_audio:
    try:
        import pyaudio
    except ImportError:
        packages.append("pyaudio")

# check pip
if packages:
    raise ImportError(f"开启该功能需要安装以下未安装的依赖: {' '.join(packages)} 请您手动安装")
