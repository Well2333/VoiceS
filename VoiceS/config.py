from pathlib import Path
from noneprompt import ListPrompt, Choice, InputPrompt
from click import secho
import json

from typing import Any


class Config:

    """Slice Setting"""

    slice_min_sec: int = 0
    slice_max_sec: int = 15

    """pinyin setting"""
    pinyin_heteronym_check: bool = True
    pinyin_interactive_check: bool = False

    """tracker setting"""
    tracker_download: str = "https://ali.well404.top/files/tracker.json"
    tracker_path: str = str(Path("tracker.json"))

    def __dir__(self):
        return [
            "slice_min_sec",
            "slice_max_sec",
            "pinyin_heteronym_check",
            "pinyin_interactive_check",
            "tracker_download",
            "tracker_path",
        ]

    def __init__(self) -> None:
        if Path("config.json").exists():
            self.load(Path("config.json"))

        choices = [
            Choice("[🔧]修改配置"),
            Choice("[📃]导入配置"),
            Choice("[📝]导出配置"),
            Choice("[🎉]完成修改"),
        ]

        while True:
            secho(
                "\n".join(
                    [
                        "===== 当前配置项 =====",
                        f"最小切片时长: {self.slice_min_sec}",
                        f"最大切片时长: {self.slice_max_sec}",
                        f"多音字检查: {self.pinyin_heteronym_check}",
                        f"交互式多音字检查: {self.pinyin_heteronym_check}",
                        f"多音字提示词典路径: {self.tracker_path}",
                        f"多音字提示词典下载: {self.tracker_download}",
                    ]
                )
            )
            choice = ListPrompt("请导出/载入/调整配置项, 或直接开始:", choices=choices).prompt()
            if choice == choices[0]:
                self.modify()
            elif choice == choices[1]:
                self.load()
            elif choice == choices[2]:
                Path("config.json").write_text(
                    json.dumps(
                        {str(x): self.__getattribute__(x) for x in self.__dir__()}
                    )
                )
            elif choice == choices[3]:
                break

    def modify(self):
        pass

    def load(self, path: Path = None):
        if not path:
            ans = InputPrompt("请输入配置文件的路径, 或直接输入其内容:").prompt()
            if ans.strip().startswith("{"):
                secho("检测到输入为配置信息, 尝试解析")
            else:
                secho("检测到输入为配置文件路径, 尝试读取")
                ans = Path(ans).read_text(encoding="utf-8")
        else:
            secho("检测到当前路径包含 config.json, 尝试读取")
            ans = path.read_text(encoding="utf-8")
        try:
            cfg: dict[str, Any] = json.loads(ans.strip())
            secho("解析成功, 正在覆盖当前配置", fg="bright_green")
        except Exception as e:
            raise RuntimeError("无法解析配置信息") from e
        for key in cfg:
            self.__setattr__(key, cfg[key])

secho(
    """
 _    __        _             _____
| |  / /____   (_)_____ ___  / ___/
| | / // __ \ / // ___// _ \ \__ \ 
| |/ // /_/ // // /__ /  __/___/ / 
|___/ \____//_/ \___/ \___//____/  
""",
    fg="bright_blue",
)
config: Config = Config()


