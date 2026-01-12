"""
File: {New?}{Ext}File
"""

import os
import re
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Annotated, Final

from pydantic import AfterValidator, DirectoryPath, FilePath, NewPath

PathLikeStr = os.PathLike | str
_FILE_TYPE_PATTERN: Final[re.Pattern] = re.compile(r"^(New)?(\w+)File$")


def _path_with_ext(ext: str) -> Callable[[Path], Path]:
    target_ext = ext.lower() if ext.startswith(".") else f".{ext.lower()}"

    def _validator(v: Path) -> Path:
        if v.suffix.lower() != target_ext:
            raise ValueError(f"Must be a .{target_ext} file")
        return v

    return _validator


def _dir_contains(name: str) -> Callable[[DirectoryPath], DirectoryPath]:
    def _validator(p: DirectoryPath) -> DirectoryPath:
        if not (p / name).exists():
            raise ValueError(f"Directory {p} does not contain required path: {name}")
        return p

    return _validator


def _bin_file(p: Path) -> Path:
    if not os.access(p, os.X_OK):
        raise ValueError(f"File {p} is not executable")
    return p


def _path_exists(p: Path) -> Path:
    if not p.exists():
        raise ValueError(f"Path {p} does not exist")
    return p


# Generic Paths
ExistingPath = Annotated[Path, AfterValidator(_path_exists)]
NewPath = NewPath

# Dirs
Dir = DirectoryPath
NewDir = NewPath
GitDir = Annotated[DirectoryPath, AfterValidator(_dir_contains(".git"))]

# Files
File = FilePath
NewFile = NewPath
BinFile = Annotated[FilePath, AfterValidator(_bin_file)]
NewBinFile = NewPath


# Dynamically generated file types
def __getattr__(name: str):
    m = _FILE_TYPE_PATTERN.match(name)
    if not m:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    path_type = NewPath if m.group(1) else FilePath
    ext = m.group(2).lower()

    GeneratedType = Annotated[path_type, AfterValidator(_path_with_ext(ext))]

    setattr(sys.modules[__name__], name, GeneratedType)

    return GeneratedType
