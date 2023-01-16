#!/usr/bin/python3

##############################################################################
# Idea from: Internet
# Author: Carlos Lacaci Moya

# Name: mount_usb.py
# Description: Utility to mount and umount USB devices
# Date: mié 26 oct 2022 09:37:20 CEST
# Dependencies:
# Version: 1.1
##############################################################################

import subprocess
import re
from pathlib import Path
from collections import namedtuple
from dataclasses import dataclass, field
from typing import Any, Iterator
from rich.console import Console
from database import CreateDatabase
from helpers import BeautiPanel

# From rich module
console = Console()


class RunCommand:
    """Execute command as a subprocess"""

    @staticmethod
    def run(command: Any) -> Any:
        """Run the command"""
        return subprocess.run(command,
                              capture_output=True,
                              text=True,
                              shell=True)


@dataclass
class CheckUsb:
    """Class to deal with USB operations"""

    process: Any = field(default=RunCommand(), init=False)
    connected: Any = field(default=namedtuple('connected', 'status, name'))
    mount_directory: str = field(default="/media")
    database: Any = field(default=CreateDatabase())
    devices: list = field(default_factory=list)

    def __post_init__(self) -> None:
        """ Get devices names from the usbs.dbm"""

        # FOR DEBUGGING
        # print("Calling from CheckUsb")

        self.devices: list = self.database.show_items()

    def _check_mount_directory(self, usb_name: str) -> Path:
        """Check if mount_directory exists, if not create it"""

        mnt_directory: Path = Path().joinpath(self.mount_directory, usb_name)

        # Creating the mnt_directory
        if not mnt_directory.is_dir():
            make_dir: str = f"sudo mkdir -p {mnt_directory}"
            self.process.run(make_dir)

        change_permissions: str = f"sudo chmod -R 777 {mnt_directory}"
        self.process.run(change_permissions)

        change_group: str = f"sudo chgrp -R users {mnt_directory}"
        self.process.run(change_group)

        return mnt_directory

    def _get_usbs_name(self) -> Iterator[str]:
        """Read and return the favorite USBs from 'usbs.dbm'"""

        yield from self.devices

    def _plugged_usbs(self) -> list:
        """Check if the favorite USBs are plugged in"""

        usbs_connected: list[str] = []
        favorite_usbs_list: list[str] = list(self._get_usbs_name())

        for usb_name in favorite_usbs_list:
            get_device_name: str = f"sudo blkid | grep {usb_name}"
            cmd: Any = self.process.run(get_device_name)
            # FOR DEBUGGING
            # print(cmd)
            get_cmd_output: int = cmd.returncode

            if get_cmd_output == 0:
                output_code: bool = True
                console.print(f"[green][+] USB [{usb_name}] connected[/]")

                # Store output and device nane in namedtuple
                usbs_status: Any = self.connected(output_code, usb_name)
                usbs_connected.append(usbs_status)

        return usbs_connected

    def _find_usb_uuid(self, usb: str) -> str:
        """Return the UUID of the USBs found"""

        get_device_uuid: str = f"sudo blkid | grep {usb}"
        cmd: Any = self.process.run(get_device_uuid)

        # FOR DEBUGGING
        # print(cmd)
        get_cmd_output: int = cmd.returncode
        # FOR DEBUGGING
        # print(get_cmd_output)

        if get_cmd_output == 0:
            regex: Any = re.compile(r"\sUUID=(\S+)", re.M)
            if match := regex.search(str(cmd)):
                # FOR DEBUGGING
                console.print(
                    f"[green][+] Found: USB [{usb}] with id: {match.group(1)}[/]"
                )
                usb_uuid: Any = match.group(1).strip('"')

            else:
                console.print(f"[red][!] USB [{usb}] not connected[/]")

        return usb_uuid


@dataclass
class MountUsb:
    """Class for mounting USB drives"""

    usb_checker: Any = field(default=CheckUsb())
    process: Any = field(default=RunCommand(), init=False)
    mounted_usb: list = field(default_factory=list)

    def mount_usb(self, usb_uuid: str, usb_name: str) -> None:
        """Mount the device with the given _id"""

        mnt_directory: Path = self.usb_checker._check_mount_directory(usb_name)

        mount: str = f"sudo mount --uuid {usb_uuid} {mnt_directory} -o umask=000"
        cmd: Any = self.process.run(mount)
        # FOR DEBUGGING
        # print(cmd)
        returncode: int = cmd.returncode
        # print(returncode)

        if returncode == 0:
            console.print(
                f"[green][+] USB [{usb_name}] mounted on: {mnt_directory}[/]")
        elif returncode in {32, 1}:
            # elif returncode == 32 or returncode == 1:
            console.print(f"[red][!] USB [{usb_name}] was already mounted[/]")
        else:
            console.print("[red]! Unknown returncode[/]")

            # FOR DEBUGGING
            # console.print(cmd)

    def mounted_usbs(self, show_output: bool = True) -> list:
        """List already mounted USBs"""

        # mounted_usb: list = []
        usb_mount_point: Any = namedtuple('usb_mount_point',
                                          'name, mount_directory')
        favorite_usb_list: Iterator[str] = self.usb_checker._get_usbs_name()

        for usb in favorite_usb_list:
            get_mounted_usb: str = f"lsblk | grep {usb}"
            cmd: Any = self.process.run(get_mounted_usb)
            get_cmd_output: int = cmd.returncode

            if get_cmd_output == 0:
                mnt_directory: Path = Path().joinpath(
                    self.usb_checker.mount_directory, usb)
                usb_mounted_on: Any = usb_mount_point(usb, mnt_directory)
                self.mounted_usb.append(usb_mounted_on)

                if show_output:
                    BeautiPanel.draw_panel(
                        "green", f"USB [{usb}] mounted on: {mnt_directory}")

        if not self.mounted_usb and show_output:
            BeautiPanel.draw_panel("yellow",
                                   "No favorite USB devices mounted!")

        return self.mounted_usb

    def umount_usb(self) -> None:
        """Check if the USB is mounted on mount_point"""

        usbs_mounted: list = self.mounted_usbs()
        for usb in usbs_mounted:
            umount: str = input(
                f"Do you want to unmount {usb.name}? [Yes/No]: ")
            if umount.lower() in {'y', 'yes'}:
                umount_cmd: str = f"cd;sudo umount {usb.mount_directory}"
                self.process.run(umount_cmd)
                console.print(f"[yellow][+] USB [{usb.name}] unmounted[/]")

                # Remove the mount point
                remove_mount_point: str = f"sudo rm -rf {usb.mount_directory}"
                self.process.run(remove_mount_point)


# Functions to handle the classes operations called from "pyusb_lnx.py"
def mount_all() -> None:
    """Main function to mount all the USBs"""

    usb_checker = CheckUsb()
    usb_mounter = MountUsb()

    if usbs_connected := usb_checker._plugged_usbs():
        for usb in usbs_connected:
            usb_uuid: Any = usb_checker._find_usb_uuid(usb.name)
            if usb_uuid != 0:
                usb_mounter.mount_usb(usb_uuid, usb.name)
    else:
        console.print("[red][!] No favorite USB devices found![/]")
        console.print("[red][!] Plug it in or check 'database_menu.py'[/]")


def umount_all() -> None:
    """Main function to unmount all the USBs"""

    usb_mounter = MountUsb()
    usb_mounter.umount_usb()


def mounted_usbs() -> None:
    """Main function to list all the mounted USBs """

    usb_mounter = MountUsb()
    usb_mounter.mounted_usbs()
