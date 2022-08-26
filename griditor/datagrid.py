from __future__ import annotations

import math
from datetime import datetime

from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.console import RenderableType
from rich.pretty import Pretty
from rich.text import Text

from textual import events
from textual.app import Widget, Reactive

from .data import Data

PAST = 950000000
FUTURE = 1900000000


def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val


def value_renderable(value) -> RenderableType:
    if isinstance(value, float) and math.isnan(value):
        return Text("∅", style="dim")

    if (isinstance(value, float) or isinstance(value, int)) and PAST < int(value) < FUTURE:
        return Text(datetime.fromtimestamp(value).strftime("%Y-%b-%d"))

    if isinstance(value, bool):
        return Text("✅", style="green") if value else Text("❌")

    return str(value)


class DataGrid(Widget, can_focus=True):
    can_focus: bool = True

    data: Data = Data()

    zero_idx: Reactive[bool] = Reactive(False)

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    height: Reactive[int] = Reactive(20)
    max_cols: Reactive[int] = Reactive(11)

    def __init__(self, data: Data, name: str | None = None) -> None:
        super().__init__(name)
        self.data = data
        self.reset()

    async def on_mount(self, event: events.Mount) -> None:
        self.set_interval(0.1, callback=self.refresh)

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_key(self, event: events.Key) -> None:
        await self.dispatch_key(event)

    async def key_down(self) -> None:
        self.data.move_cursor(row_delta=1)

    async def key_up(self) -> None:
        self.data.move_cursor(row_delta=-1)

    async def key_pagedown(self) -> None:
        self.data.move_cursor(row_delta=self.get_page_size())

    async def key_pageup(self) -> None:
        self.data.move_cursor(row_delta=self.get_page_size())

    async def key_home(self) -> None:
        self.data.set_cursor(0, 0)

    async def key_end(self) -> None:
        self.data.set_cursor(len(self.data.df.columns),
                             len(self.data.df.index))

    async def key_left(self) -> None:
        self.data.move_cursor(col_delta=-1)

    async def key_right(self) -> None:
        self.data.move_cursor(col_delta=1)

    async def key_x(self) -> None:
        self.data.df = self.data.df.sample(frac=1)

    async def key_c(self) -> None:
        self.data.clean()

    async def key_zero(self) -> None:
        self.zero_idx = not self.zero_idx

    async def key_w(self) -> None:
        self.data.rsort()

    async def key_s(self) -> None:
        self.data.sort()

    def reset(self) -> None:
        self.data.restore()

    def clean(self) -> None:
        self.data.clean()

    def scroll(self, delta: int = 1) -> None:
        self.data.move_cursor(row_delta=delta)

    def filter(self, query: str = "") -> None:
        self.data.filter(query)

    def get_page_size(self) -> int:
        return self.size.height - 7

    def get_styles(self) -> dict:
        styles = {
            "panel": "dim",
            "column": "white",
            "row": "",
            "selected_row": "bold red",
            "selected": "white on bright_black",
            "header": "white",
            "index": "dim",
            "box": box.SIMPLE,
        }

        if self.has_focus:
            styles.update(
                {
                    "panel": "white",
                    "selected": "white on dark_green",
                }
            )
        return styles

    def render(self) -> RenderableType:
        styles = self.get_styles()

        num_cols = min(self.max_cols, len(self.data.df.columns))

        first_col = clamp(
            self.data.cursor[0] - self.max_cols + 1, 0, len(self.data.df.columns))
        last_col = clamp(first_col + num_cols, 0, len(self.data.df.columns))

        out = table = Table(
            expand=True,
            box=styles["box"],
            show_footer=True,
        )
        out = Panel(out, style=styles["panel"])

        table.add_column(
            "", style=styles["index"], justify="right")
        for index, column in self.data.headers()[first_col:last_col]:
            style = (
                styles["selected"] if index == self.data.cursor[0] else styles["column"]
            )
            table.add_column(
                column,
                style=style,
                header_style=styles["header"],
            )

        num_rows = len(self.data.df.index)
        page_size = self.get_page_size()

        first_row = clamp(
            self.data.cursor[1] - page_size//2, 0, num_rows - 1)
        last_row = clamp(first_row + page_size, 0, num_rows)
        first_row = clamp(last_row - page_size, 0, num_rows - 1)

        skew = +1 if not self.zero_idx else 0
        for index, value_list in self.data.df[first_row:last_row].iterrows():
            style = (
                styles["selected_row"] if index == self.data.cursor[1] else styles["row"]
            )
            row = [value_renderable(x) for x in value_list]
            row = row[first_col:last_col]
            table.add_row(str(index + skew), *row, style=style)

        return Panel(table, box=box.ROUNDED, style=styles["panel"])
