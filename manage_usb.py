#!/usr/bin/python3
##############################################################################
# Author: Carlos Lacaci Moya
# Description: Interface to database.py that manage USB NAMES

# Date: jue 20 oct 2022 11:00:15 CEST

# Options:
# -a          add usb name
# -d          delete usb name
# -h          show this screen
# -r          remove database
# -s          show  usb names
# --version   program version
##############################################################################
"""
Usage:
    manage_usb.py [options]

    manage_usb.py -a (add usb name)
    manage_usb.py -d (delete usb name)
    manage_usb.py -h (show this screen)
    manage_usb.py -r (REMOVE database)
    manage_usb.py -s (show usb names)

Options:
    -a          add usb name
    -d          delete usb name
    -h          show this screen
    -r          REMOVE database
    -s          show usb names
    --version   program version
"""
from docopt import docopt

from database import CreateDatabase

if __name__ == "__main__":
    args = docopt(__doc__, version="manage_usb.py v.1.1 - 2022")  # type: ignore

    db = CreateDatabase()

    if args["-a"]:
        print("add usb name")
        db.add_item()

    if args["-d"]:
        print("delete usb name")
        db.delete_item()

    if args["-r"]:
        print("remove database")
        print(db.delete_database())

    if args["-s"]:
        print("show usb names")
        print(db.show_items())
    else:
        print("Type manage_usb.py -h for help")
