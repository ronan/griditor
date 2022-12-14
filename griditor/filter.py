from __future__ import annotations

import re

import rich

from textual import events
from textual.message import Message
from textual.views import DockView
from textual.reactive import Reactive

from .data import Data
from .input import TextInput


class Filter(DockView):
    can_focus: bool = True
    has_focus: Reactive[bool] = Reactive(False)
    visible: bool = False
    layout_size: int = 3

    def __init__(self, data: Data) -> None:
        super().__init__(name="filter")
        self.data = data

        self.regex = TextInput(
            title=" ",
            placeholder=".*",
            prefix="s/ ",
            suffix=" /g",
        )
        self.regex.on_change_handler_name = "handle_on_change_regex"

    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", "filter"

    async def on_mount(self, event: events.Mount) -> None:
        await self.dock(self.regex)

    async def on_show(self, event: events.Show) -> None:
        self.snapshot = len(self.data.dfs) - 1
        await self.regex.focus()

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True
        await self.regex.focus()

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False
        await self.close(False)

    async def on_key(self, event: events.Key) -> None:
        if event.key in ["escape"]:
            event.prevent_default().stop()
            await self.close(commit=False)

        if event.key in ["enter", "return"]:
            event.prevent_default().stop()
            await self.close(commit=True)

        await self.dispatch_key(event)

    async def close(self, commit=False) -> None:
        if not commit:
            self.data.dfs = self.data.dfs[0:self.snapshot]
        await self.app.action_escape()

    async def handle_on_change_regex(self, message: Message) -> None:
        try:
            re.compile(message.sender.value)
            self.regex.valid = True
        except re.error:
            self.regex.valid = False

        self.data.dfs = self.data.dfs[0:self.snapshot]
        self.data.filter(message.sender.value)

    def reset(self) -> None:
        self.regex.value = ""
