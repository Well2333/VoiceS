import argparse
import sys
from pathlib import Path

parser = argparse.ArgumentParser(
    description="根据 ASS 文件将多种类的音频文件切片为指定格式的文件，并生成对应的 .lab 文件"
)
parser.add_argument("src", type=Path, help="需要处理的文件夹（data文件夹）")
parser.add_argument("des", type=Path, help="处理后文件的输出的文件夹")
args = parser.parse_args()

src: Path = args.src
des: Path = args.des


if not src.exists():
    print(f"源路径 {src.absolute()} 不存在！")
    input("按任意键退出程序...")
    sys.exit(0)
elif not src.is_dir():
    print(f"源路径 {src.absolute()} 不是文件夹！")
    input("按任意键退出程序...")
    sys.exit(0)
elif not len(list(src.iterdir())):
    print(f"源路径 {src.absolute()} 是空文件夹！")
    input("按任意键退出程序...")
    sys.exit(0)

des.mkdir(0o755,True,True)
if len(list(des.iterdir())):
    print(f"目标路径 {des.absolute()} 不是空文件夹！")
    print("程序仍可继续执行，但其中的文件可能会被覆盖或出现未知的错误。")
    input("若继续执行请回车, 若退出请按 Ctrl+C...")

from .main import main

main(src,des)

