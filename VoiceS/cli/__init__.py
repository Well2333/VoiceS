import click

from .slicer import slicer
from voices import __version__



click.secho(
    """
 _    __        _             _____
| |  / /____   (_)_____ ___  / ___/
| | / // __ \ / // ___// _ \ \__ \ 
| |/ // /_/ // // /__ /  __/___/ / 
|___/ \____//_/ \___/ \___//____/  
""",
    fg="bright_blue",
)


@click.group()
@click.version_option(
    __version__,
    "-V",
    "--version",
    prog_name="VoiceS",
)
def main():
    pass
    # 有缘再写
    # click.secho(
    #    """
    # _    __        _             _____
    # | |  / /____   (_)_____ ___  / ___/
    # | | / // __ \ / // ___// _ \ \__ \
    # | |/ // /_/ // // /__ /  __/___/ /
    # |___/ \____//_/ \___/ \___//____/
    # """,
    #    fg="bright_blue",
    # )
    # click.secho("欢迎使用 VoiceS!", fg="green", bold=True)
    # choices = [Choice("[slicer] 将音频文件按照字幕文件进行切片, 并将字幕文件转换成 .lab 文件")]
    # result = choices.index(ListPrompt("今天需要做什么呢?", choices=choices).prompt())

    # if result == 0:
    #    slicer()


main.add_command(slicer)
