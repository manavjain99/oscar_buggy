import cv2
from code.jetson.yolov3.yolov3_opencv.yolo_v3_opency import yolo_v3_opencv
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
    net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
    net.setPreferableTarget(cv2.dnn.DNN_TARGET_OPENCL_FP16)
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
        Area, centers, labels, x_y, w_h = yolo_v3_opencv(frame,size,classes,confidence_threshold, nms_threshold, net, layer_names, output_layers)
        print(labels)
        label = input('Enter object to select')
        while (1):
            ret, frame = vs.read()
            frame = cv2.resize(frame, size)
            Area, centers, labels, x_y, w_h = yolo_v3_opencv(frame,size,classes,confidence_threshold, nms_threshold, net, layer_names, output_layers)
            for index, object in labels:
                if object == label:
                    xy = x_y[index]
                    x, y = xy[0], xy[1]
                    wh = w_h[index]
                    w, h = wh[0], wh[1]
                    center_x, center_y = centers[index]
                    cv2.rectangle(frame,(x,y),(x+w,y+h),2)#color,2)
                    cv2.putText(frame,label,(x,y+30),font,1,(255,255,255),2)
                    cv2.putText(frame,(str(w*h/(608*608)))[:5],(x,y+70),font,1,(255,255,255),2)
                    cv2.putText(frame,str(center_x) +str(",")+ str(center_y),(center_x,center_y),font,1,(255,255,255),2)
            cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()




