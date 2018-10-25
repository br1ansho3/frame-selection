# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frame_window(object):
    def setupUi(self, frame_window):
        frame_window.setObjectName("frame_window")
        frame_window.resize(1027, 534)
        self.widget = QtWidgets.QWidget(frame_window)
        self.widget.setGeometry(QtCore.QRect(10, 10, 271, 521))
        self.widget.setObjectName("widget")
        self.done_btn = QtWidgets.QPushButton(self.widget)
        self.done_btn.setGeometry(QtCore.QRect(10, 490, 80, 22))
        self.done_btn.setObjectName("done_btn")
        self.reset_btn = QtWidgets.QPushButton(self.widget)
        self.reset_btn.setGeometry(QtCore.QRect(100, 490, 80, 22))
        self.reset_btn.setObjectName("reset_btn")
        self.label = QtWidgets.QLabel(self.widget)
        self.label.setGeometry(QtCore.QRect(10, 10, 251, 121))
        self.label.setObjectName("label")
        self.lineEdit = QtWidgets.QLineEdit(self.widget)
        self.lineEdit.setGeometry(QtCore.QRect(10, 160, 113, 21))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(10, 210, 113, 21))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.radioButton = QtWidgets.QRadioButton(self.widget)
        self.radioButton.setGeometry(QtCore.QRect(10, 140, 85, 20))
        self.radioButton.setObjectName("radioButton")
        self.radioButton_2 = QtWidgets.QRadioButton(self.widget)
        self.radioButton_2.setGeometry(QtCore.QRect(10, 190, 85, 20))
        self.radioButton_2.setObjectName("radioButton_2")
        self.wg_label = QtWidgets.QWidget(frame_window)
        self.wg_label.setGeometry(QtCore.QRect(290, 0, 731, 531))
        self.wg_label.setObjectName("wg_label")
        self.img_frame = QtWidgets.QLabel(self.wg_label)
        self.img_frame.setGeometry(QtCore.QRect(0, 0, 731, 531))
        self.img_frame.setObjectName("img_frame")

        self.retranslateUi(frame_window)
        QtCore.QMetaObject.connectSlotsByName(frame_window)

    def retranslateUi(self, frame_window):
        _translate = QtCore.QCoreApplication.translate
        frame_window.setWindowTitle(_translate("frame_window", "Widget"))
        self.done_btn.setText(_translate("frame_window", "Done"))
        self.reset_btn.setText(_translate("frame_window", "Reset"))
        self.label.setText(_translate("frame_window", "<html><head/><body><p>Two options:</p><p>1. Click and drag mouse on image</p><p>2. Input size into lineedits</p><p><span style=\" color:#ff0000;\">* Size reduced by 1/2 *</span></p></body></html>"))
        self.radioButton.setText(_translate("frame_window", "ROI:"))
        self.radioButton_2.setText(_translate("frame_window", "RM:"))
        self.img_frame.setText(_translate("frame_window", "TextLabel"))

