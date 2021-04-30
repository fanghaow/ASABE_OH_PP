#!user/bin/env python
import cv2
import matplotlib.pyplot as plt
import sys
import time
import os
import serial
import shutil
cap = cv2.VideoCapture(0)

path = '/home/dlinano/tensorrtx-master/yolov5/samples/'
try:
    ser = serial.Serial("/dev/ttyTHS1", 9600, timeout = 0)
except:
    ser = serial.Serial("/dev/ttyTHS2", 9600, timeout = 0)
order = 0
try:
    shutil.rmtree('/home/dlinano/tensorrtx-master/yolov5/samples')
    os.mkdir('/home/dlinano/tensorrtx-master/yolov5/samples')
except:
    pass
while(True):
    t1 = time.time()
    ret, img = cap.read()
    img = img[:,420:1500,:]
    t2 = time.time()
    str1 = ser.readline().decode()
    if (str1 == '1\r\n'):
        print(str(order) + "Save OK")
        if order >= 1:
            os.remove(path + str(order-1) + '.jpg')
            pass
        #print('img_shape: ',img.shape)
        cv2.imwrite(path + str(order)+'.jpg',img)
        order += 1
        #if ret == True:
            #cv2.imshow('standard_video',img)
            #plt.imshow(img)
            #plt.show()
            #time.sleep(0.3)
            #plt.close()
        #else:
            #print('no img took in')
        #if cv2.waitKey(1) & 0xFF == ord('q'):
            #break
        t3 = time.time()
        print(t3 - t1)
        if order >= 13:
            time.sleep(2)
            os.remove(path + str(order-1) + '.jpg')
            break 
cap.release()
