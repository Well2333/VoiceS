from pathlib import Path
from soundfile import _formats

from VoiceS import load_text, lab

def main(data: Path = Path("data")):
    data.joinpath("output").mkdir(0o755, parents=True, exist_ok=True)
    with open("excp_file.txt", "w", encoding="utf-8") as f:
        for ass_file in data.rglob("*.ass"):
            ass = load_text(ass_file.read_text(encoding="utf-8"), "ass")
            if not ass:
                continue
            for audio_file in ass_file.parent.rglob(f"{ass_file.stem}.*"):
                if audio_file.suffix.upper()[1:] not in _formats.keys():
                    continue
                f.write("\n".join(lab(audio_file, ass, data.joinpath("output"))))
                f.write("\n\n")
                break


if __name__ == "__main__":
    main()
