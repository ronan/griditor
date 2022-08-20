import psutil, os
from textual.app import Widget, Reactive, log

from rich import box
from rich.table import Table
from rich.console import RenderableType
from rich.panel import Panel


class Footer(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.layout_size = 1

    def render(self) -> RenderableType:

        table = Table.grid(padding=(0, 1), expand=True)
        table.style = "bold white on dark_blue"
        table.add_column("help", justify="left")
        table.add_column("stats", justify="right")

        memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        table.add_row("?: Show Help  Q: Quit", f"RAM: {memory:.0f} MB")
        return table
