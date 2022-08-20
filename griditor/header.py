import psutil, os
from textual.app import Widget, Reactive, log

from rich import box
from rich.table import Table
from rich.text import Text
from rich.console import RenderableType


class Header(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.layout_size = 1

    def render(self) -> RenderableType:
        table = Table.grid(padding=(0, 1), expand=True)
        table.style = "bold white on dark_blue"
        table.add_column("appname", justify="left", style="cyan")
        table.add_column("version", justify="right")

        table.add_row("🄶 🅁 🄸 🄳 🄸 🅃 🄾 🅁", "v0.1.0")
        return table
