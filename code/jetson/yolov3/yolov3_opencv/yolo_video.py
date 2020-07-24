import cv2
import yolo_v3_opency as yolo_v3
from collections import deque
from imutils.video import VideoStream
import numpy as np
import argparse
import imutils
import time

if __name__ == '__main__':
    pass
    size = (608, 608)
    confidence_threshold = 0.5
    nms_threshold = 0.6
    net = cv2.dnn.readNet('yolov3.weights', 'yolov3.cfg')
    with open(os.getcwd() + 'coco_classes.txt', 'r') as f:
        classes = [line.strip() for line in f.readlines()]
    layer_names = net.getLayerNames()
    outputLayers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
    vs = VideoStream(src=0).start()
    # vs = cv2.VideoCapture('ball_tracking_example.mp4')
    # allow the camera or video file to warm up
    time.sleep(3.0)
    centers = []
    Area = []
    labels = []
    while (1):
        ret, frame = vs.read()
        frame = cv2.resize(frame, size)
        Area, centers, labels = yolo_v3.yolo_v3_opencv(frame,size,confidence_threshold, nms_threhold, net, layer_names, output_layers)
        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #objA, objCX, objCY = trackGreenBall(frame)
        #print(str(objA) + ", " + str(objCX) + ", " + str(objCY))
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    # frame = vs.read()
    #while (1):
        #frame = vs.read()

    # import doctest
    # doctest.testmod()






