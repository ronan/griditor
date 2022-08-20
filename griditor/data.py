import pandas as pd


class Data:
    df: pd.DataFrame = None
    df_0: pd.DataFrame = None

    def load(self, file: str) -> None:
        self.df_0 = self.df = pd.read_csv(file, parse_dates=True, na_values=[""])

    def restore(self) -> None:
        self.df = self.df_0.copy()

    def shuffle(self) -> None:
        self.df = self.df.sample(frac=1)

    def clean(self, col: int):
        self.df = self.df.loc[self.col(col).notnull()]

    def filter(self, col: int, query: str = "") -> None:
        self.df = self.df.loc[self.col(col).str.contains(query, case=False)]

    def sort(self, col: int):
        self.df = self.df.sort_values(by=self.col(col).name, ascending=True, na_position="first")

    def rsort(self, col: int):
        self.df = self.df.sort_values(by=self.col_at(col), ascending=False, na_position="last")

    def col_at(self, idx: int) -> str:
        return self.df.columns[idx]

    def headers(self) -> list:
        return enumerate(self.df.columns)

    def slice(self, start: int = 0, end: int = None):
        return enumerate(self.df[start:end].values.tolist())

    def col(self, idx: int):
        return self.df.iloc[:, idx]