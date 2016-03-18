__author__='MushahidAlam'
import pandas as pd
import numpy as np
import logging
df = pd.read_csv("/Users/mushahidalam/CS799/magellan_labeling/magellan_labeling/data/sample.csv")
def get_label():
    result_dataframe=df.label
    label_df = pd.DataFrame(result_dataframe)
    return label_df

def get_possible_label():
    #@todo the valid labels should be in a config value.
    labels=['no','not-sure','unlabeled','yes'] # unlabeled,yes, no, not-sure
    return labels

def get_rows_for_given_label_list(label_list):
    #@todo have a contract to get columnname with labels.
    possible_labels = get_possible_label()
    for label in label_list:
        if label not in possible_labels:
            logging.warning('Incorrect label:',label)
            label_list.remove(label)
    if len(label_list) ==0:
        return None
    else:
        return df[df['label'].isin(label_list)]

def update_label_for_a_tuple_pair(tuple_pair):
    #@todo have a contract to get columnname with ltable.ID, rtable.ID.

    possible_labels = get_possible_label()
    if tuple[2] not in possible_labels:
        logging.warning('Incorrect label:',tuple[2])
        return False

    if any(df['ltable.ID']==tuple_pair[0]):
        if any(df['rtable.ID']==tuple_pair[1]):
            df.loc[(df['ltable.ID']==tuple_pair[0]) & (df['rtable.ID']==tuple_pair[1]),'label']=tuple_pair[2]
            df.to_csv("/Users/mushahidalam/CS799/magellan_labeling/magellan_labeling/data/sample.csv",mode = 'w', index=False)
            return True
        else:
            logging.warning("rtable.ID doesn't exist")
            return False
    else:
        logging.warning("WARNING: ltable.ID doesn't exist")
        return False


# print get_label()
#Testing the code for update_labels
# input_list = ['a2','b3','new_test']
# print update_labels(input_list)

