import pandas as pd

df = pd.read_csv(
    "https://www.opendisdata.nl/download/csv/01_DBC.csv", low_memory=False
)
df["JAAR"] = pd.to_datetime(df["JAAR"], format="%Y")
df.to_csv("nza.csv", index=False)