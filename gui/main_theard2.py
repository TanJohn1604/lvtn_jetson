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
flag_trung_gian = 0

check_confidence_counter1 = 0
check_confidence_counter2 = 0
check_confidence = 60

class MainWindow(QMainWindow):
    global db
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.button.clicked.connect(self.trung_gian)

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
        # self.uic.button_2.clicked.connect(self.reset)

    def testfirebase(self):
        a = db.child("050047057077").get()
        print(a.val())
        if a:
            self.uic.tenkhachhang.setText(str(a.val()["name"]))
            self.uic.soluongchai.setText(str(a.val()["chai"]))
            self.uic.soluonglon.setText(str(a.val()["lon"]))

    def reset(self):
        global state
        global check_confidence_counter1
        global check_confidence_counter2
        state = 0
        check_confidence_counter1 = 0
        check_confidence_counter2 = 0

    def closeEvent(self, event):
        self.stop_serial_detect()

    def stop_serial_detect(self):
        self.thread[1].stop()

    def trung_gian(self):
        global flag_trung_gian
        if flag_trung_gian == 0:
            self.start_serial_detect()
            flag_trung_gian = 1
        self.reset()

    def start_serial_detect(self):
        self.thread[1] = serial_detect(index=1)
        self.thread[1].start()
        self.thread[1].signala.connect(self.gate)
        self.thread[1].time_left.connect(self.show_time)
        # self.uic.button.setEnabled(False)

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

        if traveler[4] == 0:
            self.uic.trangthai.setText("Mời đặt chai/lon vào")

        if traveler[4] == 1:
            self.uic.trangthai.setText("Đã nhận diện 1 chai")

        if traveler[4] == 2:
            self.uic.trangthai.setText("Đã nhận diện 1 lon")

        # self.uic.button.setEnabled(True)
        # self.uic.trangthai.setStyleSheet("color : red")
    def show_time(self,traveler2):
        # self.uic.label_5.setText(str(traveler2[0]))
        


class serial_detect(QThread):
    signala = pyqtSignal(np.ndarray)
    time_left = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.index = index
        self.spilitdata = [0,0,0]
        print("start threading", self.index)
        super(serial_detect, self).__init__()

    def run(self):
        global flag
        global ser
        global db
        global state
        global check_confidence_counter1
        global check_confidence_counter2

        data = []
        check_confidence=50

        user_name = 0
        no_lon = 0
        no_chai = 0
        rfid = ""

        timer_1 = 0
        timer_2 = 0
        timer_3 = 0
        timer_4 = 0
        timer_5 = 0


        huong_roi = 0
        flag_chot_cua = 0
        flag_roi = 0
        flag_ketthuc = 0
        flag_frame_dautien = 0
        while True:
            if flag == 0:
                self.sendData(ser, [self.spilitdata[0],self.spilitdata[1],self.spilitdata[2]], 1)
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
                        for i in data[0:4]:
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
                            print("da nhan dien duoc id")
                            b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,5]), dtype=int)
                            self.signala.emit(b)
                        else:
                            state = 0
                            b = np.ndarray((5,), buffer=np.array([state, 0, 0, 0,4]), dtype=int)
                            self.signala.emit(b)
                    else:
                        b = np.ndarray((5,), buffer=np.array([state, 0, 0, 0,4]), dtype=int)
                        self.signala.emit(b)
                else:
                    b = np.ndarray((5,), buffer=np.array([state, 0, 0, 0,4]), dtype=int)
                    self.signala.emit(b)
                self.spilitdata[0] = 0

            if state == 1 and  huong_roi == 0:
                frame, width, height = cam.CaptureRGBA(zeroCopy=1)
                detections=net.Detect(frame, width, height)
                # print("detected {:d} objects in image".format(len(detections)))
                if data and data[4]=="1":
                    if detections:
                        detections.sort(key=lambda x: x.Confidence, reverse=True)
                        if(detections[0].Confidence>0.7):
                            # if (flag_frame_dautien == 0):
                            #     flag_frame_dautien = 1
                            #     timer_3 = time.time()
                            if detections[0].ClassID == 1:
                                check_confidence_counter2 = 0
                                check_confidence_counter1 = check_confidence_counter1 + 1
                                print("check_confidence_counter1 = " + str(check_confidence_counter1))
                                if check_confidence_counter1 == check_confidence:
                                    no_chai =no_chai +1
                                    db.child(rfid).child("chai").set(no_chai)
                                    check_confidence_counter1 = 0
                                    huong_roi = 1

                                    if (flag_frame_dautien == 0):
                                        flag_frame_dautien = 1
                                        timer_3 = time.time()
                                    b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                                    self.signala.emit(b)

                            elif detections[0].ClassID == 2:
                                check_confidence_counter1 = 0
                                check_confidence_counter2 = check_confidence_counter2 + 1
                                print("check_confidence_counter2 = " + str(check_confidence_counter2))
                                if check_confidence_counter2 == check_confidence:
                                    no_lon =no_lon +1
                                    db.child(rfid).child("lon").set(no_lon)
                                    check_confidence_counter2 = 0
                                    huong_roi = 2
                                    
                                    if (flag_frame_dautien == 0):
                                        flag_frame_dautien = 1
                                        timer_3 = time.time()
                                    b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                                    self.signala.emit(b)
                            else:
                                b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                                self.signala.emit(b)
                        else:
                            check_confidence_counter2 = 0
                            check_confidence_counter1 = 0
                            b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                            self.signala.emit(b)
                    else:
                        check_confidence_counter2 = 0
                        check_confidence_counter1 = 0
                        b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                        self.signala.emit(b)   


            timer_2 = time.time()
            # c = np.ndarray((1,), buffer=np.array([int(timer_2) % 60]), dtype=int)
            # self.time_left.emit(c)
            if  (flag_chot_cua == 0) and (flag_frame_dautien == 1) and (timer_2 - timer_3 > 0.5) :
                self.spilitdata[0] = 1
                flag_chot_cua = 1
                timer_1 = time.time()

            if (timer_2 - timer_1 > 0.5) and (flag_chot_cua == 1) and (flag_roi == 0) :
                flag_roi = 1
                timer_4 = time.time()
                if huong_roi==1:
                    self.spilitdata[1] = 1
                else:
                    self.spilitdata[1] = 0
                    
            if (flag_roi == 1) and (timer_2 - timer_4 > 2)  and (flag_ketthuc == 0):
                self.spilitdata[2] = 1
                flag_ketthuc = 1
                timer_5 = time.time()

            if (timer_2 - timer_5 > 2) and flag_ketthuc == 1:
                huong_roi = 0
                flag_ketthuc = 0
                flag_roi = 0
                flag_frame_dautien = 0
                flag_chot_cua = 0
                self.spilitdata[0] = 0
                self.spilitdata[1] = 0
                self.spilitdata[2] = 0
                b = np.ndarray((5,), buffer=np.array([state, user_name, no_lon, no_chai,huong_roi]), dtype=int)
                self.signala.emit(b) 






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
