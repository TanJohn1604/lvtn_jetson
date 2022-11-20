import jetson.inference
import jetson.utils
import time
import cv2
import numpy as np
width=640
height=480
cam=jetson.utils.gstCamera(width,height,'/dev/video0')
net = jetson.inference.detectNet(argv=['--model=bottle-can-90/90epoch-ssd-mobilenet.onnx', '--labels=bottle-can-90/labels.txt', '--input-blob=input_0', '--output-cvg=scores', '--output-bbox=boxes'], threshold=0.6)
timeMark=time.time()
fpsFilter=0
timeMark=time.time()
font=cv2.FONT_HERSHEY_SIMPLEX
startTime =  time.time()
dtav = 0
while True:
    frame, width, height = cam.CaptureRGBA(zeroCopy=1)
    detections=net.Detect(frame, width, height)

    print("detected {:d} objects in image".format(len(detections)))

    for detection in detections:
        print(detection)

    frame=jetson.utils.cudaToNumpy(frame,width,height,4)
    frame=cv2.cvtColor(frame, cv2.COLOR_RGBA2BGR).astype(np.uint8)

    cv2.putText(frame,str( round(net.GetNetworkFPS())),(0,30),font,1,(0,0,255),2)

    dt = time.time() - startTime
    startTime = time.time()
    dtav = 0.9 * dtav + 0.1 * dt
    fps = 1 / dtav
    cv2.putText(frame, str(round(fps, 1)) + ' fps', (450, 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('webCam',frame)
    cv2.moveWindow('webCam',0,0)
    if cv2.waitKey(1)==ord('q'):
        break
cam.release()
cv2.destroyAllWindows()