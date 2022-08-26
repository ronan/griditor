from __future__ import annotations

import rich

from textual import events
from textual.layouts.grid import GridLayout
from textual.view import View
from textual.views import WindowView, DockView
from textual.reactive import Reactive

from .data import Data
from .input import TextInput


class Export(DockView):
    datagrid = None
    has_focus: Reactive[bool] = Reactive(False)
    data: Reactive[Data] = Reactive(Data())
    visible: Reactive[bool] = False
    layout_size: int = 3

    def __init__(self, data: Data, name: str | None = None) -> None:
        super().__init__(name="export")
        self.data = data
        self.filepath = TextInput(
            name="filepath",
            title="Export To",
            placeholder="~/.griditor/exports/output.csv",
            value="~/.griditor/exports/",
            prefix="export to:",
            suffix=".csv",
        )

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", "export"

    async def on_mount(self, event: events.Mount) -> None:
        await self.dock(self.filepath)

    async def on_key(self, event: events.Key) -> None:
        if event.key in ["ctrl+i", "escape"]:
            event.prevent_default().stop()
            await self.app.action_escape()

        if event.key == "enter":
            event.prevent_default().stop()
            await self.submit()

        await self.dispatch_key(event)

    async def on_show(self, event: events.Show) -> None:
        await self.filepath.focus()

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True
        await self.filepath.focus()

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def submit(self) -> None:
        if self.filepath.value:
            self.data.save(self.filepath.value)
        await self.app.action_escape()

    def reset(self) -> None:
        # self.filepath.value = ""
        return
