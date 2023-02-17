import click
from pathlib import Path


@click.command(help="运行 VoiceS")
@click.option("-i", "--input", prompt="请输入需要处理的文件夹的路径", help="需要处理的文件夹")
@click.option("-o", "--output", prompt="请输入处理后输出的文件夹的路径", help="处理后输出的文件夹")
@click.option("-f", "--force", is_flag=True, help="强制执行")
@click.help_option("-h", "--help", help="显示帮助信息")
def run(input: str, output: str, force: bool):
    src = Path(input)
    des = Path(output)
    if not src.exists():
        click.secho(f"源路径 {src.absolute()} 不存在！", fg="bright_red")
        return
    elif not src.is_dir():
        click.secho(f"源路径 {src.absolute()} 不是文件夹！", fg="bright_red")
        return
    elif not len(list(src.iterdir())):
        click.secho(f"源路径 {src.absolute()} 是空文件夹！", fg="bright_red")
        return

    des.mkdir(0o755, True, True)
    if len(list(des.iterdir())) and not force:
        click.secho(f"目标路径 {des.absolute()} 不是空文件夹！请添加 --force 或 -f 跳过此检查")
        return

    from .main import main

    main(src, des)
