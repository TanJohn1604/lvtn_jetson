# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1024, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.button = QtWidgets.QPushButton(self.centralwidget)
        self.button.setGeometry(QtCore.QRect(70, 350, 301, 121))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button.setFont(font)
        self.button.setObjectName("button")
        self.trangthai = QtWidgets.QLabel(self.centralwidget)
        self.trangthai.setGeometry(QtCore.QRect(110, 90, 221, 138))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.trangthai.setFont(font)
        self.trangthai.setLineWidth(1)
        self.trangthai.setAlignment(QtCore.Qt.AlignCenter)
        self.trangthai.setObjectName("trangthai")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(500, 50, 451, 431))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setLineWidth(1)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.tenkhachhang = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.tenkhachhang.setFont(font)
        self.tenkhachhang.setAutoFillBackground(False)
        self.tenkhachhang.setAlignment(QtCore.Qt.AlignCenter)
        self.tenkhachhang.setObjectName("tenkhachhang")
        self.gridLayout.addWidget(self.tenkhachhang, 0, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setLineWidth(1)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.soluongchai = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.soluongchai.setFont(font)
        self.soluongchai.setAutoFillBackground(False)
        self.soluongchai.setAlignment(QtCore.Qt.AlignCenter)
        self.soluongchai.setObjectName("soluongchai")
        self.gridLayout.addWidget(self.soluongchai, 1, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setLineWidth(1)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.soluonglon = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.soluonglon.setFont(font)
        self.soluonglon.setAutoFillBackground(False)
        self.soluonglon.setAlignment(QtCore.Qt.AlignCenter)
        self.soluonglon.setObjectName("soluonglon")
        self.gridLayout.addWidget(self.soluonglon, 2, 1, 1, 1)
        self.button_2 = QtWidgets.QPushButton(self.centralwidget)
        self.button_2.setGeometry(QtCore.QRect(40, 20, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_2.setFont(font)
        self.button_2.setObjectName("button_2")
        self.button_3 = QtWidgets.QPushButton(self.centralwidget)
        self.button_3.setGeometry(QtCore.QRect(230, 20, 151, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.button_3.setFont(font)
        self.button_3.setObjectName("button_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1024, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.button.setText(_translate("MainWindow", "PushButton"))
        self.trangthai.setText(_translate("MainWindow", "Xin mời quét thẻ"))
        self.label.setText(_translate("MainWindow", "Tên khách hàng"))
        self.tenkhachhang.setText(_translate("MainWindow", "TextLabel"))
        self.label_3.setText(_translate("MainWindow", "Số lượng chai"))
        self.soluongchai.setText(_translate("MainWindow", "TextLabel"))
        self.label_4.setText(_translate("MainWindow", "Số lượng lon"))
        self.soluonglon.setText(_translate("MainWindow", "TextLabel"))
        self.button_2.setText(_translate("MainWindow", "PushButton_2"))
        self.button_3.setText(_translate("MainWindow", "PushButton_3"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
