from typing import Literal

from click import secho

from . import ass
from .slice import Lyrics, Slice

support_type = Literal["ass"]


def load_text(text: str, text_type: support_type):
    try:
        if text_type == "ass":
            return ass.load(text)
        else:
            raise NotImplementedError
    except Exception as e:
        for _ in range(3):
            secho(e,fg="bright_red")
