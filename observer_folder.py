#!/usr/bin/python3

##############################################################################
# Idea from: watchdog module
# Author: Carlos Lacaci Moya

# Description: Monitorize changes in several folders whether local or mounted
#              usb devices

# Date: lun 17 oct 2022 22:35:03 CEST
# Dependencies: See requirements.txt
##############################################################################
import time

from watchdog.observers import Observer

from classes.folders import Folders
from classes.handler import Handler
from helpers import BeautiPanel
from mount_usb import MountUsb


def check_media(ftc) -> None:
    """ Check that the folder to backup has the media plugged in """

    IGNORE = "MINIS_SDA"
    plugged_usbs = MountUsb().mounted_usbs(show_output=False)
    device = str(ftc).split("/")

    # Get the list of the usbs already mounted
    mounted_devices = [usb.name for usb in plugged_usbs]

    if device[-1] == IGNORE:
        pass
    elif device[-1] not in mounted_devices:
        BeautiPanel.draw_panel(
            fontcolor="green",
            borderstyle="blue",
            message=f"Backing up data to: {ftc} but the USB is not plugged.")
        BeautiPanel.draw_panel(
            fontcolor="yellow",
            message=
            "Insert the USB first before running the 'observer_folder.py'!")


folders = Folders().return_paths()

observer = Observer()

for ftt, ftc in folders.items():
    print(f"watching folder: {ftt}")
    print(f"\t -> backing up to: {ftc}\n")
    event_handler = Handler(ftt, ftc)
    observer.schedule(event_handler, ftt, recursive=True)

    check_media(ftc)

observer.start()
try:
    while True:
        time.sleep(5)
except KeyboardInterrupt:
    observer.stop()

observer.join()
