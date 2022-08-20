import sys

import pandas as pd

from textual import events
from textual.app import App, Reactive, log, View
from textual.widgets import Placeholder, Static
from textual.widgets import ScrollView
from textual.keys import Keys
from textual.views import GridView, DockView

from rich.text import Text
from rich.layout import Layout
from rich.pretty import Pretty

from .help import Help
from .footer import Footer
from .header import Header
from .datagrid import DataGrid
from .filter import Filter
from .data import Data

from textual_inputs import IntegerInput, TextInput


file = "demo.csv"
if 1 in sys.argv:
    file = sys.argv[1]


class Griditor(App):

    filter_field: None
    filter_match: ""

    header = []
    data = None
    df = None

    show_help = Reactive(False)

    async def on_load(self, event: events.Load) -> None:
        self.df = pd.read_csv(file, parse_dates=True, na_values=[""])

        self.data = Data()
        self.data.load(file)

        await self.bind("q", "quit", "Quit")
        await self.bind("?", "view.toggle('help')", "Help")
        await self.bind("f, ctrl+i, escape, enter", "toggle_filter", "Filter")

    async def action_toggle_help(self) -> None:
        self.help.toggle()

    async def action_toggle_filter(self) -> None:
        if self.filters.visible:
            await self.action_escape()
        else:
            self.filters.visible = True
            await self.view.refresh_layout()
            await self.filters.focus()

    async def action_escape(self) -> None:
        self.filters.visible = False
        self.filters.reset()
        await self.view.refresh_layout()
        await self.grid.focus()

    async def on_mount(self, event: events.Mount) -> None:
        self.grid = DataGrid(df=self.df, data=self.data)
        self.filters = Filter()
        self.filters.datagrid = self.grid
        self.filters.df = self.df
        self.filters.visible = False
        self.help = Help()
        self.help.visible = False

        await self.view.dock(Header(), edge="top")
        await self.view.dock(Footer(), edge="bottom")
        await self.view.dock(self.filters, edge="bottom", size=3)
        await self.view.dock(self.help, edge="bottom")
        await self.view.dock(self.grid, edge="bottom")

        await self.set_focus(self.grid)



def run():
    Griditor.run(title="Griditor", log="textual.log")
