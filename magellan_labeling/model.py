__author__='MushahidAlam'
import pandas as pd

def get_label(label):
    df = pd.read_csv("data/sample.csv")
    Result_DataFrame=df[df.label==label]
    # print(Result_DataFrame)
    return Result_DataFrame