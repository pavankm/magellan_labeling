import model
import pandas as pd

label_count_dict= dict()
def get_summary():
    # remove this
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
        label_count_dict[label] = 0

def get_rows(labels):
    for label in labels:
        if label not in label_count_dict:
            print 'WARNING: Not a valid label',label
            return False
    return model.get_rows_for_given_label_list(labels)


def update_labels_for_tuple_pairs(input_list):
    result = False
    for row in input_list:
        if len(row) !=3:
            # logging, check for length and type
            print 'WARNING: Input [<ltable.id>,<rtable.id>,<label>] all 3 arguments should be string'

        # @todo think about where the valid label checking should be done !!!
        # The reason is in get_rows we do the label checking at controller level.
        # but here only partial check can be done. ltable.ID and rtable.ID checking are done at model level.

        # To be consistent, we can do the label checking at the model level.

        # Anything that is sent to model, that the model knows about it is checked by the model.

        # Anything that is returned by the model and the controller processes them for the higher layers should be
        # checked/done at the controller level.

        if row[2] not in label_count_dict:
            print 'WARNING: Not a valid label'


        if model.update_label_for_a_tuple_pair(row):
            result = True
    return result

# set_labels()
# print get_summary()