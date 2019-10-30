from pathlib import Path

import pandas as pd
import numpy as np
import requests

file_name = Path("rows.csv")
if not file_name.exists():
    data = requests.get(
        "https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.data"
    )
    file_name.write_bytes(data.content)

# Names based on https://archive.ics.uci.edu/ml/machine-learning-databases/adult/adult.names
df = pd.read_csv(
    file_name,
    header=None,
    index_col=False,
    names=[
        "age",
        "workclass",
        "fnlwgt",
        "education",
        "education-num",
        "marital-status",
        "occupation",
        "relationship",
        "race",
        "sex",
        "capital-gain",
        "capital-loss",
        "hours-per-week",
        "native-country",
    ],
)

# Prepare missing values
df = df.replace("\\?", np.nan, regex=True)

df.to_csv("census.csv", index=False)
