import subprocess
from typing import List

from .parsing import parse
from .types import ParseResult


def _diskutil_list() -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["diskutil", "list", "-plist"],
        capture_output=True,
        check=True,
    )


def diskutil_list() -> List[ParseResult]:
    process = _diskutil_list()
    data = process.stdout.decode("utf-8")
    return parse(data)


__all__ = ["diskutil_list"]
