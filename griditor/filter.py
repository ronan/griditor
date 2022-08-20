from __future__ import annotations

import rich
from rich.console import RenderableType
from rich.style import StyleType
from rich.text import Text
from rich.panel import Panel
from rich import box
from rich.style import Style

from textual import events
from textual.geometry import SpacingDimensions
from textual.layouts.grid import GridLayout
from textual.message import Message
from textual.messages import CursorMove
from textual.scrollbar import ScrollTo, ScrollBar
from textual.geometry import clamp
from textual.view import View

from textual.widgets import Static

from textual.reactive import Reactive

from textual_inputs import IntegerInput, TextInput

class FilterTextInput(TextInput):
    def render(self) -> RenderableType:
        if self.has_focus:
            segments = self._render_text_with_cursor()
        else:
          segments = [".* "]

        segments = [Text("s/ ", style="dim" )] + segments + [Text("/g ", style="dim" )]

        text = Text.assemble(*segments)

        if (
            self.title
            and not self.placeholder
            and len(self.value) == 0
            and not self.has_focus
        ):
            title = ""
        else:
            title = self.title

        return Panel(
            text,
            title_align="left",
            height=3,
            style="dim" if not self.has_focus else "" ,
            box=box.HEAVY if self.has_focus else box.SQUARE,
        )



class Filter(View):
    datagrid = None
    has_focus: Reactive[bool] = Reactive(False)
    visible: False

    def __init__(
        self,
    ) -> None:
        from textual.views import WindowView

        self.regex = FilterTextInput(
            title="REGEX Filter",
            placeholder = "s//g",
            syntax="regex"
        )
        self.regex.on_change_handler_name = "handle_on_change_regex"

        self.window = WindowView(
            self.regex
        )
        layout = GridLayout()
        layout.add_column("regex")
        layout.add_row("main")
        layout.add_areas(
            content="regex,main",
        )
        layout.place(
            content=self.window,
        )
        super().__init__(name="filter", layout=layout)

    async def on_focus(self, event: events.Focus) -> None:
        self.has_focus = True
        await self.regex.focus()

    async def on_blur(self, event: events.Blur) -> None:
        self.has_focus = False

    async def on_key(self, event: events.Key) -> None:
        if event.key == "ctrl+i" or event.key == "escape":
            event.prevent_default().stop()
            await self.app.action_escape()

        await self.dispatch_key(event)

    async def handle_on_change_regex(self, message: Message) -> None:
        self.datagrid.filter(message.sender.value)

    def reset(self) -> None:
        self.regex.value = ""


    def __rich_repr__(self) -> rich.repr.Result:
        yield "name", "filters"
