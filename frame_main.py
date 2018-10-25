import sys 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from frame_ui import *

class frame_main(QWidget, Ui_frame_window):
    def __init__(self, parent=None):
        super().__init__()
        self.scaled_width = 960
        self.scaled_height = 540

        self.setupUi(self)
        self.initUI()
        self.setup_connection()

    def initUI(self):
        #change frame geometry (because hard to do on QtCreator)
        self.wg_label.setGeometry(QRect(230, 0, 961, 541))
        self.img_frame.setGeometry(QRect(0, 0, 961, 541))

        #setup label display and event
        self.img_frame.setScaledContents(True)
        self.img_frame.installEventFilter(self)
        self.setMouseTracking(True)

        #instantiate both bands and which_band(used for flag)
        self.ROI_band = QRubberBand(QRubberBand.Rectangle, self.img_frame)
        self.RM_band = QRubberBand(QRubberBand.Rectangle, self.img_frame)
        palette = QPalette()
        palette.setBrush(QPalette.Highlight, QBrush(Qt.red))
        self.ROI_band.setPalette(palette)
        palette.setBrush(QPalette.Highlight, QBrush(Qt.blue))
        self.RM_band.setPalette(palette)
        self.which_band = self.ROI_band

    def setup_connection(self):
        #start off with ROI button checked/ set up radio --> 'switch band' connection
        self.radioButton.setChecked(True)
        self.radioButton.toggled.connect(self.switch_current_band)
        #option 2
        self.lineEdit.returnPressed.connect(self.lineEdit_to_band)
        self.lineEdit_2.returnPressed.connect(self.lineEdit_to_band)
        self.reset_btn.clicked.connect(self.reset_default)

    def reset_default(self):
        self.ROI_band.setGeometry(0, 0, 961, 541)
        self.ROI_band.show()
        self.RM_band.hide()
        self.lineEdit.setText('[0,0,1920,1080]')
        self.lineEdit_2.setText('[-1,-1,-1,-1]')

    def give_pixmap(self, pixmap):
        self.img_frame.setPixmap(pixmap)

    def lineEdit_to_band(self):
        sender = self.sender()
        value = sender.text()
        if not len(value) > 0:
            return
        
        #allows both with [] and without to work by trimming it
        value = value.strip()
        if value[0] == '[':
            value = value[1:]
        if value[len(value) - 1] == ']':
            value = value[:-1]
        value = value.split(',')

        if len(value) == 4:
            start_x = int(value[0]) / 2
            start_y = int(value[1]) / 2
            end_x = int(value[2]) / 2
            end_y = int(value[3]) / 2

            origin = QPoint(start_x, start_y)
            size = QSize(end_x - start_x, end_y - start_y)
            if sender == self.lineEdit:
                self.ROI_band.setGeometry(QRect(origin, size))
                self.ROI_band.show()
            else:
                self.RM_band.setGeometry(QRect(origin, size))
                self.RM_band.show()

            sender.setText('hi')   #fix this

        else:
            sender.setText('Invalid Input')
    
    def switch_current_band(self):
        if self.which_band != self.ROI_band:
            self.which_band = self.ROI_band
        else:
            self.which_band = self.RM_band

    def eventFilter(self, source, event):
        if source is self.img_frame:
            if event.type() == QEvent.MouseButtonPress:
                self.origin = event.pos()
            
            elif event.type() == QEvent.MouseMove:
                self.which_band.setGeometry(QRect(self.origin, event.pos()).normalized())
                self.which_band.show()

            elif event.type() == QEvent.MouseButtonRelease:
                x = event.pos().x()
                y = event.pos().y()

                #prevent out of bounds dragging
                if x > self.scaled_width:
                    x = self.scaled_width
                elif x < 0:
                    x = 0

                if y > self.scaled_height:
                    y = self.scaled_height
                elif y < 0:
                    y = 0
                self.which_band.setGeometry(QRect(self.origin, QPoint(x, y)).normalized())

                #make sure the box is at least 30x30
                x_diff = abs(x - self.origin.x())
                y_diff = abs(y - self.origin.y())
                if y_diff >= 30 and x_diff >= 30:
                    self.append_to_lineedit(self.origin, QPoint(x, y))
                else:
                    self.which_band.hide()
        
        return False
    
    def append_to_lineedit(self, origin, end):
        diff = end - origin
        if diff.x() < 0:
            x_temp = origin.x()
            origin.setX(end.x())
            end.setX(x_temp)
        if diff.y() < 0:
            y_temp = origin.y()
            origin.setY(end.y())
            end.setY(y_temp)

        band_size = '[' + str(origin.x() * 2) + ',' + str(origin.y() * 2) + ',' + \
            str(end.x() * 2) + ',' + str(end.y() * 2) + ']'
        if self.radioButton.isChecked():
            self.lineEdit.setText(band_size)
        else:
            self.lineEdit_2.setText(band_size)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    panel = frame_main('')
    panel.show()
    sys.exit(app.exec_())