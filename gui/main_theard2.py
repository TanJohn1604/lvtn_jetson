import sys
# pip install pyqt5
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from login import Ui_MainWindow
import pyrebase
import serial
import time

flag = 1

def initConnection( port, baud):
    try:
        ser = serial.Serial(port, baud)
        print("Device connected")
        return ser
    except:
        print("Errorrrrrrr")


ser = initConnection("/dev/ttyACM0", 9600)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.button.clicked.connect(self.start_serial_detect)

        self.firebaseConfig = {
            'apiKey': "AIzaSyAdQpKmaK3OMezJ42WDaZj7AKDX8pqkr1w",
            'authDomain': "lvtntd18-2023.firebaseapp.com",
            'databaseURL': "https://lvtntd18-2023-default-rtdb.firebaseio.com",
            'projectId': "lvtntd18-2023",
            'storageBucket': "lvtntd18-2023.appspot.com",
            'messagingSenderId': "510602719174",
            'appId': "1:510602719174:web:6e26243e22ef3136e38cc7",
            'measurementId': "G-XMTFKQX3QG"
        }
        self.email = "lvtn.td18@gmail.com"
        self.password = "@lvtn123456"
        self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        self.auth = self.firebase.auth()
        self.db = self.firebase.database()

        self.thread = {}

    def closeEvent(self, event):
        self.stop_serial_detect()

    def stop_serial_detect(self):
        self.thread[1].stop()

    def start_serial_detect(self):
        self.thread[1] = serial_detect(index=1)
        self.thread[1].start()
        self.thread[1].signala.connect(self.gate)
        self.uic.button.setEnabled(False)
        self.uic.trangthai.setText("Đang xữ lý")

    def gate(self, traveler):
        """Updates the image_label with a new opencv image"""
        self.uic.tenkhachhang.setText(str(traveler))
        # self.stop_serial_detect()
        self.uic.button.setEnabled(True)
        self.uic.trangthai.setText("Xữ lý xong")

class serial_detect(QThread):
    signala = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.index = index
        self.spilitdata = [0]
        print("start threading", self.index)
        super(serial_detect, self).__init__()

    def run(self):
        global flag
        global ser
        now = time.time()
        data = []
        while True:
            if flag == 0:
                self.sendData(ser, [self.spilitdata[0]], 3)
            if flag == 1:
                while ser.inWaiting() != 0:
                    data = ser.readline()
                    data = str(data, 'utf-8')
                    data = data.strip('\r\n')
                    data = data.split(",")
                    print(data)
                    flag = 0
            if data:
                if int(data[0]) != 0:

                    a = {'0': data[0], '1': data[1], '2': data[2], '3': data[3]}
                    data2 = ""
                    for i in data:
                        if int(i) < 100:
                            data2 = data2 + "0" + i
                        else:
                            data2 = data2 + i

                    b = np.ndarray((2,), buffer=np.array([int(data[0]), 2]), dtype=int)
                    self.signala.emit(b)
                    break
                    
            # if time.time() - now > 30:
            #     break
        # cap = cv2.VideoCapture(0)  # 'D:/8.Record video/My Video.mp4'
        # while True:
        #     ret, cv_img = cap.read()
        #     if ret:
        #         self.signala.emit(cv_img)

    def stop(self):
        print("stop threading", self.index)
        self.terminate()

    def sendData(self,se, data, digits):
        global flag
        myString = "$"
        for d in data:
            myString += str(d).zfill(digits)
        try:
            se.write(myString.encode())
            flag = 1
            # print(myString)
        except:
            print("send fail")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
