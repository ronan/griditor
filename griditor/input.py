from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Tuple, Union

from textual.reactive import Reactive

from textual_inputs import TextInput as BaseTextInput
from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from rich import box


class TextInput(BaseTextInput):
    name: Optional[str] = "None"
    title: Optional[str] = None
    value: Optional[str] = None
    valid: Reactive[bool] = Reactive(False)

    def __init__(
        self,
        name: Optional[str] = None,
        value: str = "",
        placeholder: str = "",
        title: str = "",
        password: bool = False,
        syntax: Optional[str] = None,
        prefix: Optional[str] = None,
        suffix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            name=name,
            value=value,
            placeholder=placeholder,
            title=title,
            password=password,
            syntax=syntax,
            **kwargs,
        )
        self.prefix = prefix
        self.suffix = suffix

    def __rich_repr__(self):
        yield "name", self.name
        yield "title", self.title
        yield "value", self.value

    def render(self) -> RenderableType:
        if self.has_focus:
            segments = self._render_text_with_cursor()
        else:
            segments = [".* "]

        if self.prefix:
            segments = [Text(self.prefix, style="dim")] + segments
        if self.suffix:
            segments = segments + [Text(self.suffix, style="dim")]

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

        style = "green" if self.valid else "red"
        return Panel(
            text,
            title_align="left",
            height=3,
            style="dim" if not self.has_focus else style,
            box=box.SQUARE,
        )
