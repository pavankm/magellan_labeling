import sys
from PyQt4 import QtGui, QtCore

from magellan_labeling import controller
from magellan_labeling import model
class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QVBoxLayout(self)

        ########Label Selection Table##############

        label_table = QtGui.QTableWidget()
        labels = controller.get_labels()

        label_table.setColumnCount(1)
        label_table.setRowCount(len(labels))
        label_table.setVerticalHeaderLabels(labels)
        label_table.setHorizontalHeaderLabels(['labels'])

        radio_buttons = list()
        for i in range(len(labels)):
            radio = QtGui.QRadioButton(labels[i])
            radio.setChecked(1)
            label_table.setCellWidget(i, 0, radio)
            radio_buttons.append(radio)

        Button_Group = QtGui.QButtonGroup(label_table)
        for radio in radio_buttons:
            Button_Group.addButton(radio)

        #########Summary Frame#####################
        summary_table = QtGui.QTableWidget()
        summary_df = controller.get_summary()
        summary_table.setColumnCount(len(summary_df.columns))
        summary_table.setRowCount(len(summary_df.index))
        summary_table.setVerticalHeaderLabels(summary_df.index)
        summary_table.setHorizontalHeaderLabels(['count'])


        for i in range(len(summary_df.index)):
            for j in range(len(summary_df.columns)):
                summary_table.setItem(i,j,QtGui.QTableWidgetItem(str(summary_df.iget_value(i, j))))
        ###########Tuple Frame##############
        tuple_table = QtGui.QTableWidget()
        id_pairs = controller.get_all_ids_and_labels()
        temp_row = controller.get_row_tablename_and_id('A',id_pairs[0][0])

        headers = list(temp_row.columns)
        tuple_table.setColumnCount(len(id_pairs)*3)
        tuple_table.setHorizontalHeaderLabels(headers)

        tuple_table.setColumnCount(len(temp_row.columns))
        tuple_table.setRowCount(len(id_pairs)*3)

        item = None
        i=0 # Indicates the current row in the table
        k=0 # Used to index id_pair list
        while k<len(id_pairs):
            row_1 = controller.get_row_tablename_and_id('A',id_pairs[k][0])
            row_2 = controller.get_row_tablename_and_id('B',id_pairs[k][1])
            label_given = id_pairs[k][2]
            k+=1
            for j in range(len(row_1.columns)):
                item = QtGui.QTableWidgetItem(str(row_1.iget_value(0, j)))
                tuple_table.setItem(i,j,item)
            i+=1
            for j in range(len(row_2.columns)):
                item = QtGui.QTableWidgetItem(str(row_2.iget_value(0, j)))
                tuple_table.setItem(i,j,item)
            i+=1

            #Add radio for labels for the current tuple pairs
            labels = controller.get_labels()
            radio_buttons = list()
            for p in range(len(labels)):
                radio = QtGui.QRadioButton(labels[p])
                if label_given==labels[p]:
                    radio.setChecked(1)
                else:
                    radio.setChecked(0)
                tuple_table.setCellWidget(i, p, radio)
                radio_buttons.append(radio)

            Button_Group = QtGui.QButtonGroup(summary_table)
            for radio in radio_buttons:
                Button_Group.addButton(radio)

            i+=1
            # summary_table.itemClicked.connect(self.labelchanged)


        #####Splitter Added########
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(summary_table)
        splitter2.addWidget(label_table)
        splitter2.setSizes([150,500])

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(splitter2)
        splitter.addWidget(tuple_table)
        # splitter.setStretchFactor(1,0)

        splitter.setSizes([100,600])
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(0, 0, 1024, 720)
        self.setWindowTitle('QtGui.QSplitter')
        self.showMaximized()

    def labelchanged(self,item):
        print item.row()
        
def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    