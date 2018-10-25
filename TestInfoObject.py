from PyQt5.QtWidgets import *
class TestInfo(QWidget):
    def __init__(self, parent=None):
        super().__init__()

        self.initUI()
    
    def initUI(self):
        labels = [QLabel('Action:'), QLabel('Duration:'), QLabel('Test Case:'), QLabel('Score:')]

        self.action = QComboBox()
        self.action.addItems(['', 'LT_PERFORMANCE', 'CMP_IMG'])
        self.duration = QLineEdit()
        self.test_case = QLineEdit()
        self.score = QLineEdit()
        user_inputs = [self.action, self.duration, self.test_case, self.score]

        final_layout = QHBoxLayout()
        for each in range(len(labels)):
            section = QVBoxLayout()
            section.addWidget(labels[each])
            section.addWidget(user_inputs[each])
            final_layout.addLayout(section)

        self.setLayout(final_layout)
        self.show()

    def check_empty(self):
        for each in (self.action.currentText(), self.duration.text(), self.test_case.text(), self.score.text()):
            if each == '':
                msg_Box = QMessageBox()
                msg_Box.setIcon(QMessageBox.Warning)
                msg_Box.setText('Missing Parameter')
                msg_Box.exec_()
                return False
        else: 
            return True