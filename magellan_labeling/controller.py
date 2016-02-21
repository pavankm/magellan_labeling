import model
def get_summary():
    result_df=model.get_label()
    labels_list = result_df.values
    labels_count = {}
    for label in labels_list:
        if label in labels_count:
            labels_count[label]=labels_count[label]+1
        else:
            labels_count[label]=1
    for label in labels_count:
        print(label,labels_count[label])


get_summary()
