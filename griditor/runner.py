from collections.abc import Callable
import sys

import asyncio

from textual import events
from textual.app import log

from .app import Griditor


class Runner(Griditor):
    fn: Callable = log
    running = False
    tasks = []

    def __init__(
        self,
        **kwargs
    ):
        self.fn = kwargs.pop('fn')
        self.src = kwargs.pop('src')
        super().__init__(**kwargs)

    async def on_load(self, event: events.Load) -> None:
        await self.bind("l", "restart", "Run")
        await self.bind("k", "pause", "Run")
        self.set_timer(1, lambda: self.action("restart"))

    async def process_row(self, tasks):
        if not self.running:
            return

        try:
            idx = next(tasks)
            log(f"Processing row {idx} of {len(self.data.df)}")
            await self.fn(self.data, idx)
            log(("-" * 60), "done")
            self.data.cursor[1] = idx
            self.grid.refresh()
        except StopIteration:
            self.running = False
        except Exception as e:
            log(("!" * 60), f"\n{e}\n", ("!" * 60))
        finally:
            await self.call_later(Runner.process_row, self, tasks)
            await asyncio.sleep(0)

    async def action_restart(self):
        self.running = True
        await self.call_later(Runner.process_row, self, iter(self.data.df.index.to_list()))

    async def action_pause(self):
        self.running = not self.running


def run(src, fn):
    Runner.run(title="Griditor", log="textual.log", fn=fn, src=src)
