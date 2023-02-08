# VoiceS
根据 ASS 文件将多种类的音频文件切片为指定格式的文件，并生成对应的 .lab 文件

## 功能与计划

### 功能

- [x] 导出多音字列表
- [x] 交互式多音字排查
- [ ] 整合mfa？

### 输入文件类型

- [x] ass(aegisub)
- [ ] 其他的类型？

## 使用方法

### 配置运行环境

本脚本所需的基本运行环境与 [教程](https://www.yuque.com/sunsa-i3ayc/sivu7h/uz01rcgfixw3t6lh) 中的 `diff` 环境一致（交互式多音字修复需要额外依赖，详见下文），可直接共用环境。

如果你需要直接配置环境可以参考以下命令:

```shell
conda create -n diff python=3.8
conda activate diff
pip install librosa pypinyin # 必装依赖
pip install pyaudio noneprompt # 选装依赖
```

### 下载时间轴工具

下载 [AgeiSub](https://github.com/Aegisub/Aegisub/releases/tag/v3.2.2) 或其他能够根据音频生成 `.ass` 文件的时间轴工具

### 打轴

导入音频文件并生成对应的时间轴，可参考 <https://www.bilibili.com/video/BV19F411w7m5>

注意：

1. 生成的时间轴中每行将会被视为一个“切片”，切片的长度应在 5-15s 为宜，不得超过 2-20s
2. 歌词中不应出现任何标点符号，可以出现空格，也可提前将多音字替换为拼音

### 生成原始数据

注意：若时间轴中某一切片超过 2-20s 的范围，将会报错并跳过**整个文件**，但不会影响到其他文件的处理。

#### 使用命令行运行（默认）

将 `.ass` 文件和 **同名** 的音频文件放置于同一文件夹或其子文件夹下。cd 到 `main.py` 同目录下后输入 `python ./main.py <src> <des>` 命令，程序将会从 `src` 文件夹读取文件，处理后输出到 `des` 文件夹。

例如，数据文件放置于 `/home/admin/src file`，输出文件放置于 `/home/admin/desfile`，那么对应的命令为:
`python ./main.py "/home/admin/src file" /home/admin/des`

#### 直接运行

将 `.ass` 文件和 **同名** 的音频文件放置于 `data` 文件夹或其子文件夹下。cd 到 `data` 文件夹的**根目录**后运行 `main.py`（需将其中第一行的`True`替换为`False`），程序将会从 `data` 文件夹读取文件，处理后输出输出到 `data/output` 文件夹下

### 修正原始数据

在输出目录下（也就是 `des` 或 `data/output`）会生成 `exception.json` 文件，其中记录了包含多音字的切片。此时可以根据此文件对 `.lab` 文件进行修正。（当然你也可以头铁直接拿去mfa，此时生成的文件格式上是没有错误的）

### 交互式多音字修复

在程序启动时会询问 `是否开启 **交互式** 多音字检查` 如果你按照提示开启了该功能，在程序遇到多音字时会记录并在终端开启一个 CLI 来辅助你动态的更改多音字的发音。此功能需要额外的依赖 `noneprompt`。

如果你使用的设备也带有音频播放功能，可在询问 `是否在 **交互式** 多音字检查中开启音频播放` 时开启该功能。此功能需要额外的依赖 `pyaudio`。

如果你在交互式修复过程中未对 **全部** 多音字进行修复，在 `exception.json` 中也会记录未修复的部分。
