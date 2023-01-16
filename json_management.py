#!/usr/bin/python3

##############################################################################
# Idea from: Carlos Lacaci Moya
# Author: CLM
# Description: Manage the JSON file operations like a database
# Date: mar 18 oct 2022 16:59:46 CEST
# Dependencies:
##############################################################################
import json
import shutil
from helpers import (abspath, Rule_, BeautiPanel, ShowTable, clear_screen,
                     ShowTable)
from collections import defaultdict
from dataclasses import dataclass, field
from rich.console import Console

console = Console()


@dataclass
class ManageJson:

    file_path: str = abspath("folders.json")
    backup_file_path: str = abspath("folders.json.bak")

    json_structure: list = field(default_factory=list)
    json_file: dict = field(default_factory=dict[str, str])

    def __post_init__(self) -> None:
        """ Initialize init variables """

        self.json_structure: list = [
            "folder_id", "folder_to_track", "folder_to_copy_to"
        ]

        self.json_file = self.load_json_file()

    def load_json_file(self) -> dict:
        """ Load the json_file """

        with open(self.file_path, "r+") as jf:
            self.json_file = json.load(jf)

        return self.json_file

    def edit_json_file(self) -> None:
        """ Edit the json_file """

        Rule_.draw_rule("Edit json_file <folders.json>")

        found_record: bool = False

        ShowTable(self.json_file, self.json_structure)

        id_number = console.input(
            "Type the [green]folder id[/green] to modify: ")

        for element in self.json_file["Folders"]:
            if element["folder_id"] == id_number:
                found_record: bool = True  # There's a match
                for item in self.json_structure:

                    # This returns True if you want to modify it
                    # else the for goes for next iteration
                    if self.modify_data(id_number, item):
                        if value := console.input(
                                f"Enter the new value for [green]{item}[/green] of [green]{id_number}[/green]): "
                        ):
                            element[item] = value

        if not found_record:  # Flag is False
            BeautiPanel.draw_panel(
                fontcolor="yellow",
                message="Record not found or wrong key pressed!",
                borderstyle="red")
        else:
            self.dump_to_json_file()

        input("\nPress any key to continue ...")
        clear_screen()

    def add_data(self) -> None:
        """Add new data to json_file"""

        Rule_.draw_rule(message='Adding data')

        self.new_entries: defaultdict[str, str] = defaultdict(str)

        # Show the next id to insert
        next_id: int = self.get_last_id()
        next_id += 1

        BeautiPanel.draw_panel(fontcolor="yellow",
                               message=f"The next id to insert is: {next_id}",
                               borderstyle="red")

        for item in self.json_structure:
            if get_data := console.input(f"Add [green]{item}: [/green]"):
                self.new_entries[item] = get_data

                BeautiPanel.draw_panel(
                    fontcolor="yellow",
                    message=f"Inserted <{self.new_entries[item]}> in <{item}>",
                    borderstyle="red")

            else:
                BeautiPanel.draw_panel(fontcolor="yellow",
                                       message=f"Inserted <null> in <{item}>",
                                       borderstyle="red")

                self.new_entries[item] = "null"

        self.json_file['Folders'].append(self.new_entries)

        self.dump_to_json_file()

    def modify_data(self, id_number: str, item: str) -> bool:
        """ Returns True if you want to modify the field """

        message = "Type 'yes' to modify, any key leave field untouched"

        BeautiPanel.draw_panel(fontcolor="yellow",
                               message=f"{message}",
                               borderstyle="red")

        modify = console.input(
            f"Do you want to modify the field [bold]{item}[/bold] of record [bold]{id_number}[/bold]?: "
        )
        return "yes".lower() in modify

    def dump_to_json_file(self) -> None:
        """ Write data to the json_file """

        with open(self.file_path, "w") as file_output:
            json.dump(self.json_file, file_output, indent=2)

    def get_last_id(self) -> int:
        """Get the last id of the folder in the json_file"""

        last_id = [item['folder_id'] for item in self.json_file["Folders"]]

        return int(last_id[-1])

    def view_data(self) -> None:
        """ Display json data in a Table"""

        json_file = self.load_json_file()
        Rule_.draw_rule("Folders to watch")

        ShowTable(json_file, self.json_structure)

    def delete_data(self) -> None:
        """deletes data entries by folder_id"""

        Rule_.draw_rule("Deleting")

        ShowTable(self.json_file, self.json_structure)

        if id_number := console.input(
                "[bold red]Which folder id would like you delete?: [/bold red]"
        ):
            for element in self.json_file["Folders"]:
                if id_number in element["folder_id"]:

                    for item in self.json_structure:
                        del element[item]

            self.dump_to_json_file()

            # Remove dangling empty {} from json_file"""
            self.clean_dictionary(id_number)

    def clean_dictionary(self, id_number: str) -> None:
        """Remove empty {} from json_file"""

        unwanted_item: list[str] = ['{}']

        for item in self.json_file["Folders"]:
            # Found an empty {}
            if str(item) == unwanted_item[0]:
                self.json_file["Folders"].remove(item)

                BeautiPanel.draw_panel(
                    fontcolor="yellow",
                    message=f"Folder id <{id_number} deleted>",
                    borderstyle="red")

        self.dump_to_json_file()

    def backup_data(self) -> None:
        """ Backup the json file in .bak format"""

        Rule_.draw_rule("Backing up")

        try:
            if self.file_path:
                shutil.copyfile(self.file_path, self.backup_file_path)
                BeautiPanel.draw_panel(
                    fontcolor="green",
                    message=f"[+] Backup <{self.backup_file_path}> created",
                    borderstyle="blue")

                input("Press any key ...")
                clear_screen()

        except FileNotFoundError:
            BeautiPanel.draw_panel(
                fontcolor="yellow",
                message=f"[!] <{self.file_path}> not found!",
                borderstyle="red")

    def restore_data(self) -> None:
        """ Restore the json backup file"""

        Rule_.draw_rule("Restoring backup")
        try:
            if self.backup_file_path:
                shutil.copyfile(self.backup_file_path, self.file_path)
                BeautiPanel.draw_panel(
                    fontcolor="green",
                    message=f"[+] <{self.file_path}> restored",
                    borderstyle="blue")

        except FileNotFoundError:
            BeautiPanel.draw_panel(
                fontcolor="yellow",
                message=f"[!] <{self.file_path}> not found!",
                borderstyle="red")
