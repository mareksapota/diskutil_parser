from typing import Union

from .containers import Partition, Disk, Volume

ParseResult = Union[Disk, Partition, Volume]

__all__ = ["ParseResult"]
