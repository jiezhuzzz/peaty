import sys
from pathlib import Path
from typing import Annotated


class Ext:
    def __init__(self, extension: str):
        self.extension = extension.lower()

    def __repr__(self):
        return f"Ext('{self.extension}')"


def __getattr__(name: str):
    if name.endswith("Path") and len(name) > 4:
        prefix = name[:-4]
        extension = f".{prefix.lower()}"

        GeneratedType = Annotated[Path, Ext(extension)]

        setattr(sys.modules[__name__], name, GeneratedType)

        return GeneratedType

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
