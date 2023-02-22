import json
import os
from pathlib import Path
from typing import Any

from click import secho
from noneprompt import CancelledError, Choice, ConfirmPrompt, InputPrompt, ListPrompt

DEFULAT_CONFIG_PATH = (
    Path(os.getcwd()).joinpath("voices_config", "slicer.json").absolute()
)


class Config:

    """Slice Setting"""

    slice_min_sec: float = 0
    slice_max_sec: float = 15

    """pinyin setting"""
    pinyin_heteronym_check: bool = True
    pinyin_interactive_check: bool = False

    """tracker setting"""
    tracker_download: str = "https://ali.well404.top/files/tracker.json"
    tracker_path: str = str(DEFULAT_CONFIG_PATH.parent.joinpath("slicer_tracker.json"))

    """skip setting"""
    skip_exist_slice: bool = True

    def __dir__(self):
        return [
            "slice_min_sec",
            "slice_max_sec",
            "pinyin_heteronym_check",
            "pinyin_interactive_check",
            "tracker_download",
            "tracker_path",
            "skip_exist_slice",
        ]

    def __init__(self) -> None:
        if DEFULAT_CONFIG_PATH.exists():
            self.load(defualt=True)

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
                        f"跳过已存在的切片: {self.skip_exist_slice}",
                    ]
                )
            )
            choice = ListPrompt("请导出/载入/调整配置项, 或直接开始:", choices=choices).prompt()
            if choice == choices[0]:
                self.modify()
            elif choice == choices[1]:
                self.load()
            elif choice == choices[2]:
                self.save()

            elif choice == choices[3]:
                break

    def modify(self):
        while True:
            try:
                min_sec = float(
                    f"""{float(
                    InputPrompt(
                        "请输入 **切片最短时长**, 取值范围为 [0, 5] 秒:", default_text=str(self.slice_min_sec)
                    ).prompt()
                ):.02f}"""
                )
                if 0 <= min_sec <= 5:
                    self.slice_min_sec = min_sec
                    break
            except CancelledError:
                secho("已终止配置流程! 已修改的部分将会保留!", fg="bright_red")
                return
            except Exception as e:
                secho(f"输入值无法解析, 请重新输入: {e}", fg="bright_red")

        while True:
            try:
                max_sec = float(
                    f"""{float(
                    InputPrompt(
                        "请输入 **切片最长时长**, 取值范围为 (5, 20] 秒:", default_text=str(self.slice_max_sec)
                    ).prompt()
                ):.02f}"""
                )
                if 5 < max_sec <= 20:
                    self.slice_max_sec = max_sec
                    break
            except CancelledError:
                secho("已终止配置流程! 已修改的部分将会保留!", fg="bright_red")
                return
            except Exception as e:
                secho(f"输入值无法解析, 请重新输入: {e}", fg="bright_red")

        try:
            self.pinyin_heteronym_check = ConfirmPrompt(
                "是否开启多音字检查?", default_choice=self.pinyin_heteronym_check
            ).prompt()
            if self.pinyin_heteronym_check:
                self.pinyin_interactive_check = ConfirmPrompt(
                    "是否开启 **交互式** 多音字检查?", default_choice=self.pinyin_interactive_check
                ).prompt()
            else:
                self.pinyin_interactive_check = False

            self.tracker_download = InputPrompt(
                "请输入 <tracker.json 在线地址>(若不想在线获取则留空)?",
                default_text=self.tracker_download,
            ).prompt()
            self.tracker_path = InputPrompt(
                "请输入 <tracker.json 保存路径>?", default_text=self.tracker_path
            ).prompt()

            self.skip_exist_slice = ConfirmPrompt(
                "是否跳过已存在的切片?", default_choice=self.skip_exist_slice
            ).prompt()
        except CancelledError:
            secho("已终止配置流程! 已修改的部分将会保留!", fg="bright_red")
            return

    def load(self, defualt: bool = False):
        if defualt:
            secho("检测到当前路径包含 slicer 的配置文件, 尝试读取")
            try:
                ans = DEFULAT_CONFIG_PATH.read_text(encoding="utf-8")
            except Exception as e:
                secho(f"无法正常读取配置文件, 使用默认值: {e}")
                return
        else:
            ans = InputPrompt(
                "请输入配置文件的路径, 或直接输入其内容:", default_text=str(DEFULAT_CONFIG_PATH)
            ).prompt()
            if ans.strip().startswith("{"):
                secho("检测到输入为配置信息, 尝试解析")
            else:
                secho("检测到输入为配置文件路径, 尝试读取")
                try:
                    ans = Path(ans).read_text(encoding="utf-8")
                except Exception as e:
                    secho(f"无法正常读取配置文件: {e}")
                    self.load()

        try:
            cfg: dict[str, Any] = json.loads(ans.strip())
            secho("解析成功, 正在覆盖当前配置", fg="bright_green")
        except CancelledError:
            return
        except Exception as e:
            secho(f"无法解析配置信息, 请重新输入: {e}", fg="bright_red")
            self.load()
        for key in cfg:
            self.__setattr__(key, cfg[key])

    def save(self):
        cfg = json.dumps(
            {str(x): self.__getattribute__(x) for x in self.__dir__()},
            ensure_ascii=False,
        )
        try:
            ans = InputPrompt(
                "请输入要保存的路径, 或输入 str 以直接获取其内容", default_text=str(DEFULAT_CONFIG_PATH)
            ).prompt()
            if ans.lower() == "str":
                print(cfg)
                return
            des = Path(ans)
            des.parent.mkdir(0o755, True, True)
            des.write_text(cfg, encoding="utf-8")
            return
        except CancelledError:
            return
        except Exception as e:
            secho(f"无法正常写入, 请重新输入: {e}", fg="bright_red")
            self.save()


config: Config = Config()
