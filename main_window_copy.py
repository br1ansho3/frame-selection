import sys, os, shutil
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from main_window_ui_copy import *
from golden_grid_table_main import *
from TestInfoObject import *
from import_dialog import import_dialog, frame_label

class main_window(QMainWindow, Ui_main_window):
    def __init__(self, parent=None):
        super().__init__()
        self.table = 1

        self.setupUI(self)
        self.initUI()
        self.setup_connection()
        self.import_btn.clicked.connect(self.import_frames)

    def initUI(self):
        #fill in central widget
        self.central_widget = QWidget()
        self.central_layout = QVBoxLayout()

        #project info 
        self.project_bar = TestInfo()
        self.central_layout.addWidget(self.project_bar)

        #grid_tables wrapped in a scroll area
        self.grid_table_widget = QWidget()
        self.grid_table_layout = QHBoxLayout()
        grid_table = golden_grid_table(self.table)
        self.grid_table_layout.addWidget(grid_table)
        self.grid_table_widget.setLayout(self.grid_table_layout)
        self.table_scroll_area = QScrollArea()
        self.table_scroll_area.setWidgetResizable(True)
        self.table_scroll_area.setWidget(self.grid_table_widget)
        self.central_layout.addWidget(self.table_scroll_area)

        #save & create functions
        self.btn_layout = QHBoxLayout()
        self.save_btn = QPushButton('Save')
        self.create_btn = QPushButton('Create')
        self.btn_layout.addWidget(self.save_btn)
        self.btn_layout.addWidget(self.create_btn)
        self.central_layout.addLayout(self.btn_layout)
        self.central_widget.setLayout(self.central_layout)

        self.setCentralWidget(self.central_widget)

        #add tool buttons [+] & [-]
        self.add_toolbutton = QToolButton()
        self.add_toolbutton.setIcon(QIcon('add-icon.png'))
        self.add_toolbutton.setToopTip('Add Frameset')
        self.main_tool_bar.addWidget(self.add_toolbutton)
        self.remove_toolbutton = QToolButton()
        self.remove_toolbutton.setIcon(QIcon('remove-icon.png'))
        self.remove_toolbutton.setToolTip('Remove Frameset')
        self.main_tool_bar.addWidget(self.remove_toolbutton)

        #setup dock widget with btn and default label
        self.import_btn = QPushButton('import')
        self.import_btn.resize(50, 20)
        self.import_btn.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.dock_layout = QHBoxLayout()
        self.dock_layout.setContentsMargins(10, 10, 0, 10)
        self.dock_layout.addWidget(self.import_btn)

        default_pixmap = QPixmap('default.png')
        label = frame_label(default_pixmap, 'default.png')
        label.setToolTip('Drag this to clear row')
        self.dock_layout.addWidget(label)
        label.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.frames_widget.setLayout(self.dock_layout)
    
    def setup_connection(self):
        self.add_toolbutton.clicked.connect(self.add_table)
        self.remove_toolbutton.clicked.connect(self.remove_table)
        self.create_btn.clicked.connect(self.display_cmd)
        self.save_btn.clicked.connect(self.save_to_folder)
    
    def save_to_folder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Save to Folder', '', QFileDialog.ShowDirsOnly)
        folder = folder.replace('\\', '\\\\')
        used_goldens = self.findChildren(golden_widget)
        for golden in used_goldens:
            if golden.img_btn.isEnabled():
                shutil.copy(golden.full_path, folder)
            else:
                break

    def import_frames(self):
        dialog = import_dialog()
        if dialog.exec_():
            self.path = dialog.path
            image_files = os.listdir(self.path)

            for image_file in image_files:
                path = self.path + '\\\\' + image_file
                if os.path.isfile(path):
                    pixmap = QPixmap(path)
                    label = frame_label(pixmap, image_file)
                    self.dock_layout.addWidget(label)

    def add_table(self):
        self.table += 1
        self.grid_table_layout.addWidget(golden_grid_table(self.table))

    def remove_table(self):
        self.table -= 1
        tables = self.findChildren(golden_grid_table)
        if len(tables) > 1:
            tables[len(tables) - 1].setParent(None)
    
    def make_cmd(self):
        mode = ''
        golden = ''
        roi = ''
        rm = ''
        grid_tables = self.findChildren(golden_grid_table)
        for grid_table in grid_tables:
            if(grid_table.partial_cmd()):
                mode += grid_table.partial_cmd()[0] + ':'
                golden += grid_table.partial_cmd()[1] + ':'
                roi += grid_table.partial_cmd()[2] + ':'
                rm += grid_table.partial_cmd()[3] + ':'
            else:
                return
        
        return 'VideoCmp<{}><{}><{}><{}><{}><{}><{}>'.format(
            self.project_bar.action.currentText(),
            self.project_bar.duration.text(),
            self.project_bar.text_case.text(),
            mode[:-1],
            golden[:-1]
            self.project_bar.score.text(),
            roi[:-1],
            rm[:-1]
        )
    
    def display_cmd(self):
        flag = self.project_bar.check_empty()
        msg_Box = QMessageBox()

        if flag:
            cmd = self.make_cmd()
            if cmd:
                msg_Box.setIcon(QMessageBox.Information)
                copy_btn = msg_Box.addButton('Copy', QMessageBox.ActionRole)
                msg_Box.addButton('Ok', QMessageBox.AcceptRole)
                msg_Box.setText(cmd)
                msg_Box.exec_()
            
            if msg_Box.clickedButton() == copy_btn:
                message = QMessageBox()
                message.setIcon(QMessageBox.Information)
                message.setText('Copied!')
                message.exec_()
                QGuiApplication.clipboard().setText(cmd)
        else:
            msg_Box.setIcon(QMessageBox.Warning)
            msg_Box.setText('One or more frameset has no frames')
            msg_Box.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = main_window()
    panel.show()
    sys.exit(app.exec_())