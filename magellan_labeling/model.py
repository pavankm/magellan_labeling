__author__='MushahidAlam'
import pandas as pd
import numpy as np

df = pd.read_csv("../magellan_labeling/data/sample.csv")
def get_label():
    result_dataframe=df.label
    label_df = pd.DataFrame(pd.Series(result_dataframe))
    return label_df

def get_possible_label():
    labels=['no','not-sure','unlabeled','yes']
    return labels

def get_rows_given_label(label):
    return df[df['label'].isin(label)]

def update_labels(input_list):
    if any(df['ltable.ID']==input_list[0]):
        if any(df['rtable.ID']==input_list[1]):
            df.loc[(df['ltable.ID']==input_list[0]) & (df['rtable.ID']==input_list[1]),'label']=input_list[2]
            df.to_csv("data/sample.csv",mode = 'w', index=False)
            return True
        else:
            print "WARNING: rtable.ID doesn't exist"
            return False
    else:
        print "WARNING: ltable.ID doesn't exist"
        return False


#Testing the code for update_labels
# input_list = ['a2','b3','new_test']
# print update_labels(input_list)

