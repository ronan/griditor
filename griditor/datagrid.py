import json, csv, os, random, psutil, math, sys
from pprint import pformat
from datetime import datetime

import pandas as pd

from rich import box
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich.console import RenderableType, Console
from rich.pretty import Pretty
from rich.text import Text

from textual import events
from textual.app import Widget, Reactive, log
from textual.widgets import Placeholder

PAST = 950000000
FUTURE = 1900000000


def clamp(val, min, max):
    if val < min: return min
    if val > max: return max
    return val


def value_renderable(value) -> RenderableType:
    if isinstance(value, float) and math.isnan(value):
        return Text("∅", style="dim")

    if isinstance(value, float) and PAST < int(value) < FUTURE:
        return Text(datetime.fromtimestamp(value).strftime("%Y-%b-%d"))

    if isinstance(value, bool):
        return Text("✅", style="green") if value else Text("❌")

    return str(value)


class DataGrid(Widget, can_focus=True):
    can_focus: bool = True

    original_df = None
    df = None
    data = None
    
    selected_col: Reactive[int] = Reactive(0)
    offset: Reactive[int] = Reactive(0)
    zeroidx: Reactive[bool] = Reactive(False)

    has_focus: Reactive[bool] = Reactive(False)
    mouse_over: Reactive[bool] = Reactive(False)
    height: Reactive[int] = Reactive(20)

    def __init__(
        self,
        name: str = None,
        df = None,
        data = None
    ) -> None:
        super().__init__(name)

        self.original_df = df
        self.dfs = df.copy()
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
        self.scroll(1)

    async def key_up(self) -> None:
        self.scroll(-1)

    async def key_pagedown(self) -> None:
        self.scroll(self.get_page_size())

    async def key_pageup(self) -> None:
        self.scroll(-self.get_page_size())

    async def key_home(self) -> None:
        self.offset = 0

    async def key_end(self) -> None:
        self.scroll(len(self.data.df.index))

    async def key_left(self) -> None:
        self.move_column_selection(-1)

    async def key_right(self) -> None:
        self.move_column_selection(1)

    async def key_x(self) -> None:
        self.shuffle()

    async def key_c(self) -> None:
        self.clean()

    async def key_r(self) -> None:
        self.reset()

    async def key_g(self) -> None:
        self.group()

    async def key_z(self) -> None:
        self.zeroidx = not self.zeroidx

    async def key_w(self) -> None:
        self.data.sort(self.selected_col)

    async def key_s(self) -> None:
        self.data.rsort(self.selected_col)

    def reset(self) -> None:
        self.data.restore()
        self.select_column(0)
        self.offset = 0

    def shuffle(self) -> None:
        self.data.shuffle()

    def clean(self) -> None:
        self.data.clean()

    def scroll(self, delta: int = 1) -> None:
        self.offset = clamp(self.offset + delta, 0, len(self.data.df.index) - self.get_page_size())

    def filter(self, query: str = "") -> None:
        data.filter(self.selected_col, query)

    def move_column_selection(self, delta) -> None:
        self.select_column(self.selected_col + delta)

    def select_column(self, idx) -> None:
        self.selected_col = clamp(idx, 0, len(self.data.df.index) - 1)

    def get_page_size(self) -> None:
        return self.size.height - 7

    def get_styles(self) -> dict:
        styles = {
                "panel": "dim",
                "column": "white",
                "selected": "white on bright_black",
                "header": "white",
                "index": "dim",
                "box": box.SIMPLE
            }

        if self.has_focus:
            styles.update({
                "panel": "white",
                "selected": "white on dark_green",
            })
        return styles

    def render(self) -> RenderableType:
        num_rows = len(self.data.df.index)
        # num_rows = len(self.df.index)

        styles = self.get_styles()
        visible = self.get_page_size()
        start = clamp(self.offset, 0, num_rows - 1)
        end = clamp(start + visible, 0, num_rows - 1)

        out = table = Table(
            expand=True,
            caption=f"{len(self.data.df.index)} of {len(self.data.df_0.index)} records. POS: {self.selected_col}, {self.offset}",
            box=styles['box']
        )
        out = Panel(out, style=styles['panel'])

        table.add_column("", style=styles['index'], justify="right")

        # Add Cols
        for index, column in self.data.headers():
            style = styles['selected'] if index == self.selected_col else styles['column']
            table.add_column(column, style=style, header_style=styles['header'])

        # Add Rows
        skew = +1 if not self.zeroidx else 0
        for index, value_list in self.data.slice(start, end):
            row = [value_renderable(x) for x in value_list]
            table.add_row(str(index + start + skew), *row)

        return Panel(table, box=box.ROUNDED, style=styles['panel'])