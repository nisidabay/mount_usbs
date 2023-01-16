#!/usr/bin/python3
##############################################################################
# Author: Carlos Lacaci Moya
# Name: folders_to_watch.py
# Description: Interface to json_management.py
# Date: lun 17 oct 2022 12:50:22 CEST
# Version: 1.0
# Dependencies: mount_usb.py
##############################################################################
"""
Usage:
    json_menu.py (-a | -b | -d | -e | -r | -h | -v)

Options:
    -a          add data to json file
    -b          backup json file
    -d          delete record from json file
    -e          edit data in json file
    -r          restore json file
    -v          show data from json file
    -h          show this help
    --version   program version
"""
from docopt import docopt  # type:ignore
from json_management import ManageJson

MJ = ManageJson()
if __name__ == "__main__":
    args = docopt(__doc__,
                  version="json_meny.py v.1.0 - 2022 @CLM")  # type: ignore

    if args["-a"]:
        print("add data to json file")
        MJ.add_data()

    if args["-b"]:
        print("backup json file")
        MJ.backup_data()

    if args["-d"]:
        print("delete record from json file")
        MJ.delete_data()

    if args["-e"]:
        print("modify json file")
        MJ.edit_json_file()

    if args["-r"]:
        print("restore json file")
        MJ.restore_data()

    if args["-v"]:
        print("show data from json file")
        MJ.view_data()

    if args["-h"]:
        print("show this help")
    else:
        print("Type json_menu.py -h for help")
