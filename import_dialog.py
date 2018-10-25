from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import os, sys
from frame_main import frame_main

class import_dialog(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.setup_connection()
        self.path = ''

    def initUI(self):
        final_layout = QVBoxLayout()
        self.setLayout(final_layout)

        #first layer
        path_layout = QHBoxLayout()
        path_layout.addWidget(QLabel('Import Path:'))
        self.lineedit = QLineEdit()
        self.lineedit.setPlaceholderText('Please type absolute path...')
        path_layout.addWidget(self.lineedit)
        self.folder_search_btn = QToolButton()
        self.folder_search_btn.setIcon(QIcon('folder_search.png'))
        path_layout.addWidget(self.folder_search_btn)
        final_layout.addLayout(path_layout)

        #second layer
        btn_layout = QHBoxLayout()
        self.ok = QPushButton('Ok')
        self.cancel = QPushButton('Cancel')
        btn_layout.addWidget(self.ok)
        btn_layout.addWidget(self.cancel)
        final_layout.addLayout(btn_layout)

    def setup_connection(self):
        self.ok.clicked.connect(self.ok_clicked)
        self.cancel.clicked.connect(self.reject)
        self.folder_search_btn.clicked.connect(self.folder_search)

    def folder_search(self):
        path = QFileDialog.getExistingDirectory(self, 'Import Directory', '', QFileDialog.ShowDirsOnly)
        self.lineedit.setText(path)

    def ok_clicked(self):
        has_path = os.path.isabs(self.lineedit.text())
        if has_path:
            self.path = self.lineedit.text()
            self.path.replace('\\', '\\\\')
            self.accept()
        else:
            message = QMessageBox()
            message.setIcon(QMessageBox.Warning)
            message.setText('Directory not found, please try again!')
            message.exec_()

class frame_label(QLabel):
    def __init__(self, pixmap, file_name, parent=None):
        super().__init__()
        self.pixmap = pixmap 
        self.file_name = file_name

        self.initUI()

    def initUI(self):
        self.setScaledContents(True)
        self.setPixmap(self.pixmap.scaled(96, 54))

    def mouseMoveEvent(self, event):
        if event.buttons() != Qt.LeftButton:
            return
        
        #create drag object with path info
        mimeData = QMimeData()
        mimeData.setText(self.file_name)
        mimeData.setImageData(QPixmap(self.pixmap))
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setPixmap(self.pixmap.scaled(96, 54))
        drag.setHotSpot(QPoint(drag.pixmap().width/2, drag.pixmap().height()))
        drag.exec_(Qt.CopyAction)

class golden_widget(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.initUI()
        self.setup_connection()

    def initUI(self):
        self.setAcceptDrops(True)
        self.golden_widget_layout = QHBoxLayout()
        self.golden_widget_label = QLabel()
        self.golden_widget_label.setPixmap(QPixmap('default.png').scaled(96, 54))
        self.golden_widget_layout.addWidget(self.golden_widget_label)
        self.img_btn = QPushButton()
        self.img_btn.setEnabled(False)
        self.img_btn.setText('Drag Here!')
        self.golden_widget_layout.addWidget(self.img_btn)
        self.setLayout(self.golden_widget_layout)

    def setup_connection(self):
        self.img_btn.clicked.connect(lambda: self.parentWidget().frame.show())

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        pixmap = event.mimeData().imageData()
        file_name = event.mimeData().text()
        self.img_btn.setText(file_name.split('.')[0]) #this gets the file name without the .xxx

        parent_grid_row = self.parentWidget() #this is the grid_row self is in
        parent_grid_row.frame.give_pixmap(pixmap)
        self.golden_widget_label.setPixmap(pixmap.scaled(96, 54))
        #when dropped in self, roi & rm go to default
        if file_name.split('.')[0] == 'default':
            self.img_btn.setEnabled(False)
            parent_grid_row.roi.setText('null')
            parent_grid_row.rm.setText('null')
        else:
            self.img_btn.setEnabled(True)
            parent_grid_row.roi.setText('[0,0,1920,1080]')
            parent_grid_row.rm.setText('[-1,-1,-1,-1]')
            parent_grid_row.frame.reset_default()
        