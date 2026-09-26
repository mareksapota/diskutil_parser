import subprocess
from typing import List

from .containers import Disk
from .parsing import parse


def _diskutil_list() -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["diskutil", "list", "-plist"],
        capture_output=True,
        check=True,
    )


def diskutil_list() -> List[Disk]:
    process = _diskutil_list()
    data = process.stdout.decode("utf-8")
    return parse(data)


__all__ = ["diskutil_list"]
