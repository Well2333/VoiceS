USE_COMMAD_LINE: bool = True


if USE_COMMAD_LINE:  # 命令行运行
    from VoiceS.cli import *

else:  # 直接运行
    from VoiceS import main

    if __name__ == "__main__":
        main()

