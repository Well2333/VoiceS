from pathlib import Path
from typing import Tuple,List

import click
from noneprompt import CancelledError

@click.command(help="将音频文件按照字幕文件进行切片, 并将字幕文件转换成 .lab 文件")
@click.option(
    "-i",
    "--input",
    multiple=True,
    prompt="请输入需要处理的文件夹的路径",
    help="需要处理的文件夹",
)
@click.option(
    "-o",
    "--output",
    prompt="请输入处理后输出的文件夹的路径",
    help="处理后输出的文件夹",
)
@click.option(
    "-s",
    "--subtype",
    prompt_required=False,
    type=click.Choice(["ass"], case_sensitive=False),
    prompt="请输入字幕文件类型",
    help="字幕文件类型",
    default="ass",
)
@click.option("-f", "--force", is_flag=True, help="强制执行")
def slicer(input: Tuple[str], output: str, subtype: str, force: bool):
    # sourcery skip: raise-from-previous-error
    srcs:List[Path] = []
    for src in input:
        src = Path(src)
        if not src.exists():
            click.secho(f"源路径 {src.absolute()} 不存在！", fg="bright_red")
            return
        elif not src.is_dir():
            click.secho(f"源路径 {src.absolute()} 不是文件夹！", fg="bright_red")
            return
        elif not len(list(src.iterdir())):
            click.secho(f"源路径 {src.absolute()} 是空文件夹！", fg="bright_red")
            return
        srcs.append(src)

    des = Path(output)
    des.mkdir(0o755, True, True)
    if len(list(des.iterdir())) and not force:
        click.secho(f"目标路径 {des.absolute()} 不是空文件夹！请添加 --force 或 -f 跳过此检查")
        return

    try:
        from ..functions.slicer import main as slicer

        slicer(srcs, des, subtype)
    except CancelledError:
        raise KeyboardInterrupt
