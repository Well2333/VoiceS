from pathlib import Path

import click
from noneprompt import CancelledError


@click.command(help="将 openutau 工程文件(.ustx) 转为 Aegisub 文件(.ass)")
@click.option(
    "-i",
    "--input",
    prompt="请输入需要处理的文件的路径",
    help="需要处理的文件",
)
@click.option(
    "-o",
    "--output",
    prompt="请输入处理后输出的文件的路径",
    help="处理后输出的文件",
)
@click.option(
    "-t",
    "--track",
    default=None,
    prompt="请输入需要提取的轨道名",
    prompt_required=False,
    help="需要提取的轨道",
)
@click.option(
    "-l",
    "--lyrics",
    default=None,
    prompt="请输入歌词原文文件",
    prompt_required=False,
    help="歌词原文文件",
)
@click.option(
    "--perset",
    default=0,
    prompt="请输入每行前添加的空白秒数, 单位为毫秒(ms)",
    prompt_required=False,
    help="每行前添加的空白秒数",
)
@click.option(
    "--offset",
    default=0,
    prompt="请输入每行后添加的空白秒数, 单位为毫秒(ms)",
    prompt_required=False,
    help="每行后添加的空白秒数",
)
def uta(input: str, output: str, track: str, lyrics: str, perset: int, offset: int):
    # sourcery skip: raise-from-previous-error
    src = Path(input)
    des = Path(output)
    lys = Path(lyrics).read_text("utf-8") if lyrics else ""

    try:
        from ..functions.tools.uta import UtA

        click.secho(f"正在将 {src.absolute()} 转化为 {des.absolute()}")
        UtA(
            src.read_text("utf-8"),
            track,
            lys,
            perset=perset,
            offset=offset,
        ).write(des)
    except CancelledError:
        raise KeyboardInterrupt
