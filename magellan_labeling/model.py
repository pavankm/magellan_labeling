import pandas as pd
import numexpr
def get_label(label):
    df = pd.read_csv("data/sample.csv")
    Result_DataFrame = pd.DataFrame()
    Result_DataFrame=df[df.label=="yes"]
    return Result_DataFrame
