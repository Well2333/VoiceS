# openutau 转 .ass(k轴) 工具(uta)

使用 `voices uta -i <src> -o <des>` 指令来启动脚本，或在脚本中自行输入 `<src>` 或 `<des>`，随后根据脚本的提示修改配置项后即可开始切片。

- `--input(-i)`: 输入路径 `<src>`，也就是需要处理的文件。
- `--output(-o)`: 输出路径 `<des>`，也就是处理后输出的文件。

同时，你也可以添加此两项参数：

- `--perset`: 每行字幕的“前摇”，设置后将会在每行字幕前额外添加一个空值，单位为毫秒(ms)。
- `--offset`: 每行字幕的“后摇”，设置后将会在每行字幕后额外添加一个空值，单位为毫秒(ms)。

注意，脚本分行的依据是 openutau 项目文件中的断字进行区分，并将句中的 `AP` `SP` 替换为空格，忽略句首的 `AP` `SP`，将 `+` 的时长拼接至上一字。
