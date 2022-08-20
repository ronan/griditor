from textual.app import Widget, Reactive, log

from rich import box
from rich.table import Table
from rich.console import RenderableType
from rich.panel import Panel


class Help(Widget):
    can_focus: bool = True
    visible: Reactive[bool] = False

    def __init__(
        self,
    ) -> None:
        super().__init__("help")

    def render(self) -> RenderableType:
        table = Table.grid(padding=(0, 1), expand=True)
        table.style = "bold white on dark_blue"
        table.add_column("key", justify="right", width=4, style="bold white")
        table.add_column("command", justify="left", width=10)
        table.add_column("help", justify="left", ratio=1)

        table.add_row(f"Q", "Quit", "Exit Griditor")
        table.add_row(f"?", "Help", "Show this help screen")
        table.add_row(f"X", "Shuffle", "Randomize the order of all rows")
        table.add_row(
            f"C", "Clean", "Remove all rows where the selected column is empty"
        )
        table.add_row(f"S", "Sort ↓", "Sort rows by the selected column")
        table.add_row(f"W", "Sort ↑", "Reverse sort rows by the selected column")
        table.add_row(f"R", "Reset", "Revert to the original data set")

        self.layout_size = 11

        return Panel(
            table,
            title="Help",
            border_style="blue",
            box=box.ROUNDED,
            height=self.layout_size,
            padding=(1, 0),
        )
