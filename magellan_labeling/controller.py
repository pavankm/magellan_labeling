import model
import pandas as pd
def get_summary():
    result_df=model.get_label()
    labels_list = result_df.label
    labels_count = {}
    for label in labels_list:
        if label in labels_count:
            labels_count[label]=labels_count[label]+1
        else:
            labels_count[label]=1
    df = pd.DataFrame(pd.Series(labels_count),columns=list('c'))
    return (df)

print get_summary()
