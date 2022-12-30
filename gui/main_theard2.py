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
import jetson.inference
import jetson.utils


flag = 1
firebaseConfig = {
'apiKey': "AIzaSyAdQpKmaK3OMezJ42WDaZj7AKDX8pqkr1w",
'authDomain': "lvtntd18-2023.firebaseapp.com",
'databaseURL': "https://lvtntd18-2023-default-rtdb.firebaseio.com",
'projectId': "lvtntd18-2023",
'storageBucket': "lvtntd18-2023.appspot.com",
'messagingSenderId': "510602719174",
'appId': "1:510602719174:web:6e26243e22ef3136e38cc7",
'measurementId': "G-XMTFKQX3QG"
}
email = "lvtn.td18@gmail.com"
password = "@lvtn123456"
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()


def initConnection( port, baud):
    try:
        ser = serial.Serial(port, baud)
        print("Device connected")
        return ser
    except:
        print("Errorrrrrrr")

width=640
height=480
cam=jetson.utils.gstCamera(width,height,'/dev/video0')
# cam=jetson.utils.gstCamera(width,height,'0')
# net=jetson.inference.imageNet('googlenet')
# net = jetson.inference.detectNet('ssd-mobilenet-v1',threshold=0.9)
net = jetson.inference.detectNet(argv=['--model=bottle-can-90/90epoch-ssd-mobilenet.onnx', '--labels=bottle-can-90/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.5)
# net = jetson.inference.detectNet('mobilenet-v1-ssd-mp-0_675.pth',threshold=0.9)
ser = initConnection("/dev/ttyACM0", 9600)
state = 0

class MainWindow(QMainWindow):
    global db
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.button.clicked.connect(self.start_serial_detect)

        # self.firebaseConfig = {
        #     'apiKey': "AIzaSyAdQpKmaK3OMezJ42WDaZj7AKDX8pqkr1w",
        #     'authDomain': "lvtntd18-2023.firebaseapp.com",
        #     'databaseURL': "https://lvtntd18-2023-default-rtdb.firebaseio.com",
        #     'projectId': "lvtntd18-2023",
        #     'storageBucket': "lvtntd18-2023.appspot.com",
        #     'messagingSenderId': "510602719174",
        #     'appId': "1:510602719174:web:6e26243e22ef3136e38cc7",
        #     'measurementId': "G-XMTFKQX3QG"
        # }
        # self.email = "lvtn.td18@gmail.com"
        # self.password = "@lvtn123456"
        # self.firebase = pyrebase.initialize_app(self.firebaseConfig)
        # self.auth = self.firebase.auth()
        # self.db = self.firebase.database()

        self.thread = {}
        self.uic.button_2.clicked.connect(self.reset)

    def testfirebase(self):
        a = db.child("050047057077").get()
        print(a.val())
        if a:
            self.uic.tenkhachhang.setText(str(a.val()["name"]))
            self.uic.soluongchai.setText(str(a.val()["chai"]))
            self.uic.soluonglon.setText(str(a.val()["lon"]))

    def reset(self):
        global state
        state = 0

    def closeEvent(self, event):
        self.stop_serial_detect()

    def stop_serial_detect(self):
        self.thread[1].stop()

    def start_serial_detect(self):
        self.thread[1] = serial_detect(index=1)
        self.thread[1].start()
        self.thread[1].signala.connect(self.gate)
        # self.uic.button.setEnabled(False)
        self.uic.trangthai.setText("Đang xữ lý")
        self.uic.trangthai.setStyleSheet("color : blue")
    
    def gate(self, traveler):
        if traveler[1] == 0:
            self.uic.tenkhachhang.setText(" - ")
            self.uic.soluonglon.setText(" - ")
            self.uic.soluongchai.setText(" - ")
            self.uic.trangthai.setText("Mời chạm thẻ")

        else:
            self.uic.tenkhachhang.setText(str(traveler[1]))
            self.uic.soluonglon.setText(str(traveler[2]))
            self.uic.soluongchai.setText(str(traveler[3]))
        # self.uic.button.setEnabled(True)
            self.uic.trangthai.setText("Xữ lý xong")
        # if traveler
        # self.uic.trangthai.setStyleSheet("color : red")

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
        global db
        global state
        now = time.time()
        data = []
        check_confidence=50
        check_confidence_counter1=0
        check_confidence_counter2=0
        user_name = 0
        no_lon = 0
        no_chai = 0
        rfid = ""
        while True:
            if flag == 0:
                self.sendData(ser, [self.spilitdata[0]], 3)
            if flag == 1:
                while ser.inWaiting() != 0:
                    data = ser.readline()
                    data = str(data, 'utf-8')
                    data = data.strip('\r\n')
                    data = data.split(",")
                    # print(data)
                    flag = 0
            if state == 0:
                if data:
                    if data[0] != "0":
                        rfid = ""
                        for i in data:
                            if int(i) < 100:
                                rfid = rfid + "0" + i
                            else:
                                rfid = rfid + i
                        result = db.child(rfid).get()
                        if result:
                            state = 1
                            user_name = int(result.val()["name"])
                            no_lon = int(result.val()["lon"])
                            no_chai = int(result.val()["chai"])
                            b = np.ndarray((4,), buffer=np.array([state, user_name, no_lon, no_chai]), dtype=int)
                        else:
                            state = 0
                            b = np.ndarray((4,), buffer=np.array([state, 0, 0, 0]), dtype=int)
                    b = np.ndarray((4,), buffer=np.array([state, 0, 0, 0]), dtype=int)
                else:
                    b = np.ndarray((4,), buffer=np.array([state, 0, 0, 0]), dtype=int)
                self.signala.emit(b)
            if state == 1:
                frame, width, height = cam.CaptureRGBA(zeroCopy=1)
                detections=net.Detect(frame, width, height)
                # print("detected {:d} objects in image".format(len(detections)))
                if detections:
                    detections.sort(key=lambda x: x.Confidence, reverse=True)
                    if(detections[0].Confidence>0.5):
                        if detections[0].ClassID == 1:
                            check_confidence_counter2 = 0
                            check_confidence_counter1 = check_confidence_counter1 + 1
                            print("check_confidence_counter1  " + str(check_confidence_counter1))
                            if check_confidence_counter1 == 100:
                                no_chai =no_chai +1
                                db.child(rfid).child("chai").set(no_chai)
                                check_confidence_counter1 = 0
                                b = np.ndarray((4,), buffer=np.array([state, user_name, no_lon, no_chai]), dtype=int)
                                self.signala.emit(b)

                        if detections[0].ClassID == 2:
                            check_confidence_counter1 = 0
                            check_confidence_counter2 = check_confidence_counter2 + 1
                            print("check_confidence_counter2  " + str(check_confidence_counter2))
                            if check_confidence_counter2 == 100:
                                no_lon =no_lon +1
                                db.child(rfid).child("chai").set(no_lon)
                                check_confidence_counter2 = 0
                                b = np.ndarray((4,), buffer=np.array([state, user_name, no_lon, no_chai]), dtype=int)
                                self.signala.emit(b)
                    else:
                        check_confidence_counter2 = 0
                        check_confidence_counter1 = 0
                else:
                    check_confidence_counter2 = 0
                    check_confidence_counter1 = 0
                b = np.ndarray((4,), buffer=np.array([state, user_name, no_lon, no_chai]), dtype=int)
                self.signala.emit(b)
                # # dt=time.time()-timeMark
                # # fps=1/dt
                # # fpsFilter=.95*fpsFilter+.05*fps
                # # timeMark=time.time()

                # frame=jetson.utils.cudaToNumpy(frame,width,height,4)
                # frame=cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)
                # cv2.imshow('nanoCam', frame)




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
