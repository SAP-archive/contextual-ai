from pathlib import Path

import pandas as pd

def read_pandas(file_name: Path) -> pd.DataFrame:
    """Read DataFrame based on the file extension. This function is used when the file is in a standard format.
    Various file types are supported (.csv, .json, .jsonl, .data, .tsv, .xls, .xlsx, .xpt, .sas7bdat, .parquet)
    Args:
        file_name: the file to read
    Returns:
        DataFrame
    Notes:
        This function is based on pandas IO tools:
        https://pandas.pydata.org/pandas-docs/stable/user_guide/io.html
        https://pandas.pydata.org/pandas-docs/stable/reference/io.html
        This function is not intended to be flexible or complete. The main use case is to be able to read files without
        user input, which is currently used in the editor integration. For more advanced use cases, the user should load
        the DataFrame in code.
    """
    extension = file_name.suffix.lower()
    if extension == ".json":
        df = pd.read_json(str(file_name))
    elif extension == ".jsonl":
        df = pd.read_json(str(file_name), lines=True)
    elif extension == ".dta":
        df = pd.read_stata(str(file_name))
    elif extension == ".tsv":
        df = pd.read_csv(str(file_name), sep="\t")
    elif extension in [".xls", ".xlsx"]:
        df = pd.read_excel(str(file_name))
    elif extension in [".hdf", ".h5"]:
        df = pd.read_hdf(str(file_name))
    elif extension in [".sas7bdat", ".xpt"]:
        df = pd.read_sas(str(file_name))
    elif extension == ".parquet":
        df = pd.read_parquet(str(file_name))
    elif extension in [".pkl", ".pickle"]:
        df = pd.read_pickle(str(file_name))
    else:
        if extension != ".csv":
            print(extension)

        df = pd.read_csv(str(file_name), header=None)
    return df

path = Path("feature_names.csv")
x = read_pandas(file_name=path)
print(x)

path = Path("train_data.csv")
y = read_pandas(file_name=path)
print(y)
