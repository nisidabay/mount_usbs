#!/usr/bin/python3

##############################################################################
# Idea from: watchdog module
# Author: Carlos Lacaci Moya

# Description: Monitorize changes in several folders whether local or mounted
#              usb devices

# Date: lun 17 oct 2022 22:35:03 CEST
# Dependencies: See requirements.txt
##############################################################################
from watchdog.events import FileSystemEventHandler
from pathlib import Path
from helpers import Notification, RunCommand

popup: Notification = Notification()


class Handler(FileSystemEventHandler):
    """ Manage modifications in the folder specified """

    def __init__(self, folder_to_track, folder_to_copy) -> None:

        # user home() directory
        self.path: Path = Path.home()

        # folder to watch
        self.origin: Path = self.path.joinpath(folder_to_track)

        # folder to copy to
        self.destination: Path = self.path.joinpath(folder_to_copy)

        # synchronized folders
        self._refresh_dest_folder()

        popup.send_message(
            "WATCHDOG ON", f"Start monitoring the files on: {folder_to_track}")

    def on_modified(self, event) -> None:
        """ Update the folder to watch on modified events """

        self._refresh_dest_folder()

        # UNCOMMENT IF YOU WANT POPUP MESSAGES
        # popup.send_message(f"{self.origin.name}", "Modified")

    def on_moved(self, event) -> None:
        """ Update the folder to watch  on move events """

        self._refresh_dest_folder()

        # UNCOMMENT IF YOU WANT POPUP MESSAGES
        # popup.send_message(f"{self.origin.name}", "Moved")

    def on_deleted(self, event) -> None:
        """ Update the folder to watch on delete events """

        self._refresh_dest_folder()

        # UNCOMMENT IF YOU WANT POPUP MESSAGES
        # popup.send_message(f"{self.origin.name}", "Deleted")

    def _refresh_dest_folder(self) -> None:
        """ Update the destination folder """

        cmd: str = f"rsync -rt {self.origin}/ {self.destination}/ --delete"
        RunCommand.run(cmd)
