__author__='MushahidAlam'
import pandas as pd
import numpy as np

df = pd.read_csv("../magellan_labeling/data/sample.csv")
def get_label():
    result_dataframe=df.label
    # print type(result_dataframe)
    label_df = pd.DataFrame(result_dataframe)
    return label_df

def get_possible_label():
    #@todo the valid labels should be in a config value.
    labels=['no','not-sure','unlabeled','yes'] # unlabeled,yes, no, not-sure
    return labels

def get_rows_for_given_label_list(label_list):
    #@todo have a contract to get columnname with labels.
    return df[df['label'].isin(label_list)]

def update_label_for_a_tuple_pair(tuple_pair):
    #@todo have a contract to get columnname with ltable.ID, rtable.ID.
    if any(df['ltable.ID']==tuple_pair[0]):
        if any(df['rtable.ID']==tuple_pair[1]):
            df.loc[(df['ltable.ID']==tuple_pair[0]) & (df['rtable.ID']==tuple_pair[1]),'label']=tuple_pair[2]
            # Update this with absolute path
            df.to_csv("data/sample.csv",mode = 'w', index=False)
            return True
        else:
            #@todo use loggers!!!!
            print "WARNING: rtable.ID doesn't exist"
            return False
    else:
        print "WARNING: ltable.ID doesn't exist"
        return False


# print get_label()
#Testing the code for update_labels
# input_list = ['a2','b3','new_test']
# print update_labels(input_list)

