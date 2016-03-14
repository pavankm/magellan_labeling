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

def get_rows(label):
    return model.get_rows_label([label])

def update_labels(input_list):
    if len(input_list) !=3:
        print 'ERROR: Input [<ltable.id>,<rtable.id>,<label>] all 3 arguments should be string'
        return False
    if input_list[2] not in label_count_dict:
        print 'ERROR: Not a valid label'
        return False
    return model.update_labels(input_list)


set_labels()
print get_summary()
# print obj.get_rows('no')
print update_labels(['a2','b3','yes'])
