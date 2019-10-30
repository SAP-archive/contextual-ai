import pandas as pd

df = pd.read_csv(
    "https://raw.githubusercontent.com/berkmancenter/url-lists/master/lists/et.csv",
    parse_dates=["date_added"],
)
df.to_csv("website_inaccessibility.csv", index=False)