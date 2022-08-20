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
    data = None
    df = None

    async def on_load(self, event: events.Load) -> None:
        self.df = pd.read_csv(file, parse_dates=True, na_values=[""])

        self.data = Data()
        self.data.load(file)

        await self.bind("q", "quit", "Quit")
        await self.bind("?", "view.toggle('help')", "Help")
        await self.bind("f", "view.toggle('filter')", "Filter")
        await self.bind("e", "view.toggle('export')", "Export")

        await self.bind("ctrl+i", "tab")
        await self.bind("escape", "escape")

    # # async def action_toggle_filter(self) -> None:
    # #     if self.filters.visible:
    # #         await self.action_escape()
    # #     else:
    # #         self.filters.visible = True
    # #         await self.filters.focus()
    # #     await self.view.refresh_layout()

    # async def action_toggle_export(self) -> None:
    #     if self.export.visible:
    #         await self.action_escape()
    #     else:
    #         self.export.visible = True
    #         await self.export.focus()
    #     await self.view.refresh_layout()

    async def action_escape(self) -> None:
        self.filter.reset()
        self.export.reset()
        self.export.visible = False
        self.filter.visible = False
        await self.grid.focus()
        await self.view.refresh_layout()

    async def action_tab(self) -> None:
        pass

    async def on_mount(self, event: events.Mount) -> None:
        self.grid = DataGrid(df=self.df, data=self.data)
        self.filter = Filter(data=self.data)
        self.export = Export(data=self.data)
        self.help = Help()

        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.filter, edge="bottom", size=3)
        await self.view.dock(self.export, edge="bottom", size=3)
        await self.view.dock(self.help, edge="bottom")
        await self.view.dock(self.grid, edge="bottom")

        await self.set_focus(self.grid)


def run():
    Griditor.run(title="Griditor", log="textual.log")
