__author__='MushahidAlam'
import pandas as pd

def get_label():
    df = pd.read_csv("data/sample.csv")
    Result_DataFrame=df.label
    # print(Result_DataFrame)
    return Result_DataFrame