#!/usr/bin/python3
"""Bunch of helpful utilities accross different projects"""

##############################################################################
# Author: Carlos Lacaci Moya
# Description: A bunch of Helper Clases and functions
# Modified Date: sáb 10 sep 2022 08:38:43 CEST
# version : 1.1
##############################################################################

import os
import subprocess
import signal
import sys
import socket
from pathlib import Path as path
from rich import print as pr
from rich.panel import Panel
from rich.console import Console
from rich.rule import Rule as rule
from rich.progress import Progress
from rich.table import Table
from PIL import Image  # type: ignore
from typing import Any
from notifypy import Notify


class RunCommand:
    """Execute command as a subprocess"""

    @staticmethod
    def run(command: Any) -> Any:
        """Run the command"""
        return subprocess.run(command,
                              capture_output=True,
                              text=True,
                              shell=True)


def abspath(file: str, dir: str = ".") -> str:
    """Returns the absolute path of a resource. 
       Default dir current working directory"""

    file_path = path(__file__).parent.absolute().joinpath(dir).joinpath(file)
    return str(file_path) if file_path.exists() else ""


def dirpath(dir: str) -> str:
    """Returns the absolute path of a directory"""

    dirpath = ""
    if path(dir).exists():
        p = path(dir)
        dirpath = str(p.resolve())
    else:
        pr(f"Folder: [bold red]<{dir}> does not exist![/bold red] :bomb: :boom:"
           )

    return dirpath


def clear_screen() -> None:
    """Clear the screen"""

    os.system("clear")


def is_host_oneline(ip_address: str, verbose: bool = False) -> bool:
    """Check if a host in online"""

    status = False
    try:
        host, _, ip = socket.gethostbyaddr(ip_address)
        if verbose:
            pr(f"Found host: [green]{host} [/green] with ip: [yellow]{ip}[/yellow] :thumbsup:"
               )
        status = True

    except socket.herror:
        pr(f"Unknown host: [bold red]{ip_address}[/bold red]")
        pr("[bold red]Are you online???[/bold red] :bomb: :boom:")
        sys.exit(1)
    return status


def show_image(name: str):
    """Show an image store in pictures folder"""

    # read the image
    image = abspath(f"{name}.jpg")
    im = Image.open(image)

    # show image
    im.show()


class BeautiPanel(Panel):
    """Write a message inside a panel. Inherit from rich.panel"""

    @staticmethod
    def draw_panel(fontcolor: str,
                   message: str,
                   borderstyle: str = "red") -> None:
        panel = Panel.fit(f"[bold {fontcolor}]{message}",
                          border_style=f"{borderstyle}")
        pr(panel)


class HeaderLine():
    """Write an underline title message"""

    @staticmethod
    def draw_line(message: str) -> None:
        console = Console()
        console.rule(f"[bold green underline]{message}")


class Rule_(rule):
    """Writes an underline title message. Inherits from rich.rule"""

    @staticmethod
    def draw_rule(message: str) -> None:
        console = Console()
        console.rule(f"[blink bold white on black]{message}")


def progress_bar():
    """Fake progress bar"""

    with Progress() as progress:
        task = progress.add_task("[green]Syncing ...", total=10000)

        while not progress.finished:
            progress.update(task, advance=0.01)


class Notification(Notify):
    """ Create an information message """

    def send_message(self, title: str, message: str, audio: Any = "") -> None:
        """ Send the message """
        self.title = title
        self.message = message
        if audio:
            self.audio = audio
        self.send()


class ShowTable:
    """Displays a table based on params passed"""

    def __init__(self, json_file: dict, columns: list) -> None:

        self.data = json_file
        self.columns = columns

        self.table = Table(show_header=True, header_style="bold blue")
        self.console = Console()
        self.display_data()

    def display_data(self):
        """ Fill in the table with data"""

        self.create_headers()
        self.create_rows()

        self.console.print(self.table)

    def create_headers(self):
        """Create table headers"""

        self.table.add_column("folder_id", min_width=2, justify="center")
        self.table.add_column("folder_to_track", min_width=10, justify="left")
        self.table.add_column("folder_to_copy_to",
                              min_width=10,
                              justify="left")

    def create_rows(self):
        """Create table rows"""

        for item in self.data["Folders"]:
            self.table.add_row(str(item['folder_id']), item['folder_to_track'],
                               item['folder_to_copy_to'])
