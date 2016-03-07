__author__='MushahidAlam'
import pandas as pd

class ModelClass():
    df = pd.read_csv("data/sample.csv")
    def get_label(self):
        result_dataframe=self.df.label
        label_df = pd.DataFrame(pd.Series(result_dataframe))
        return label_df

    def get_possible_label(self):
        label_coulumn= self.df.label.values
        labels=[]
        for label in label_coulumn:
            if label not in labels:
                labels.append(label)
        return labels

    def get_rows_label(self,label):
        return self.df[self.df['label'].isin(label)]