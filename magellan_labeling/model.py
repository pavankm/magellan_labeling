__author__='MushahidAlam'
import pandas as pd

df = pd.read_csv("data/sample.csv")
def get_label():
    result_dataframe=df.label
    label_df = pd.DataFrame(pd.Series(result_dataframe))
    return label_df

def get_possible_label():
    label_coulumn= df.label.values
    labels=[]
    for label in label_coulumn:
        if label not in labels:
            labels.append(label)
    return labels

def get_rows_label(label):
    return df[df['label'].isin(label)]

def update_labels(input_list):
    df_inter = df[df['ltable.ID'].isin(['a3'])]
    df_final = df_inter[df_inter['rtable.ID'].isin(['b2'])]
    index_arr = df_final.index

    print index_arr
    for i in index_arr:
        df.iloc[i]['label'] = 'test'



    # if df['ltable.ID'].str.contains(input_list[0]):
    #     if df['rtable.ID'].str.contains(input_list[1]):
    #         df[input_list[0]]
    #     else:
    #         print "ERROR: rtable.ID doesn't exist"
    #     return False
    # else:
    #     print "ERROR: ltable.ID doesn't exist"
    #     return False

print update_labels('asd')
