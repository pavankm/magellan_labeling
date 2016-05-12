import model
import pandas as pd
import logging
def get_summary():
    """
    :return: dataframe with indexs as label names and corresponing count of each of the labels in the tabelC
    """
    label_count_dict= dict()
    possible_labels = model.get_possible_label()
    for label in possible_labels:
        label_count_dict[label] = 0
    result_df=model.get_label()
    labels_list = result_df.label
    for label in labels_list:
        label_count_dict[label]=label_count_dict[label]+1
    df = pd.DataFrame(pd.Series(label_count_dict),columns=list('c'))
    return (df)

def get_rows(labels):
    """
    :param labels:<list> of labels
    :return: rows with given label in table C
    """
    return model.get_rows_for_given_label_list(labels)

def get_labels():
    """:return <list> of all possible """
    return model.get_possible_label()

def get_all_ids_and_labels():
    """:return <list> of lists all id pairs form tableC"""
    return model.get_id_pairs_and_labels()


def update_labels_for_tuple_pairs(input_list):
    """:arg <list> of lists of tuple pairs with labels"""
    result = False
    for row in input_list:
        if len(row) !=3:
            # logging, check for length and type
            logging.warning('Format [<ltable.id>,<rtable.id>,<label>]',row)
        if type(row[0]) != str or type(row[1]) != str or type(row[0]) != str:
            logging.warning('Input type of id and lable should be string',row)

        # @todo think about where the valid label checking should be done !!!
        # The reason is in get_rows we do the label checking at controller level.
        # but here only partial check can be done. ltable.ID and rtable.ID checking are done at model level.

        # To be consistent, we can do the label checking at the model level.

        # Anything that is sent to model, that the model knows about it is checked by the model.

        # Anything that is returned by the model and the controller processes them for the higher layers should be
        # checked/done at the controller level.

        if model.update_label_for_a_tuple_pair(row):
            result = True
    return result

def get_tuple_ids_given_labels(labels):
    """:arg <list> of labels"""
    return model.get_idpairs_given_labels(labels)

def get_row_tablename_and_id(table,id):
    return model.get_row_from_table(table,id)

# set_labels()
# print get_summary()

#test id_pairs
# print get_all_ids()