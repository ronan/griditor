import pandas as pd


class Data():
  num_rows: int = 0
  num_cols: int = 0

  df: pd.DataFrame = None


  def load(self, file: str) -> None:
    self.df = pd.read_csv(
        file,
        parse_dates = True,
        na_values = ['']
    )

  def shuffle() -> None:
    self.df = self.df.sample(frac=1)

  def clean(col: int):
    self.df = self.df[self.col(col).notnull()]

  def filter(query: str = "") -> None:
    self.df = self.df.loc[self.col(col).str.contains(query, case=False)]

  def sort(col: int):
    self.df = self.df.sort_values(by=self.col(col), ascending=True, na_position="first")

  def rsort(col: int):
    self.df = self.df.sort_values(by=self.col(col), ascending=False, na_position="last")

  def headers() -> list:
    return enumerate(self.df.columns)

  def slice(start: int = 0, end: int = None):
    enumerate(self.df[start:end].values.tolist())
    return 

  def col(idx: int):
    return self.df.iloc[:, idx]

  






