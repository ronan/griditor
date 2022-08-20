import sys

import pandas as pd

from textual import events
from textual.app import App

from .data import Data
from .help import Help
from .footer import Footer
from .header import Header
from .datagrid import DataGrid
from .filter import Filter
from .export import Export

file = "demo.csv"
if 1 in sys.argv:
    file = sys.argv[1]


class Griditor(App):
    data = Data()
    df = None

    async def on_load(self, event: events.Load) -> None:
        self.data.load(file)

        await self.bind("q", "quit", "Quit")
        await self.bind("?", "view.toggle('help')", "Help")
        await self.bind("f", "view.toggle('filter')", "Filter")
        await self.bind("e", "view.toggle('export')", "Export")
        await self.bind("r", "reset", "Reset")
        await self.bind("ctrl+h", "delete", "Delete")

        await self.bind("ctrl+i", "tab")
        await self.bind("escape", "escape")

    async def action_escape(self) -> None:
        self.filter.reset()
        self.export.reset()
        self.export.visible = False
        self.filter.visible = False
        await self.grid.focus()
        await self.view.refresh_layout()

    async def action_tab(self) -> None:
        pass

    async def action_reset(self) -> None:
        self.data.restore()
        self.filter.reset()
        self.export.reset()

    async def action_delete(self) -> None:
        self.data.delete_col()

    async def on_mount(self, event: events.Mount) -> None:
        self.grid = DataGrid(data=self.data)
        self.filter = Filter(data=self.data)
        self.export = Export(data=self.data)
        self.help = Help()

        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.filter, edge="bottom")
        await self.view.dock(self.export, edge="bottom")
        await self.view.dock(self.help, edge="bottom")
        await self.view.dock(self.grid, edge="bottom")

        await self.set_focus(self.grid)


def run():
    Griditor.run(title="Griditor", log="textual.log")
