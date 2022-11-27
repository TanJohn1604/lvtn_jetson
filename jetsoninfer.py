import jetson.inference
import jetson.utils
import time
import cv2
import numpy as np
import serial
import time

spilitdata=[0,0,0] # khung du lieu duoc gui den
flag=1 # co dung de luan phien gui-nhan du lieu tu arduino
width=640
height=480

# load model, bat camera
cam=jetson.utils.gstCamera(width,height,'/dev/video0')
net = jetson.inference.detectNet(argv=['--model=bottle-can-90/90epoch-ssd-mobilenet.onnx', '--labels=bottle-can-90/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.7)

# cac bien cho viec xu ly framne, fps
font=cv2.FONT_HERSHEY_SIMPLEX
startTime =  time.time()
dtav = 0

def initConnection(port,baud):
    try:
        ser=serial.Serial(port,baud)
        print("Device connected")
        return ser
    except:
        print("Errorrrrrrr")
def sendData(se,data,digits):
    global flag
    myString="$"
    for d in data:
        myString+= str(d).zfill(digits)
    try:
        se.write(myString.encode())
        flag=1
        # print(myString)
    except:
        print("send fail")

ser=initConnection("/dev/ttyUSB0",9600)
while True:
    
    if flag==0:
        sendData(ser,[spilitdata[0],spilitdata[1],spilitdata[2]],3)
    if flag==1:
        while (ser.inWaiting() != 0):
            data = ser.readline()
            data = str(data, 'utf-8')
            data = data.strip('\r\n')
            spilitdata = data.split(",")
            flag=0

    # -------------------- nhan dien - START ---------------------------------------
    frame, width, height = cam.CaptureRGBA(zeroCopy=1)
    detections=net.Detect(frame, width, height,overlay='none')
    frame=jetson.utils.cudaToNumpy(frame,width,height,4)
    frame=cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)
    # -------------------- nhan dien - END -----------------------------------------

    # -------------------- xu ly cac vat duoc phat hien START ----------------------
    for detection in detections:
        # print("detected {:d} objects in image".format(detection.ClassID))
        if(detection.Confidence>0.7):
            cv2.rectangle(frame,(int(detection.Left),int(detection.Top)),(int(detection.Right),int(detection.Bottom)),(0,0,255),2)
            cv2.putText(frame, str(detection.ClassID) + " = " +  str(round(detection.Confidence, 3)) , (int(detection.Left)+10,int(detection.Top)+40), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0), 2)
            print(detection.Confidence)
    # -------------------- xu ly cac vat duoc phat hien END ------------------------
    
    # -------------------- xuat fps START ------------------------------------------
    cv2.putText(frame,str( round(net.GetNetworkFPS())),(0,30),font,1,(0,0,255),2)
    dt = time.time() - startTime
    startTime = time.time()
    dtav = 0.9 * dtav + 0.1 * dt
    fps = 1 / dtav
    cv2.putText(frame, str(round(fps, 1)) + ' fps', (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    # -------------------- xuat fps END --------------------------------------------

    # -------------------- xuat frame START -----------------------------------------------
    cv2.imshow('webCam',frame)
    cv2.moveWindow('webCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
    # -------------------- xuat frame END -----------------------------------------------
cam.release()
cv2.destroyAllWindows()