import time
from datetime import datetime

from griditor.runner import run


async def modify(data, idx):
    if idx == 3:
        raise Exception("Woah! Bad record, bub!")

    data.df.loc[idx, 'birthday'] = datetime.strptime(
        data.df.loc[idx, 'birthday'], '%m/%d/%Y').isoformat()

    time.sleep(1)


if __name__ == "__main__":
    run(fn=modify, src="../demo.csv")
