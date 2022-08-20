import psutil, os
from textual.app import Widget, Reactive, log

from rich import box
from rich.table import Table
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text


class Footer(Widget):
    def __init__(self) -> None:
        super().__init__()
        self.layout_size = 1

    def render(self) -> RenderableType:

        table = Table.grid(padding=(0, 1), expand=True)
        table.style = "bold white on dark_blue"
        table.add_column("help", justify="left")
        table.add_column("stats", justify="right")

        def render_key(key: str, label: str):
            return Text.assemble(
                Text(f" {key} ", style="white"),
                Text(f" {label} ", style="black on cyan"),
            )

        keys = Text.assemble(
            render_key("?", "Help"),
            render_key("R", "Revert"),
            render_key("E", "Export"),
            render_key("Q", "Quit"),
        )

        memory = psutil.Process(os.getpid()).memory_info().rss / (1024 * 1024)
        table.add_row(keys, f"RAM: {memory:.0f} MB")
        return table
