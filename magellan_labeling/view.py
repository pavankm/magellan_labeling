import sys
from PyQt4 import QtGui, QtCore
import logging
from magellan_labeling import controller
#define QT_NO_USERDATA
changed_rows = list()

#TODO submit button and update button
#TODO: Event handler for both the buttons
#TODO: Global list of rows updates to be flushed

current_labels_modified = dict()
summary_table = None
tuple_table = None
label_table = None

class TupleButtons(QtGui.QPushButton):
    def __init__(self,text, tuple_pair):
        super(TupleButtons, self).__init__(text)
        self.tuple_pair = tuple_pair

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()


    def FilterLayout(self):
        global label_table

        filter_layout = QtGui.QVBoxLayout()

        label_table = QtGui.QTableWidget()
        labels = controller.get_labels()
        label_table.setColumnCount(len(labels))

        label_table.setColumnCount(1)
        label_table.setRowCount(len(labels))
        label_table.setVerticalHeaderLabels(labels)
        label_table.setHorizontalHeaderLabels(['labels'])

        for i in range(len(labels)):
            item = QtGui.QTableWidgetItem(labels[i])
            item.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                  QtCore.Qt.ItemIsEnabled)
            item.setCheckState(QtCore.Qt.Checked)

            #set the checkbox item to table
            label_table.setItem(i, 0, item)
            # label_table.cell

        #Event handles for Label Selection
        # label_table.itemClicked.connect(self.filters_update_callback)


        filter_button = QtGui.QPushButton("Update")
        filter_button.setMaximumWidth(200)
        filter_button.setMaximumHeight(200)

        filter_button.clicked.connect(self.filter_update_callback)


        filter_layout.addWidget(label_table)
        filter_layout.addWidget(filter_button)

        filter_widget = QtGui.QWidget()
        filter_widget.setLayout(filter_layout)
        return filter_widget

    def SummaryLayout(self):
        global summary_table
        summary_table = QtGui.QTableWidget()
        summary_df = controller.get_summary()
        summary_table.setColumnCount(len(summary_df.columns))
        summary_table.setRowCount(len(summary_df.index))
        summary_table.setVerticalHeaderLabels(summary_df.index)
        summary_table.setHorizontalHeaderLabels(['count'])


        for i in range(len(summary_df.index)):
            for j in range(len(summary_df.columns)):
                summary_table.setItem(i,j,QtGui.QTableWidgetItem(str(summary_df.iget_value(i, j))))

        return summary_table

    def TupleLayout(self):
        global tuple_table
        buttonLayout = QtGui.QHBoxLayout()


        tuple_table = QtGui.QTableWidget()

        buttonLayout.addWidget(tuple_table)

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
                btn = TupleButtons(labels[p], [id_pairs[k-1][0],id_pairs[k-1][1], labels[p]])
                #Set the State Based on the label

                #Checkable and Background Color
                # data =  [id_pairs[k-1][0],id_pairs[k-1][1]]
                # btn.clicked.connect(lambda: self.labelchanged([id_pairs[k-1][0],id_pairs[k-1][1], str(btn.text())]))
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

            # button_group.tuple_pair(id_pairs[k-1][0])
            button_group.buttonClicked[QtGui.QAbstractButton].connect(self.labelchanged)
            #Increment the row number in Table
            i+=1

        font = QtGui.QFont()
        font.setPixelSize(18)
        font.setBold(1)

        tuple_layout_title = QtGui.QLabel()
        tuple_layout_title.setFont(font)
        tuple_layout_title.setText("<font color=\"black\">Tuple Pairs</font>")

        submit_button = QtGui.QPushButton("Save and Continure")
        submit_button.setMaximumWidth(200)
        submit_button.setMaximumHeight(200)

        submit_button.clicked.connect(self.update_model)


        tuple_title_layout = QtGui.QHBoxLayout()
        tuple_title_layout.addWidget(tuple_layout_title)
        tuple_title_layout.addWidget(submit_button)
        # label.setText("Mushahid")

        summary_layout = QtGui.QVBoxLayout()
        summary_layout.addLayout(tuple_title_layout)
        summary_layout.addLayout(buttonLayout)

        summary_widget = QtGui.QWidget()
        summary_widget.setLayout(summary_layout)
        return summary_widget

    def initUI(self):
        global summary_table
        global tuple_table
        hbox = QtGui.QVBoxLayout(self)

        ########Label Selection Table#######
        filter_widget = self.FilterLayout()

        #########Summary Frame##############
        self.SummaryLayout()
        ###########Tuple Frame##############

        summary_widget = self.TupleLayout()

        #####Splitter Added########
        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(summary_table)
        splitter2.addWidget(filter_widget)
        splitter2.setSizes([150,500])

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(splitter2)
        splitter.addWidget(summary_widget)
        # splitter.setStretchFactor(1,0)

        splitter.setSizes([100,600])
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, 1024, 720)
        self.setWindowTitle('QtGui.QSplitter')
        self.showMaximized()

    def update_summary(self):
        global summary_table
        summary_df = controller.get_summary()
        for i in range(len(summary_df.index)):
            for j in range(len(summary_df.columns)):
                summary_table.setItem(i,j,QtGui.QTableWidgetItem(str(summary_df.iget_value(i, j))))
        summary_table.show()

    def filter_tuples(self, labels_selected):
        """:arg list of labels selected to filter
        Updates the tuple table based on the labels provided"""
        global tuple_table
        #print tuple_table
        id_pairs = controller.get_tuple_ids_given_labels(labels_selected)
        print id_pairs
        temp_row = controller.get_row_tablename_and_id('A',id_pairs[0][0])
        headers = list(temp_row.columns)
        #print headers
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
                btn = TupleButtons(labels[p], [id_pairs[k-1][0],id_pairs[k-1][1], labels[p]])
                #Set the State Based on the label

                #Checkable and Background Color
                # data =  [id_pairs[k-1][0],id_pairs[k-1][1]]
                # btn.clicked.connect(lambda: self.labelchanged([id_pairs[k-1][0],id_pairs[k-1][1], str(btn.text())]))
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

            # button_group.tuple_pair(id_pairs[k-1][0])
            button_group.buttonClicked[QtGui.QAbstractButton].connect(self.labelchanged)
            #Increment the row number in Table
            i+=1
        tuple_table.show()



    def labelchanged(self, button):
        global current_labels_modified
        key = button.tuple_pair[0]+button.tuple_pair[1]
        current_labels_modified[key] = button.tuple_pair

    def update_model(self):
        global current_labels_modified
        update_list = list()
        for key in current_labels_modified:
            update_list.append(current_labels_modified[key])
        controller.update_labels_for_tuple_pairs(update_list)
        self.update_summary()


    def filter_update_callback(self, buton):
        global label_table
        label_selected = list()
        possible_labels = controller.get_labels()
        for i in range(-1,len(possible_labels)-1):
            if label_table.item(1,i).checkState() !=0:
                label_selected.append(str(label_table.item(1,i).text()))
        self.filter_tuples(label_selected)

        # global current_labels_selected
        # if item.checkState() == QtCore.Qt.Checked:
        #     current_labels_selected.append(item.text())
        #     #print('"%s" Checked' % item.text())
        # else:
        #     current_labels_selected.remove(item.text())
        #     #print('"%s" UnChecked' % item.text())


def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    