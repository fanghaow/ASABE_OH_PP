import RPi.GPIO as GPIO
import time
import cv2
import sys
import serial
import numpy as np
import shutil
import os

f = open('yours.txt', 'w')
f.close()
os.remove('yours.txt')
f = open('yours.txt', 'w')
f.close()

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(15, GPIO.IN)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
GPIO.setup(24, GPIO.OUT)

def GoAhead(step):
    for i in range(step):
        #pwm1 = GPIO.PWM(20, 100000)
        #pwm1.start(50)
        GPIO.output(20, GPIO.HIGH)
        #GPIO.output(26, GPIO.HIGH)
        time.sleep(0.0001)
        #GPIO.output(26, GPIO.LOW)
        #time.sleep(0.00005)
        #GPIO.output(26, GPIO.HIGH)
        GPIO.output(20, GPIO.LOW)
        #time.sleep(0.0002)
        #GPIO.output(26, GPIO.LOW)
        time.sleep(0.0001)
        #time.sleep(0.00001)
        #pwm1.stop()

#cap = cv2.VideoCapture(0)
#cap.set(3, 1920)
#cap.set(4, 1080)
#ret, img = cap.read()
#Port = "/dev/ttyUSB0"
#Port1 = "/dev/ttyUSB1"
#baudRate = 9600

angle = 150
pwm = GPIO.PWM(12, 50)
pwm.start(8)
pwm.ChangeDutyCycle(angle / 18. + 3)
time.sleep(0.3)
angle2 = 100
pwm2 = GPIO.PWM(26, 50)
pwm2.start(8)
pwm2.ChangeDutyCycle(angle2 / 18. + 3)
time.sleep(0.3)
#pwm.stop()

#try:
    #ser = serial.Serial(Port, baudRate, timeout = 0)
#except:
    #ser = serial.Serial(Port1, baudRate, timeout = 0)

order = 0

while True:
    GoAhead(100)
    #str1 = ''
    #str1 = ser.readline().decode()
    if (GPIO.input(15) == 0):
        #ret, img = cap.read()
        #img = img[:,460:1460,:]
        #img = cv2.subtract(img, np.ones(img.shape, dtype = np.uint8)* 20)
        #cv2.imwrite('/home/pi/Desktop/standard_photos' + '/' + str(order) + '.jpg', img)
        f = open('yours.txt', 'w')
        f.write(str(order))
        f.close()
        print('Save OK')
        #client('/home/pi/Desktop' + '/' + str(order) + '.jpg')
        GoAhead(2000)
        order += 1
        if order > 11:
            break


GPIO.cleanup()
sys.exit(0)
