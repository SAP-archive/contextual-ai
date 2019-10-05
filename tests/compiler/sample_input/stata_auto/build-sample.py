import pandas as pd

df = pd.read_stata(
    "http://www.stata-press.com/data/r15/auto2.dta"
)
df.to_stata("auto.dta")