from dataclasses import dataclass, is_dataclass
from typing import Any


@dataclass
class Envelope:
    data: str
    type: str   # text or name of these classes


@dataclass
class Error:
    msg: str

    def __str__(self):
        return f"ERROR: {self.msg}"


@dataclass
class Warning:
    msg: str

    def __str__(self):
        return f"WARNING: {self.msg}"


@dataclass
class Result:
    msg: str
    data: Any
    type: str

    def __str__(self):
        return f"Result: {self.msg}"

    def __post_init__(self):
        if self.data is None and self.type is None:
            return
        if self.data is None or self.type is None:
            raise ValueError("data and type must both be None or both be provided")
