import plistlib
from pathlib import Path
from typing import TextIO, List

from .containers import Disk, Partition, Volume
from .types import ParseResult


def parse(data: TextIO | str) -> List[ParseResult]:
    if isinstance(data, TextIO):
        data = data.read()

    plist = plistlib.loads(data.encode("utf-8"))
    # We're interested in the partitions too
    adap_data = plist["AllDisksAndPartitions"]
    return [deserialize(disk_data) for disk_data in adap_data]


def deserialize(data) -> ParseResult:
    """
    Deserialize `data` into a Disk, Partition or Volume, depending on the data.

    :param data: the plist data
    :return: a Disk, Partition, or Volume
    """
    if "Partitions" in data:
        # This is a disk
        return deserialize_disk(data)
    if "VolumeUUID" in data:
        # This is a volume
        return deserialize_volume(data)
    # Otherwise probably a partition
    return deserialize_part(data)


def deserialize_disk(data) -> Disk:
    size = data["Size"]
    part_scheme = data.get("Content", "")
    device_id = data["DeviceIdentifier"]
    partitions = [deserialize_part(part_data) for part_data in data["Partitions"]]
    volumes = (
        [deserialize_volume(volume_data) for volume_data in data["APFSVolumes"]]
        if "APFSVolumes" in data
        else []
    )
    return Disk(size, part_scheme, device_id, partitions, volumes)


def deserialize_part(data) -> Partition:
    # I think DiskUUID is what we want.
    uuid = data.get("DiskUUID", "")
    name = data.get("VolumeName", "")
    mount_point = Path(data["MountPoint"]) if "MountPoint" in data else None
    size = data["Size"]
    content_type = data["Content"]
    device_id = data["DeviceIdentifier"]
    return Partition(name, content_type, device_id, uuid, size, mount_point)


def deserialize_volume(data) -> Volume:
    uuid = data.get("DiskUUID", "")
    name = data.get("VolumeName", "")
    mount_point = Path(data["MountPoint"]) if "MountPoint" in data else None
    size = data["Size"]
    os_internal = data["OSInternal"]
    device_id = data["DeviceIdentifier"]
    return Volume(name, device_id, uuid, size, mount_point, os_internal)


__all__ = [
    "parse",
    "deserialize",
    "deserialize_disk",
    "deserialize_part",
    "deserialize_volume",
]
