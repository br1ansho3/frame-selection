import sys, os 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frame_main import frame_main
from frame_ui import *
from import_dialog import golden_widget

class grid_row(QWidget):
    def __init__(self, row, parent=None):
        super().__init__()
        self.row = str(row)
        self.frame = frame_main()
        self.initUI()
        self.setup_connection()
        self.setToolTip('Golden --> ROI --> RM')

    def initUI(self):
        self.grid_layout = QGridLayout()
        #self.grid_layout.setSpacing(20)

        if len(self.row) == 1:
            self.row = '0' + self.row
        self.row_count = QLabel(self.row)
        self.grid_layout.addWidget(self.row_count, 0, 0, 1, 1, Qt.AlignHCenter)
        self.golden_widget = golden_widget()
        self.grid_layout.addWidget(self.golden_widget, 0, 1, 1, 1, Qt.AlignHCenter)
        self.roi = QLabel('null')
        self.grid_layout.addWidget(Self.roi, 0, 2, 1, 1, Qt.AlignHCenter)
        self.rm = QLabel('null')
        self.grid_layout.addWidget(self.rm, 0, 3, 1, 1, Qt.AlignHCenter)

        self.setLayout(self.grid_layout)

        self.grid_layout.setColumnMinimumWidth(0, 12)
        self.grid_layout.setColumnMinimumWidth(1, 195)
        self.grid_layout.setColumnMinimumWidth(2, 113)
        self.grid_layout.setColumnMinimumWidth(3, 113)

    def setup_connection(self):
        self.frame.done_btn.clicked.connect(self.append_values)

    def append_values(self):
        ROI_string = self.frame.lineEdit.text()
        RM_string = self.frame.lineEdit_2.text()
        if (ROI_string and RM_string):
            self.roi.setText(ROI_string)
            self.rm.setText(RM_string)
        self.frame.hide()
    
class golden_grid_table(QWidget):
    def __init__(self, number, parent=None):
        super().__init__()
        self.number - number
        self.rows = 5
        self.mode_string = ''
        self.golden_string = ''
        self.roi_string = ''
        self.rm_string = ''

        self.initUI()
        self.setup_connections()

    def initUI(self):
        self.final_layout = QVBoxLayout()

        #frameset layout: label + combobox
        seq_layout = QHBoxLayout()
        seq_layout.addWidget(QLabel('Frameset (' + str(self.number) + '):'))
        self.seq_combo_box = QComboBox()
        self.seq_combo_box.addItem('')
        self.seq_combo_box.addItem('WAIT_GOLDEN')
        self.seq_combo_box.addItem('WAIT_NON_GOLDEN')
        self.seq_combo_box.addItem('STABLE')
        seq_layout.addWidget(self.seq_combo_box)
        spacerItem = QSpacerItem(40, 20, 
            QSizePolicy.Expanding, QSizePolicy.Minimum)
        seq_layout.addItem(spacerItem)
        self.final_layout.addLayout(seq_layout)

        #adding header row
        self.header_row = QGridLayout()
        #self.header_row.setSpacing(80)
        self.row_header = QLabel('Row')
        self.header_row.addWidget(self.row_header, 0, 0, 1, 1, Qt.AlignHCenter)
        self.golden_header = QLabel('Golden')
        self.header_row.addWidget(self.golden_header, 0, 1, 1, 1, Qt.AlignHCenter)
        self.roi_header = QLabel('ROI')
        self.header_row.addWidget(self.roi_header, 0, 2, 1, 1, Qt.AlignHCenter)
        self.rm_header = QLabel('RM')
        self.header_row.addWidget*self.rm_header, 0, 3, 1, 1, Qt.AlignHCenter)
        #self.final_layout.addLayout(self.header_row)
        self.header_row.setColumnMinimumWidth(0, 12)
        self.header_row.setColumnMinimumWidth(1, 195)
        self.header_row.setColumnMinimumWidth(2, 113)
        self.header_row.setColumnMinimumWidth(3, 113)

        #adding actual grid_tables with default of 5 row
        self.grid_layout = QGridLayout()
        for row in range(1, self.rows + 1):
            self.grid_layout.addWidget(grid_row(row), row, 0, 1, 1, Qt.AlignLeft)

        #putting grid_layout into a widget to wrap scroll area around it 
        grid_widget = QWidget()
        grid_widget.setLayout(self.grid_layout)
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        grid_widget.setBackgroundRole(QPalette.Dark)
        scroll_area.setWidget(grid_widget)
        scroll_area.setMinimunWidth(548)
        self.final_layout.addWidget(scroll_area)

        #add extra grid_row & clear buttons
        function_layout = QHBoxLayout()
        self.add_btn = QPushButton('Add Golden')
        self.reset_btn = QPushButton('Reset')
        spacerItem1 = QSpacerItem(40, 20,
            QSizePolicy.Expanding, QSizePolicy.Minimum)
        function_layout.addWidget(self.add_btn)
        function_layout.addItem(spacerItem1)
        function_layout.addWidget(self.reset_btn)
        self.final_layout.addLayout(function_layout)
        self.setLayout(self.final_layout)

    def setup_connections(self):
        self.add_btn.clicked.connect(self.add_row)
        self.reset_btn.clicked.connect(self.reset_table)

    def add_row(self):
        self.rows += 1
        self.grid_layout.addWidget(grid_row(self.rows), self.rows, 0, 1, 1, Qt.AlignLeft)

    def reset_table(self):
        children = self.findChildren(grid_row)
        count = 0 
        for row in children:
            if count < 5:
                row.golden_widget.golden_widget_label.setPixmap(QPixmap('default.png').scaled(96, 54))
                row.golden_widget.img_btn.setText('Drag Here!')
                row.golden_widget.img_btn.setEnabled(False)
                row.roi.setText('null')
                row.rm.setText('null')
            else:
                row.setParent(None)
                self.rows -= 1
            count += 1
    
    # partial cmd
    def partial_cmd(self):
        self.golden_string = ''
        self.roi_string = ''
        self.rm_string = ''
        first_golden = self.findChildren(golden_widget)[0].img_btn
        if (self.seq_combo_box.currentText() != '') and (first_golden.isEnabled()):
            self.mode_string = self.seq_combo_box.currentText() + ':'
            grid_rows = self.findChildren(grid_row)
            for row in grid_rows:
                if row.golden_widget.img_btn.isEnabled():
                    self.golden_string += row.golden_widget.img_btn.text() + ';'
                else:
                    break
                if row.roi.text() != 'null':
                    self.roi_string += row.roi.text() + ';'
                if row.rm.text() != 'null':
                    self.rm_string += row.rm.text() + ';'
        else:
            return False
        
        return [self.mode_string[:-1], self.golden_string[:-1], self.roi_string[:-1], self.rm_string[:-1]]

if __name__ == '__main__':
    app = QApplication(sys.argv)
    table = golden_grid_table(1)
    table.show()
    sys.exit(app.exec_())