#!/usr/bin/python3
""" Basic Database management system """

##############################################################################
# Author: Carlos Lacaci Moya
# Description: Basic Database management system
# Date: jue 13 oct 2022 23:25:36 CEST
# CAUTION: DO NOT USE IT DIRECTLY. USE manage_usb.py INSTEAD.
# Dependencies: See below
##############################################################################
from pathlib import Path as path
import shelve
import sys
from typing import Any

from rich.console import Console

from helpers import RunCommand

# rich module
console = Console()


class CreateDatabase:
    """Create a Database for storing USB names using the shelve module"""

    def __init__(self) -> None:
        """Initalize the shelve object"""
        # Stores a copy of the dictionary
        self.temp_favorites: list = []
        # Flag to check if the database is opened
        self._db_opened: bool = False
        # Script path
        self.script_path: path = path(__file__).parent.absolute()
        # Database path
        self.db_path: path = self.script_path.joinpath("usbs.dbm")
        # Create database
        self._create_database()

    def _create_database(self) -> None:
        """Check if database exist"""

        # Database status
        self._db_opened: bool = True

        # Creating/Opening database
        self._shelve: Any = shelve.open(str(self.db_path), writeback=True)

        # Check for Data in the Database
        if not self._shelve.items():
            console.print(
                "[bold cyan]The database is empty!. Add some files ... [/bold cyan]"
            )
            self.add_item()

        else:
            self.temp_favorites: list = self._shelve["favorites"]
            # FOR DEBUGGING
            # print(self.temp_favorites)

            self._shelve.close()
            self._db_opened: bool = False

    def add_item(self) -> list:
        """Adding new item"""

        item = ""
        while item != "quit":
            if self._db_opened:

                # FOR DEBUGGING
                # print("db Opened")
                item: str = input("Enter the new item ('quit' to exit): ")

            else:
                # FOR DEBUGGING
                # print("db Closed")
                self._db_opened: bool = True

                item: str = input("Enter the new item ('quit' to exit): ")
                self._shelve: Any = shelve.open(str(self.db_path), writeback=True)

            if item == "quit":
                break

            # Inserting and swapping
            self.temp_favorites.append(item)
            self._shelve["favorites"] = self.temp_favorites
            self.temp_favorites = self._shelve["favorites"]

        self._shelve.close()
        self._db_opened: bool = False

        return self.temp_favorites

    def delete_item(self) -> list:
        """Deleting item"""

        if not self._db_opened:
            # DEBUG
            # console.print("[bold cyan]Database was not opened[/bold cyan]")
            self._shelve: Any = shelve.open(str(self.db_path), writeback=True)
            self._db_opened: bool = True

        self.temp_favorites = self._shelve["favorites"]
        if len(self.temp_favorites) == 0:
            console.print("[bold red]No items to delete[/bold red]")
            sys.exit(0)

        item: str = input("Enter the item to delete: ")
        if item in self.temp_favorites:
            self._delete_item(item)
        else:
            console.print("[bold red]Item not found! [/bold red]")
            sys.exit(0)

        return self.temp_favorites

    def _delete_item(self, item):
        item_idx: int = self.temp_favorites.index(item)
        del self.temp_favorites[item_idx]

        console.print(f"[bold red]item {[item]} deleted[/bold red]")

        self._shelve["favorites"] = self.temp_favorites

        self._shelve.close()
        self._db_opened: bool = False

    def show_items(self) -> list:
        """Show items in the shelve"""

        if not self.db_path.exists():
            console.print(
                "[bold red]The database does ot exist. Create a new one first![/bold red]"
            )
            sys.exit(0)

        if not self._db_opened:
            # FOR DEBUGGING
            # print("db was closed")
            self._shelve: Any = shelve.open(str(self.db_path), writeback=True)

            # FOR DEBUGGING
            # console.print("[bold cyan]Opening database ...[/bold cyan]")
            # Check for Data in the Database
            if not self._shelve.items():
                console.print(
                    "[bold red][!] The database is empty!. Add some files ... [/bold red]"
                )
                sys.exit(0)

            self.temp_favorites: list = self._shelve["favorites"]
        else:
            self.temp_favorites = self._shelve["favorites"]
        self._shelve.close()
        self._db_opened: bool = True

        self._db_opened: bool = False

        # FOR DEBUGGING
        # console.print(
        # "[bold cyan]Items in the database from show_items:[/bold cyan]")
        # print(self.temp_favorites)

        return self.temp_favorites

    def delete_database(self) -> None:
        """delete the database"""
        if not self.db_path.exists():
            console.print("[bold red]The database does not exist![/bold red]")
            sys.exit(0)

        if self._db_opened:
            self._shelve.close()
            self._db_opened: bool = False

        delete: str = f"rm {self.db_path}"

        prompt = ""
        while prompt.lower() not in ["y", "n"]:

            prompt: str = console.input("[bold red]DELETE DATABASE? (y/n) [/bold red]")
            if "y" in prompt.lower():
                RunCommand().run(delete)
            elif "n" in prompt.lower():
                sys.exit(0)
