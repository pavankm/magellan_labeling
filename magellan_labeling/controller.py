from model import ModelClass
import pandas as pd

class ControllerClass():
    label_count_dict= dict()
    model = ModelClass()
    def get_summary(self):
        self.set_labels()
        result_df=self.model.get_label()
        labels_list = result_df.label
        for label in labels_list:
            self.label_count_dict[label]=self.label_count_dict[label]+1
        df = pd.DataFrame(pd.Series(self.label_count_dict),columns=list('c'))
        return (df)

    def set_labels(self):
        possible_labels = self.model.get_possible_label()
        for label in possible_labels:
            self.label_count_dict[label]=0

    def get_rows(self,label):
        return self.model.get_rows_label([label])

obj = ControllerClass()
print obj.get_summary()
print obj.get_rows('no')
