import dask.dataframe as daskd
import pandas as pd
try:

    path = "/scratch/michaesb/20201025-17-57-supermag.csv"
    pd.read_csv(path)

    df = daskd.read_csv(
    "voters.csv",
    blocksize= 16 * 1024 * 1024, # 16MB chunks
)

except FileNotFoundError:
    path = "/run/media/michaelsb/HDD Linux/data/20201025-17-57-supermag.csv"
    pd.read_csv(path)
    df = daskd.read_csv(
    "voters.csv",
    blocksize= 16 * 1024 * 1024, # 16MB chunks
)
