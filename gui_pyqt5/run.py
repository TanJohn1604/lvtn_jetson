import os
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from login_handle import LOGIN_HANDLE
from main_handle import MAIN_HANDLE
from PyQt5 import QtCore, QtGui, QtWidgets
os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"

class UI():
    def __init__(self):
        self.mainUI = QMainWindow()
        self.mainHandle = MAIN_HANDLE(self.mainUI)
        self.mainHandle.pushButton.clicked.connect(lambda: self.loadLoginForm())

        self.loginUI = QMainWindow()
        self.loginHandle = LOGIN_HANDLE(self.loginUI)
        self.loginHandle.pushButton.clicked.connect(lambda: self.loadMainForm())

        self.loginUI.show()

    def loadLoginForm(self):

        self.mainUI.hide()
        self.loginUI.show()

    def loadMainForm(self):
        a = self.loginHandle.textEdit.toPlainText()
        self.mainHandle.soluongchai.setText(a)
        self.mainHandle.soluongchai.setAlignment(Qt.AlignCenter)

        self.mainUI.show()
        self.loginUI.hide()


if __name__ == "__main__":
    app = QApplication([])
    ui=UI()
    app.exec_()