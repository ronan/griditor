import os
import sys
from rich.console import RenderableType

from textual import events

from rich.syntax import Syntax
from rich.traceback import Traceback
from rich.text import Text
from rich.panel import Panel

from textual.app import App, View, log
from textual.widgets import Header, Footer, FileClick, ScrollView, DirectoryTree, Placeholder, Static, TreeControl
from textual.views import DockView
from textual_inputs import IntegerInput, TextInput
from textual._easing import EASING

class TestPanel(ScrollView):
    
    async def on_mount(self, event: events.Mount) -> None:
        out = Text("Hello")
        out = TextInput(title="REGEX")
        # out = View(out)
        await self.window.update(out)


class MyApp(App):
    """An example of a very simple Textual App"""

    async def on_load(self) -> None:
        """Sent before going in to application mode."""

        # Bind our basic keys
        await self.bind("b", "view.toggle('help')", "Toggle sidebar")
        await self.bind("q", "quit", "Quit")


    async def on_mount(self) -> None:
        """Call after terminal goes in to application mode"""

        # # Create our widgets
        # # In this a scroll view for the code and a directory tree
        # self.body = Placeholder()
        # self.help = Placeholder(name="Help")

        # # Dock our widgets
        # await self.view.dock(Header(), edge="top")
        # await self.view.dock(Footer(), edge="bottom", size=3)
        # await self.view.dock(self.help, edge="bottom", z=1, size=11, name="help")
        # await self.view.action_toggle("help")

        self.editor = DockView()
        await self.view.dock(self.editor, edge="top")
        await self.editor.dock(Static(Panel("lo")), edge="bottom", size=3)
        await self.editor.dock(Static(Panel("hi")), edge="bottom")

        # self.placeholder = Placeholder()
        # self.easing_view = DockView()
        # self.placeholder.style = "white on dark_blue"

        # await self.view.dock(self.easing_view)
        # await self.easing_view.dock(Placeholder(), edge="top")
        # await self.easing_view.dock(Placeholder(), edge="bottom", size=10)

# Run our app class
MyApp.run(title="UI Viewer", log="textual.log")
