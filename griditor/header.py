import psutil, os
from textual.app import Widget, Reactive, log

from rich import box
from rich.table import Table
from rich.text import Text
from rich.console import RenderableType
from rich.panel import Panel

class Header(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.layout_size = 2

    def render(self) -> RenderableType:
        table = Table.grid(padding=(0, 1), expand=True)
        table.style = "bold white on dark_blue"
        table.add_column("appname", justify="left", width=20, style="")
        table.add_column("versio", justify="right")

        memory = psutil.Process(os.getpid()).memory_info().rss / (1024*1024)
        table.add_row(
            Text(f"🄶 🅁 🄸 🄳 🄸 🅃 🄾 🅁", style="cyan"),
             f"v0.1.0"
        )
        return table