from pathlib import Path
from typing import List


class Device:
    def __init__(self, device_id: str, size: int):
        """
        :param device_id: The ID of the device, like disk0 or disk0s1
        :param size: The size of the device
        """
        self.device_id = device_id
        """The device ID, like disk0 or disk0s1"""
        self.size = size
        """The size of the partition, in bytes"""

    @property
    def device_path(self) -> Path:
        """
        The path to the device.
        """
        return Path(f"/dev/{self.device_id}")

    @property
    def raw_device_path(self) -> Path:
        """
        The path to the raw device, which isn't block-buffered.
        """
        return Path(f"/dev/r{self.device_id}")


class Partition(Device):
    def __init__(
        self,
        name: str,
        content_type: str,
        device_id: str,
        uuid: str,
        size: int,
        mount_point: Path,
    ):
        """
        :param name: The name of the partition
        :param content_type: The type of the partition, e.g. Linux swap, Apple_HFS
        :param device_id: The ID of the device, like disk0s1
        :param uuid: The UUID of the partition
        :param size: The size of the partition
        :param mount_point: The mount point, if this partition is mounted
        """
        super().__init__(device_id, size)
        self.name = name
        """The name of the partition"""
        self.uuid = uuid
        """The UUID of the partition"""
        self.content_type = content_type
        """The type of the partition"""
        self.mount_point = mount_point
        """The mount point, if mounted, otherwise None"""

    def is_mounted(self):
        return self.mount_point is not None and self.mount_point.exists()

    def __repr__(self) -> str:
        name_str = f" (named {self.name})" if self.name else ""
        uuid_str = f" (DiskUUID={self.uuid})" if self.uuid else ""
        mount_str = f", mounted at {self.mount_point}" if self.mount_point else ""
        os_internal_str = f" (OS internal: True)" if self.os_internal else ""
        return (
            f"<Partition {self.device_id}{name_str}{uuid_str}{os_internal_str} of type"
            f" {self.content_type}{mount_str}, {self.size} bytes>"
        )


class Volume(Device):
    def __init__(
        self,
        name: str,
        device_id: str,
        uuid: str,
        size: int,
        mount_point: Path,
        os_internal: bool,
    ):
        """
        :param name: The name of the volume
        :param device_id: The ID of the device, like disk0s1
        :param uuid: The UUID of the volume
        :param size: The size of the volume
        :param mount_point: The mount point, if this volume is mounted
        :param os_internal: Is this an OS internal volume, like Recovery
        """
        super().__init__(device_id, size)
        self.name = name
        """The name of the volume"""
        self.uuid = uuid
        """The UUID of the volume"""
        self.mount_point = mount_point
        """The mount point, if mounted, otherwise None"""
        self.os_internal = os_internal
        """True for OS internal volumes"""

    def is_mounted(self):
        return self.mount_point is not None and self.mount_point.exists()

    def __repr__(self) -> str:
        name_str = f" (named {self.name})" if self.name else ""
        uuid_str = f" (DiskUUID={self.uuid})" if self.uuid else ""
        mount_str = f", mounted at {self.mount_point}" if self.mount_point else ""
        os_internal_str = f" (OS internal: True)" if self.os_internal else ""
        return (
            f"<Volume {self.device_id}{name_str}{uuid_str}{os_internal_str}{mount_str},"
            + f" {self.size} bytes>"
        )


class Disk(Device):
    def __init__(
        self,
        size: int,
        partition_scheme: str,
        device_id: str,
        partitions: List[Partition],
        volumes: List[Volume],
        os_internal: bool,
    ):
        """
        :param size: The size of the disk
        :param partition_scheme: The partition scheme for the disk
        :param device_id: The ID of the device, like disk0
        :param partitions: The partition list
        :param volumes: The volumes list
        :param os_internal: Is this an OS internal disk
        """
        super().__init__(device_id, size)
        self.partition_scheme = partition_scheme
        """The partition scheme for the disk. May be None if not detected"""
        self.partitions = partitions
        """The partition list"""
        self.volumes = volumes
        """The volumes list"""
        self.os_internal = os_internal
        """True for OS internal disks"""

    def __repr__(self) -> str:
        part_str = (
            f", {len(self.partitions)} partitions using {self.partition_scheme}"
            if self.partition_scheme
            else ""
        )
        volume_str = f", {len(self.volumes)} volumes" if self.volumes else ""
        return f"<Disk {self.device_id}{part_str}{volume_str}, {self.size} bytes>"


__all__ = ["Device", "Partition", "Disk", "Volume"]
