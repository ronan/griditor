from textual.app import Widget


from rich import box
# from rich.table import Table
from rich.console import RenderableType
from rich.panel import Panel
from rich.text import Text
from textual import events

from .data import Data


class Info(Widget):
    data: Data = Data()

    def __init__(self, data: Data, name: str | None = None) -> None:
        super().__init__("info")
        self.data = data

    async def on_mount(self, event: events.Mount) -> None:
        self.set_interval(0.1, callback=self.refresh)

    def render(self) -> RenderableType:
        self.layout_size = 2

        out = Text(
            f"ROWS: {len(self.data.df.index):n}/{len(self.data.df_0.index):n} | " +
            f"POS: {self.data.cursor[0]},{self.data.cursor[1]} | " +
            f"COL: {self.data.col().name} | " +
            f"VER: {len(self.data.dfs)}",
        )

        return out
