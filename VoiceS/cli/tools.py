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
def uta(input: str, output: str, perset: int, offset: int):
    # sourcery skip: raise-from-previous-error
    src = Path(input)
    des = Path(output)

    try:
        from ..functions.tools.uta import UtA

        click.secho(f"正在将 {src.absolute()} 转化为 {des.absolute()}")
        UtA(src.read_text("utf-8"), perset=perset, offset=offset).write(des)
    except CancelledError:
        raise KeyboardInterrupt
