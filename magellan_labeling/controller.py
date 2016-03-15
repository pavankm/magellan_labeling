import model
import pandas as pd

label_count_dict= dict()
def get_summary():
    set_labels()
    result_df=model.get_label()
    labels_list = result_df.label
    for label in labels_list:
        label_count_dict[label]=label_count_dict[label]+1
    df = pd.DataFrame(pd.Series(label_count_dict),columns=list('c'))
    return (df)

def set_labels():
    possible_labels = model.get_possible_label()
    for label in possible_labels:
        label_count_dict[label]=0

def get_rows(labels):

    for label in labels:
        if label not in label_count_dict:
            print 'WARNING: Not a valid label',label
            return False
    return model.get_rows_given_label(labels)


def update_labels(input_list):
    result = False
    for row in input_list:
        if len(row) !=3:
            print 'WARNING: Input [<ltable.id>,<rtable.id>,<label>] all 3 arguments should be string'
        if row[2] not in label_count_dict:
            print 'WARNING: Not a valid label'
        if model.update_labels(row):
            result = True
    return result

# set_labels()
# print get_summary()