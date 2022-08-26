from __future__ import annotations
from typing import List

import re
from urllib.parse import urlparse
import mysql.connector as mysql

import pandas as pd
from pandas import DataFrame


def clamp(val, min, max):
    if val < min:
        return min
    if val > max:
        return max
    return val


class Data:
    df_0: DataFrame = DataFrame()
    dfs: List[DataFrame] = []
    cursor: List[int] = [0, 0]
    src: str = ""

    @property
    def df(self) -> DataFrame:
        if len(self.dfs) > 0:
            return self.dfs[-1]
        return pd.DataFrame()

    @df.setter  # property-name.setter decorator
    def df(self, value):
        self.dfs.append(value)

    def load(self, file: str) -> None:
        df = DataFrame
        self.src = file
        if file[:8] == "mysql://":
            result = urlparse(file)
            conn = mysql.connect(
                host=result.hostname,
                user=result.username,
                passwd=result.password,
                db=result.path[1:],
            )
            df = pd.read_sql(
                f"SELECT * FROM {result.fragment}", con=conn
            )
        else:
            df = pd.read_csv(
                file,
                parse_dates=True,
                na_values=["", "-"],
                sep=None,
                engine='python'
            )

        if isinstance(df, DataFrame):
            df.columns = [col.strip() for col in df.columns]
            self.dfs = [df]

    def save(self, filepath: str) -> None:
        self.df.to_csv(f"{filepath}.csv")

    def restore(self) -> None:
        self.reset_cursor()
        self.df = self.dfs[0].copy()

    def create_snapshot(self) -> None:
        self.dfs.append(self.df)

    def restore_snapshot(self) -> None:
        self.df = self.dfs[-1]

    def discard_snapshot(self) -> None:
        if len(self.dfs) > 1:
            self.dfs.pop()

    def delete_col(self):
        if len(self.df.columns):
            self.df = self.df.drop(self.col().name, axis=1)
            self.move_cursor(col_delta=-1)

    def clean(self):
        df = self.df.loc[self.col().notnull()]
        self.df = df.loc[self.col() != ""]

    def filter(self, query: str = "") -> None:
        try:
            re.compile(query)
            self.clean()
            self.df = self.df.loc[self.col().str.contains(query, case=False)]
        except re.error:
            pass

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

    def col(self, idx: int | None = None) -> pd.Series:
        if idx is not None and idx < len(self.df.columns):
            return self.df.iloc[:, idx]
        elif self.cursor[0] is not None:
            return self.col(self.cursor[0])
        return pd.Series()

    def row(self, idx: int | None = None) -> pd.Series:
        if idx is not None and idx < len(self.df.index):
            return self.df.iloc[idx, :]
        elif self.cursor[1] is not None:
            return self.row(self.cursor[1])
        return pd.Series()

    def next_row(self) -> pd.Series | None:
        if self.cursor[1] > len(self.df.index):
            return None

        row = self.row(self.cursor[1])
        self.move_cursor(row_delta=1)
        return row

    def move_cursor(self, col_delta: int = 0, row_delta: int = 0) -> None:
        self.set_cursor(
            col=self.cursor[0] + col_delta, row=self.cursor[1] + row_delta)
        return

    def set_cursor(self, col: int = 0, row: int = 0):
        self.cursor[0] = clamp(col, 0, len(self.df.columns) - 1)
        self.cursor[1] = clamp(row, 0, len(self.df.index) - 1)

    def reset_cursor(self):
        self.set_cursor()
