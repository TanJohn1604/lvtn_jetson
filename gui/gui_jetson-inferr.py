import sys
# pip install pyqt5
import cv2
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from gui import Ui_MainWindow
import jetson.inference
import jetson.utils
import time

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.uic = Ui_MainWindow()
        self.uic.setupUi(self)

        self.uic.Button_start.clicked.connect(self.start_capture_video)
        self.uic.Button_stop.clicked.connect(self.stop_capture_video)

        self.thread = {}

    def closeEvent(self, event):
        self.stop_capture_video()

    def stop_capture_video(self):
        self.thread[1].stop()

    def start_capture_video(self):
        self.thread[1] = capture_video(index=1)
        self.thread[1].start()
        self.thread[1].signal.connect(self.show_wedcam)

    def show_wedcam(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.uic.label.setPixmap(qt_img)

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(800, 600, Qt.KeepAspectRatio)
        return QPixmap.fromImage(p)


class capture_video(QThread):
    signal = pyqtSignal(np.ndarray)

    def __init__(self, index):
        self.index = index
        print("start threading", self.index)
        super(capture_video, self).__init__()

    def run(self):
        startTime = time.time()
        dtav=0
        # cap = cv2.VideoCapture(0)  # 'D:/8.Record video/My Video.mp4'
        while True:
            frame, width, height = cam.CaptureRGBA(zeroCopy=1)
            detections=net.Detect(frame, width, height)

            print("detected {:d} objects in image".format(len(detections)))

            for detection in detections:
                print(detection)

            # dt=time.time()-timeMark
            # fps=1/dt
            # fpsFilter=.95*fpsFilter+.05*fps
            # timeMark=time.time()

            frame=jetson.utils.cudaToNumpy(frame,width,height,4)
            frame=cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)

            cv2.putText(frame,str( round(net.GetNetworkFPS())),(0,30),font,1,(0,0,255),2)

            dt = time.time() - startTime
            startTime = time.time()
            dtav = 0.9 * dtav + 0.1 * dt
            fps = 1 / dtav
            cv2.putText(frame, str(round(fps, 1)) + ' fps', (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            # ret, cv_img = cap.read()
            # if ret:
            self.signal.emit(frame)

    def stop(self):
        print("stop threading", self.index)
        self.terminate()
        # self.wait()
        # self.exit()
        # self.quit()



if __name__ == "__main__":

    width=640
    height=480
    cam=jetson.utils.gstCamera(width,height,'/dev/video0')
    # cam=jetson.utils.gstCamera(width,height,'0')
    # net=jetson.inference.imageNet('googlenet')
    # net = jetson.inference.detectNet('ssd-mobilenet-v1',threshold=0.9)
    net = jetson.inference.detectNet(argv=['--model=bottle-can-90/90epoch-ssd-mobilenet.onnx', '--labels=bottle-can-90/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.5)
    # net = jetson.inference.detectNet('mobilenet-v1-ssd-mp-0_675.pth',threshold=0.9)
    timeMark=time.time()
    fpsFilter=0
    timeMark=time.time()
    font=cv2.FONT_HERSHEY_SIMPLEX
    startTime =  time.time()
    dtav = 0

    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec())
    
