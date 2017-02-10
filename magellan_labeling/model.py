__author__ = 'MushahidAlam'
import pandas as pd
import numpy as np
import logging

df_C = pd.read_csv("/home/pavan/ds_independent_study/magellan_labeling/magellan_labeling/data/sample.csv")
df_A = pd.read_csv("/home/pavan/ds_independent_study/magellan_labeling/magellan_labeling/data/table_A.csv")
df_B = pd.read_csv("/home/pavan/ds_independent_study/magellan_labeling/magellan_labeling/data/table_B.csv")


def get_label_columns():
    """
    :return: dataframe containing labels in table C
    """
    # @todo: have a contract to get columnname with labels.
    result_dataframe = df_C.label
    label_df = pd.DataFrame(result_dataframe)
    return label_df


def get_possible_label():
    """
    :return: list of possible labels
    """
    # @todo the valid labels should be in a config value.
    labels = ['Yes', 'No', 'Not-Sure', 'Unlabeled']  # unlabeled,yes, no, not-sure
    return labels


def get_rows_for_given_label_list(label_list):
    """
    :param label_list: list of labels for which rows needs to be searched
    :return: dataframe containing rows having the labels passed in arguement,empty list if none found
    """
    # @todo have a contract to get columnname with labels.
    possible_labels = get_possible_label()
    for label in label_list:
        if label not in possible_labels:
            logging.warning('Incorrect label:', label)
            label_list.remove(label)
    if len(label_list) == 0:
        return None
    else:
        return df_C[df_C['label'].isin(label_list)]


def update_label_for_a_tuple_pair(tuple_pair):
    """
    :param tuple_pair:list of 3 elements, where list[0]=ltable.ID, list[1]=rtable.ID, list[2]=label
    :return: True on Sucess, False on failure
    """
    # @todo have a contract to get columnname with ltable.ID, rtable.ID.
    possible_labels = get_possible_label()
    if tuple_pair[2] not in possible_labels:
        logging.warning('Incorrect label:', tuple[2])
        return False

    if any(df_C['ltable.ID'] == tuple_pair[0]):
        if any(df_C['rtable.ID'] == tuple_pair[1]):
            df_C.loc[(df_C['ltable.ID'] == tuple_pair[0]) & (df_C['rtable.ID'] == tuple_pair[1]), 'label'] = tuple_pair[
                2]
            try:
                df_C.to_csv("/Users/mushahidalam/CS799/magellan_labeling/magellan_labeling/data/sample.csv", mode='w',
                            index=False)
            except:
                logging.error("Update destionation file not found")
            return True
        else:
            logging.warning("rtable.ID doesn't exist")
            return False
    else:
        logging.warning("WARNING: ltable.ID doesn't exist")
        return False


def get_id_pairs_and_labels():
    """
    :return: list of lists, where each list contains id pairs and labels from table C
    """
    # @todo have a contract to get columnname with labels.
    id_pairs_df = df_C[['ltable.ID', 'rtable.ID', 'label']]
    id_pairs_label_list = list(list())
    for row in id_pairs_df.itertuples():
        id_pairs_label_list.append([row[1], row[2], row[3]])
    return id_pairs_label_list


def get_idpairs_given_labels(labels):
    """
    :param labels: list of labels
    :return: all id pairs with the given label form table C
    """
    label_list = list()
    possible_labels = get_possible_label()
    for label in labels:
        if label not in possible_labels:
            logging.warning('Incorrect label:' + label)
        else:
            label_list.append(label)

    id_pairs_df = df_C[['ltable.ID', 'rtable.ID', 'label']]
    id_pairs_label_list = list(list())
    for row in id_pairs_df.itertuples():
        if row[3] in label_list:
            id_pairs_label_list.append([row[1], row[2], row[3]])
    return id_pairs_label_list


def get_row_from_table(table, id):
    """
    :param table: type :string , table name which will be A or B or C
    :param id: type: string, id name which needs to be searched in the table
    :return:
    """
    if table == "A":
        return df_A[df_A['ID'] == id]
    if table == "B":
        return df_B[df_B['ID'] == id]

# print get_label()
# Testing the code for update_labels
# input_list = ['a2','b3','new_test']
# print update_labels(input_list)

# Test get_id_pairs
# get_id_pairs()

# Test get_row
# print get_row_from_table('A','a1')

# Test get_idpairs_given_labels
# print get_idpairs_given_labels(['asdsad'])
