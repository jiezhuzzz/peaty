import re
from typing import Annotated

from pydantic import StringConstraints

CmdStr = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True,
        min_length=1,
        pattern=re.compile(r"^(?![a-zA-Z_][a-zA-Z0-9_]*=).*"),
    ),
]
