import os
import shlex
import shutil
import subprocess
from pathlib import Path
from subprocess import CompletedProcess
from typing import Self, override

from pydantic import (
    BaseModel,
    ConfigDict,
    DirectoryPath,
    Field,
    field_validator,
    validate_call,
)
from rich.console import Console

from peaty.types.sh import CmdStr

console = Console()


class Command(BaseModel):
    model_config = ConfigDict(frozen=True)
    argv: list[str] = Field(min_length=1)
    env: dict[str, str] = Field(default_factory=dict)

    @override
    def __str__(self) -> str:
        return self.raw

    @classmethod
    def from_raw(cls, raw: CmdStr) -> Self:
        return cls(argv=shlex.split(raw))

    @field_validator("argv")
    @classmethod
    def _has_exec(cls, argv: list[str]) -> list[str]:
        exe = argv[0]
        if shutil.which(exe) is None:
            raise ValueError(f"Executable '{exe}' not found in PATH.")
        return argv

    def with_env(self, env: dict[str, str]) -> Self:
        return self.model_copy(update={"env": {**self.env, **env}})

    @property
    def raw(self) -> str:
        env_parts = [f"{k}={v}" for k, v in self.env.items()]
        return shlex.join([*env_parts, *self.argv])

    @validate_call
    def run(self, workdir: DirectoryPath = Path.cwd()) -> CompletedProcess[str]:
        merged_env = os.environ.copy()
        if self.env:
            merged_env.update(self.env)

        p = subprocess.run(
            self.argv,
            text=True,
            capture_output=True,
            env=merged_env,
            cwd=workdir,
        )
        return p
