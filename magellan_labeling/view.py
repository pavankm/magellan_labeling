import sys
from PyQt4 import QtGui, QtCore
import logging
from magellan_labeling import controller

changed_rows = list()

#TODO submit button and update button
#TODO: Event handler for both the buttons
#TODO: Global list of rows updates to be flushed

current_labels_modified = list()

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QVBoxLayout(self)

        ########Label Selection Table##############

        Labels_Layout =  QtGui.QHBoxLayout();

        label_table = QtGui.QTableWidget()
        labels = controller.get_labels()

        label_table.setColumnCount(1)
        label_table.setRowCount(len(labels))
        label_table.setVerticalHeaderLabels(labels)
        label_table.setHorizontalHeaderLabels(['labels'])

        for i in range(len(labels)):
            item = QtGui.QTableWidgetItem(labels[i])
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                  QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Unchecked)

            #set the checkbox item to table
            label_table.setItem(i, 0, item)

        #Event handles for Label Selection
        label_table.itemClicked.connect(self.handle_label_selected)

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


            buttons_list = list()
            for p in range(len(labels)):
                btn = QtGui.QPushButton(labels[p])
                #Set the State Based on the label

                #Checkable and Background Color
                btn.setCheckable(True)
                btn.setStyleSheet(QtCore.QString("QPushButton {background-color: None;} QPushButton:checked{background-color: lightblue;}"));

                if label_given==labels[p]:
                    btn.setChecked(1)
                else:
                    btn.setChecked(0)

                #Size of the button
                #TODO: Size is restricted by the cell size
                btn.setGeometry(QtCore.QRect(0, 550, 700, 800))

                #Add to the Group of exclusive buttons
                buttons_list.append(btn)

                #Set to the Cell
                tuple_table.setCellWidget(i, p, btn)


            button_group = QtGui.QButtonGroup(summary_table)
            for btn in buttons_list:
                button_group.addButton(btn)

            #TODO: Maintain a list of Changed labels in the callback function
            # QtCore.QObject.connect(button_group,QtCore.SIGNAL("buttonClicked(int)"),
		     #                button_group,QtCore.SLOT("labelchanged(int)"))
            button_group.buttonClicked[QtGui.QAbstractButton].connect(lambda: self.labelchanged([id_pairs[k-1][0],id_pairs[k-1][1], btn]))
            #Increment the row number in Table
            i+=1


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

    def labelchanged(self,modified_tuple):
        global current_labels_modified
        # text = button.text()
        current_labels_modified.append(modified_tuple)
        pass


    def handle_label_selected(self, item):
        global current_labels_selected
        if item.checkState() == QtCore.Qt.Checked:
            current_labels_selected.append(item.text())
            print('"%s" Checked' % item.text())
        else:
            current_labels_selected.remove(item.text())
            print('"%s" UnChecked' % item.text())


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    