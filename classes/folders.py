#!/usr/bin/python3

##############################################################################
# Idea from: watchdog module
# Author: Carlos Lacaci Moya

# Description:  Creates a dictionary with the folders to watch

# Date: mié 26 oct 2022 09:38:11 CEST
# Dependencies: See requirements.txt
##############################################################################
import json
from pathlib import Path
from helpers import abspath, BeautiPanel
from dataclasses import dataclass, field
from mount_usb import MountUsb


@dataclass
class Folders:
    """ Generates a folder dictionary with the folders to watch """

    # The JSON file with the path to the folders to watch
    file_path: str = abspath("folders.json")

    # Stores the folders from the JSON file
    json_file: dict = field(default_factory=dict[str, str])

    # Stores the folders PATH from the JSON file
    folders_dict: dict = field(default_factory=dict[str, str])

    def __post_init__(self) -> None:
        """ Stores the JSON file """
        self.json_file = self._load_json_file()

    def _load_json_file(self) -> dict:
        """ Returns the json file """

        with open(self.file_path, "r") as jf:
            self.json_file: dict = json.load(jf)

        return self.json_file

    def return_paths(self) -> dict[str, str]:
        """ Produce the dictionary with folders to parse by Handler and
        Observer """

        for key in self.json_file["Folders"]:
            ftt: Path = Path.home().joinpath(key['folder_to_track'])
            ftc: Path = Path.home().joinpath(key['folder_to_copy_to'])
            self.folders_dict[ftt] = ftc

        return self.folders_dict
