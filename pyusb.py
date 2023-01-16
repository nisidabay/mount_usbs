#!/usr/bin/python3
##############################################################################
# Author: Carlos Lacaci Moya
# Name: pyusb.py
# Description: Interface to mount_usb.py utility.
# Date: jue 13 oct 2022 23:24:05 CEST
# Version: 1.2
# Dependencies: mount_usb.py
##############################################################################
"""
Usage:
    pyusb.py (-l | -m | -u | -h)

    pyusb.py -l (list connected USBs)
    pyusb.py -m (mount connected USBs)
    pyusb.py -u (umount connected USBs)
    pyusb.py -h (show this help)

Options:
    -l          list connected USBs
    -m          mount connected USBs
    -u          umount connected USBs
    -h          show this help
    --version   program version
"""
from docopt import docopt  # type:ignore
from mount_usb import umount_all, mount_all, mounted_usbs

if __name__ == "__main__":
    args = docopt(__doc__, version="pyusb.py v.1.2 - 2022")  # type: ignore

    if args["-l"]:
        print("list connected USBs")
        mounted_usbs()

    if args["-m"]:
        print("mount connected USBs")
        mount_all()

    if args["-u"]:
        print("umount connected USBs")
        umount_all()

    else:
        print("Type pyusb.py -h for help")
