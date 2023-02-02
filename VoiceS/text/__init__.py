from .slice import Slice
from . import ass

from typing import Literal


support_type = Literal["ass"]


def load_text(text: str, text_type: support_type):
    try:
        if text_type == "ass":
            return ass.load(text)
        else:
            raise NotImplementedError
    except Exception as e:
        print(e)
