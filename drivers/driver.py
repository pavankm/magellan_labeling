import sys
# sys.path.append('/Users/mushahidalam/CS799/magellan_labeling')
from magellan_labeling import controller
# Intialize the possible labels
controller.set_labels()

# Test get_Summary
# print controller.get_summary()

#Test get_rows
# labels = ['no','yes']
# print controller.get_rows(labels)

# Code to check the Update_Labels
print controller.update_labels_for_tuple_pairs([['a2','b3','yes'],['a3','b2','yes']])