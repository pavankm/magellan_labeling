__author__='MushahidAlam'
import pandas as pd

def get_label():
    df = pd.read_csv("data/sample.csv")
    result_dataframe=df.label
    df = pd.DataFrame(pd.Series(result_dataframe))
    return df
