import sys
import datetime

from PyQt4.Qt import *
import logging
from magellan_labeling import controller
#define QT_NO_USERDATA
changed_rows = list()

#TODO submit button and update button
#TODO: Event handler for both the buttons
#TODO: Global list of rows updates to be flushed

current_labels_modified = dict()
buttonLayout = None
summary_table = None
tuple_table = None
label_table = None
saved_status_label = None

class TupleButtons(QPushButton):
    def __init__(self,text, tuple_pair):
        super(TupleButtons, self).__init__(text)
        self.tuple_pair = tuple_pair

class Example(QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()


    def FilterLayout(self):
        global label_table
        # global appStyle
        filter_layout = QVBoxLayout()
        filter_layout.setContentsMargins(1,1,1,1)

        font = QFont()
        font.setPixelSize(14)
        font.setBold(1)

        filter_layout_title = QLabel()
        filter_layout_title.setFont(font)
        filter_layout_title.setText("<font color=\"black\">Show Tuple Pairs with \nLabels:</font>")
        filter_layout_title.setWordWrap(True)
        filter_layout_title.setMaximumHeight(30)

        label_table = QTableWidget()
        label_table.setMaximumHeight(140)
        label_table.setMaximumWidth(150)
        labels = controller.get_labels()
        label_table.setColumnCount(len(labels))

        label_table.setColumnCount(1)
        label_table.setRowCount(len(labels))
        label_table.verticalHeader().hide()
        label_table.horizontalHeader().hide()
        # label_table.setColumnWidth(1,500)
        # label_table.setHorizontalHeaderLabels(["Show Tuple Pairs with \nLabels:"])
        # label_table.resizeColumnToContents(0)
        label_table.setColumnWidth(0,150)
        for i in range(len(labels)):
            item = QTableWidgetItem(labels[i])

            item.setFlags(Qt.ItemIsUserCheckable |
                                  Qt.ItemIsEnabled)
            item.setCheckState(Qt.Checked)
            #set the checkbox item to table
            label_table.setItem(i, 0, item)
            # label_table.cell

        label_table.setStyleSheet(QString("QTableWidget::indicator:checked{image: url(/Users/mushahidalam/CS799/magellan_labeling/magellan_labeling/images/check3.png);}") )
        #Event handles for Label Selection
        # label_table.itemClicked.connect(self.filters_update_callback)


        filter_button = QPushButton("Update")
        filter_button.setMaximumWidth(156)
        filter_button.setMaximumHeight(30)

        filter_button.clicked.connect(self.filter_update_callback)

        filter_layout.addWidget(filter_layout_title)
        filter_layout.addWidget(label_table)
        filter_layout.addWidget(filter_button)
        filter_layout.setSpacing(10)
        filter_layout.setContentsMargins(0,0,0,0)
        filter_layout.setAlignment(Qt.AlignTop)

        filter_widget = QWidget()
        filter_widget.setLayout(filter_layout)
        filter_widget.setContentsMargins(1,1,1,1)
        filter_widget.resize(165,filter_widget.height())
        return filter_widget

    def SummaryLayout(self):
        global summary_table

        summary_layout = QVBoxLayout()
        summary_layout.setContentsMargins(1,1,1,1)

        summary_table = QTableWidget()

        font = QFont()
        font.setPixelSize(14)
        font.setBold(1)

        summary_layout_title = QLabel()
        summary_layout_title.setFont(font)
        summary_layout_title.setText("<font color=\"black\">Label Summary</font>")
        summary_layout_title.setMaximumHeight(30)
        summary_layout_title.setMaximumWidth(170)

        summary_table.setMaximumHeight(156)
        summary_table.setMaximumWidth(170)
        summary_df = controller.get_summary()
        summary_table.setColumnCount(len(summary_df.columns))
        summary_table.setRowCount(len(summary_df.index))
        summary_table.setVerticalHeaderLabels(summary_df.index)
        summary_table.setHorizontalHeaderLabels(['count'])


        for i in range(len(summary_df.index)):
            for j in range(len(summary_df.columns)):
                summary_table.setItem(i,j,QTableWidgetItem(str(summary_df.iget_value(i, j))))




        summary_layout.addWidget(summary_layout_title)
        summary_layout.addWidget(summary_table)
        summary_layout.setSpacing(0)
        summary_layout.setContentsMargins(0,0,0,0)
        summary_layout.setAlignment(Qt.AlignTop)
        # summary_layout.set(170)

        summary_widget = QWidget()
        summary_widget.setLayout(summary_layout)
        summary_widget.setContentsMargins(1,1,1,1)
        summary_widget.resize(165,summary_widget.height())
        return summary_widget

    def TupleLayout(self):
        global tuple_table
        global saved_status_label
        global buttonLayout
        buttonLayout = QHBoxLayout()
        buttonLayout.setContentsMargins(1,1,1,1)

        tuple_table = QTableWidget()

        buttonLayout.addWidget(tuple_table)

        id_pairs = controller.get_all_ids_and_labels()
        temp_row = controller.get_row_tablename_and_id('A',id_pairs[0][0])

        headers = list(temp_row.columns)
        tuple_table.setColumnCount(len(id_pairs)*3)
        tuple_table.setHorizontalHeaderLabels(headers)

        tuple_table.setColumnCount(len(temp_row.columns))
        tuple_table.setRowCount(len(id_pairs)*3)

        tuple_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        item = None
        i=0 # Indicates the current row in the table
        k=0 # Used to index id_pair list
        while k<len(id_pairs):
            row_1 = controller.get_row_tablename_and_id('A',id_pairs[k][0])
            row_2 = controller.get_row_tablename_and_id('B',id_pairs[k][1])
            label_given = id_pairs[k][2]
            k+=1
            for j in range(len(row_1.columns)):
                item = QTableWidgetItem(str(row_1.iget_value(0, j)))
                item.setBackgroundColor(QColor.fromRgb(255,254,228,255))
                item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                tuple_table.setItem(i,j,item)
            i+=1
            for j in range(len(row_2.columns)):
                item = QTableWidgetItem(str(row_2.iget_value(0, j)))
                item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                item.setBackgroundColor(QColor.fromRgb(255,254,228,255))
                tuple_table.setItem(i,j,item)
            i+=1

            #Add radio for labels for the current tuple pairs
            labels = controller.get_labels()

            buttons_list = list()
            tuple_table.setCellWidget(i, 0,None)

            for p in range(len(labels)):
                btn = TupleButtons(labels[p], [id_pairs[k-1][0],id_pairs[k-1][1], labels[p]])
                #Set the State Based on the label

                #Checkable and Background Color
                # data =  [id_pairs[k-1][0],id_pairs[k-1][1]]
                # btn.clicked.connect(lambda: self.labelchanged([id_pairs[k-1][0],id_pairs[k-1][1], str(btn.text())]))
                btn.setCheckable(True)
                btn.setStyleSheet(QString("QPushButton {background-color: rgb(240,240,240);} QPushButton:checked{background-color: rgb(200,226,200);}"));

                if label_given==labels[p]:
                    btn.setChecked(1)
                else:
                    btn.setChecked(0)

                #Size of the button
                #TODO: Size is restricted by the cell size
                btn.setGeometry(QRect(0, 550, 700, 800))

                #Add to the Group of exclusive buttons
                buttons_list.append(btn)

                #Set to the Cell
                tuple_table.setCellWidget(i, p+1, btn)


            button_group = QButtonGroup(tuple_table)
            for btn in buttons_list:
                button_group.addButton(btn)
            #TODO: Maintain a list of Changed labels in the callback function
            # QObject.connect(button_group,SIGNAL("buttonClicked(int)"),
		     #                button_group,SLOT("labelchanged(int)"))

            # button_group.tuple_pair(id_pairs[k-1][0])
            button_group.buttonClicked[QAbstractButton].connect(self.labelchanged)
            #Increment the row number in Table
            i+=1

        # tuple_table.setColumnWidth(4,150)
        tuple_table.resizeColumnToContents(4)
        # tuple_table.resizeColumnsToContents()

        font = QFont()
        font.setPixelSize(14)
        font.setBold(1)

        tuple_layout_title = QLabel()
        tuple_layout_title.setFont(font)
        tuple_layout_title.setText("<font color=\"black\">Tuple Pairs</font>")

        status_font = QFont()
        status_font.setPixelSize(14)

        saved_status_label = QLabel()
        saved_status_label.setFont(status_font)

        submit_button = QPushButton("Save and Continure")
        submit_button.setMaximumWidth(200)
        submit_button.setMaximumHeight(35)

        submit_button.clicked.connect(self.update_model)


        tuple_title_layout = QHBoxLayout()
        tuple_title_layout.setContentsMargins(1,1,1,1)
        tuple_title_layout.addWidget(tuple_layout_title)
        tuple_title_layout.addWidget(saved_status_label)
        tuple_title_layout.addWidget(submit_button)
        # label.setText("Mushahid")

        tuple_layout = QVBoxLayout()
        tuple_layout.setContentsMargins(1,1,1,1)
        tuple_layout.addLayout(tuple_title_layout)
        tuple_layout.addLayout(buttonLayout)

        tuple_widget = QWidget()
        tuple_widget.setLayout(tuple_layout)
        return tuple_widget

    def initUI(self):
        global tuple_table
        hbox = QVBoxLayout(self)
        hbox.setContentsMargins(1,1,1,1)

        ########Label Selection Table#######
        filter_widget = self.FilterLayout()

        #########Summary Frame##############
        summary_widget = self.SummaryLayout()

        ###########Tuple Frame##############

        tuple_widget = self.TupleLayout()

        #####Splitter Added########
        splitter2 = QSplitter(Qt.Vertical)
        splitter2.setStyleSheet(QString(" background-color: rgb(255,255,255);"))
        splitter2.addWidget(summary_widget)
        splitter2.addWidget(filter_widget)
        splitter2.setSizes([200,500])
        splitter2.setMaximumWidth(110)
        # splitter2.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        splitter = QSplitter(Qt.Horizontal)
        splitter.setStyleSheet(QString(" background-color: rgb(255,255,255);"))
        splitter.addWidget(splitter2)
        splitter.addWidget(tuple_widget)
        splitter.setMaximumWidth(110)

        splitter2.setContentsMargins(10,10,10,10)
        tuple_widget.setContentsMargins(1,1,1,1)
        # splitter.setStretchFactor(1,0)

        splitter.setSizes([100,600])
        hbox.addWidget(splitter)
        self.setLayout(hbox)
        QApplication.setStyle(QStyleFactory.create('Cleanlooks'))

        self.setGeometry(0, 0, 1024, 720)
        self.setWindowTitle('QSplitter')
        self.showMaximized()

    def update_summary(self):
        global summary_table
        summary_df = controller.get_summary()
        for i in range(len(summary_df.index)):
            for j in range(len(summary_df.columns)):
                summary_table.setItem(i,j,QTableWidgetItem(str(summary_df.iget_value(i, j))))
        summary_table.show()

    def filter_tuples(self, labels_selected):
        """:arg list of labels selected to filter
        Updates the tuple table based on the labels provided"""
        global tuple_table
        #print tuple_table
        global buttonLayout
        id_pairs = controller.get_tuple_ids_given_labels(labels_selected)
        if len(id_pairs)==0:
            while tuple_table.rowCount() > 0:
                tuple_table.removeRow(0)
            tuple_table.show()
            return
        temp_row = controller.get_row_tablename_and_id('A',id_pairs[0][0])

        headers = list(temp_row.columns)
        tuple_table.setColumnCount(len(id_pairs)*3)
        tuple_table.setHorizontalHeaderLabels(headers)

        tuple_table.setColumnCount(len(temp_row.columns))
        tuple_table.setRowCount(len(id_pairs)*3)

        tuple_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        item = None
        i=0 # Indicates the current row in the table
        k=0 # Used to index id_pair list
        while k<len(id_pairs):
            row_1 = controller.get_row_tablename_and_id('A',id_pairs[k][0])
            row_2 = controller.get_row_tablename_and_id('B',id_pairs[k][1])
            label_given = id_pairs[k][2]
            k+=1
            for j in range(len(row_1.columns)):
                item = QTableWidgetItem(str(row_1.iget_value(0, j)))
                item.setBackgroundColor(QColor.fromRgb(255,254,228,255))
                item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                tuple_table.setItem(i,j,item)
            i+=1
            for j in range(len(row_2.columns)):
                item = QTableWidgetItem(str(row_2.iget_value(0, j)))
                item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEnabled)
                item.setBackgroundColor(QColor.fromRgb(255,254,228,255))
                tuple_table.setItem(i,j,item)
            i+=1

            #Add radio for labels for the current tuple pairs
            labels = controller.get_labels()

            buttons_list = list()
            tuple_table.setCellWidget(i, 0,None)

            for p in range(len(labels)):
                btn = TupleButtons(labels[p], [id_pairs[k-1][0],id_pairs[k-1][1], labels[p]])
                #Set the State Based on the label

                #Checkable and Background Color
                # data =  [id_pairs[k-1][0],id_pairs[k-1][1]]
                # btn.clicked.connect(lambda: self.labelchanged([id_pairs[k-1][0],id_pairs[k-1][1], str(btn.text())]))
                btn.setCheckable(True)
                btn.setStyleSheet(QString("QPushButton {background-color: rgb(240,240,240);} QPushButton:checked{background-color: rgb(200,226,200);}"));

                if label_given==labels[p]:
                    btn.setChecked(1)
                else:
                    btn.setChecked(0)

                #Size of the button
                #TODO: Size is restricted by the cell size
                btn.setGeometry(QRect(0, 550, 700, 800))

                #Add to the Group of exclusive buttons
                buttons_list.append(btn)

                #Set to the Cell
                tuple_table.setCellWidget(i, p+1, btn)


            button_group = QButtonGroup(tuple_table)
            for btn in buttons_list:
                button_group.addButton(btn)
            #TODO: Maintain a list of Changed labels in the callback function
            # QObject.connect(button_group,SIGNAL("buttonClicked(int)"),
		     #                button_group,SLOT("labelchanged(int)"))

            # button_group.tuple_pair(id_pairs[k-1][0])
            button_group.buttonClicked[QAbstractButton].connect(self.labelchanged)
            #Increment the row number in Table
            i+=1

        # tuple_table.setColumnWidth(4,150)
        tuple_table.resizeColumnToContents(4)
        # tuple_table.resizeColumnsToContents()

        buttonLayout.addWidget(tuple_table)
        # return tuple_widget
        tuple_table.show()



    def labelchanged(self, button):
        global current_labels_modified
        key = button.tuple_pair[0]+button.tuple_pair[1]
        current_labels_modified[key] = button.tuple_pair

    def update_model(self):
        global current_labels_modified
        global saved_status_label
        update_list = list()
        for key in current_labels_modified:
            update_list.append(current_labels_modified[key])
        controller.update_labels_for_tuple_pairs(update_list)
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        saved_status_label.setText(QString("<font color=\"black\">Saved %2</font>").arg(time))
        self.update_summary()


    def filter_update_callback(self):
        global label_table
        label_selected = list()
        possible_labels = controller.get_labels()
        for i in range(-1,len(possible_labels)-1):
            if label_table.item(1,i).checkState() !=0:
                label_selected.append(str(label_table.item(1,i).text()))
        self.filter_tuples(label_selected)

        # global current_labels_selected
        # if item.checkState() == Checked:
        #     current_labels_selected.append(item.text())
        #     #print('"%s" Checked' % item.text())
        # else:
        #     current_labels_selected.remove(item.text())
        #     #print('"%s" UnChecked' % item.text())


def main():
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()    