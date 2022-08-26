from __future__ import annotations

import code

import rich

from textual import events
from textual.message import Message
from textual.views import DockView
from textual.reactive import Reactive

from .data import Data
from .input import TextInput


class Repl(DockView):
    can_focus: bool = True
    has_focus: Reactive[bool] = Reactive(False)
    visible: bool = False
    layout_size: int = 3

    def __init__(self, data: Data) -> None:
        super().__init__(name="repl")
        self.data = data

        self.repl = TextInput(
            title=" ",
            placeholder="",
            prefix=">>> ",
            suffix="",
        )
        self.repl.on_change_handler_name = "handle_on_change_repl"

    async def on_mount(self, event: events.Mount) -> None:
        await self.dock(self.repl)

    async def on_show(self, event: events.Show) -> None:
        self.snapshot = len(self.data.dfs) - 1
        await self.repl.focus()

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True
        await self.repl.focus()

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

    async def run(self):
        exec(self.cmd)

    async def close(self, commit=False) -> None:
        if not commit:
            self.data.dfs = self.data.dfs[0:self.snapshot]
        await self.app.action_escape()

    async def handle_on_change_repl(self, message: Message) -> None:
        try:
            self.cmd = code.compile_command(message.sender.value)
            self.repl.valid = True
        except:
            self.repl.valid = False

    def reset(self) -> None:
        self.cmd = None
        self.repl.value = ""
