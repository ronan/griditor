from __future__ import annotations

from typing import List

import pandas as pd


def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val


class Data:
    df: pd.DataFrame = None
    df_0: pd.DataFrame = None
    dfs: List[pd.DataFrame] = []
    cursor: List[int] = [0, 0]

    def load(self, file: str) -> None:
        self.df_0 = self.df = pd.read_csv(file, parse_dates=True, na_values=[""])

    def save(self, filepath: str) -> None:
        self.df.to_csv(f"{filepath}.csv")

    def restore(self) -> None:
        self.reset_cursor()
        self.df = self.df_0.copy()

    def create_snapshot(self) -> None:
        self.dfs.append(self.df)

    def restore_snapshot(self) -> None:
        self.df = self.dfs[-1]

    def discard_snapshot(self) -> None:
        self.dfs.pop()

    def shuffle(self) -> None:
        self.df = self.df.sample(frac=1)

    def clean(self):
        self.df = self.df.loc[self.col().notnull()]

    def filter(self, query: str = "") -> None:
        self.clean()
        self.df = self.df.loc[self.col().str.contains(query, case=False)]

    def sort(self):
        self.df = self.df.sort_values(
            by=self.col().name, ascending=True, na_position="first"
        )

    def rsort(self):
        self.df = self.df.sort_values(
            by=self.col().name, ascending=False, na_position="last"
        )

    def headers(self) -> list:
        return list(enumerate(self.df.columns))

    def header(self, idx: int) -> str:
        return self.df.columns[idx]

    def slice(self, start: int = 0, end: int | None = None):
        return enumerate(self.df[start:end].values.tolist())

    def col(self, idx: int | None = None) -> pd.Series:
        if idx is not None:
            return self.df.iloc[:, idx]
        elif self.cursor[0] is not None:
            return self.col(self.cursor[0])

    def move_cursor(self, col_delta: int = 0, row_delta: int = 0) -> None:
        self.set_cursor(col=self.cursor[0] + col_delta, row=self.cursor[1] + row_delta)
        return

    def set_cursor(self, col: int = 0, row: int = 0):
        self.cursor[0] = clamp(col, 0, len(self.df.columns))
        self.cursor[1] = clamp(row, 0, len(self.df.index))

    def reset_cursor(self):
        self.set_cursor()
