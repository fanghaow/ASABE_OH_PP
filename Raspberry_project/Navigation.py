import RPi.GPIO as GPIO
import time
import cv2
import sys
import serial
import numpy as np
import shutil
import os

class Navi():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(15, GPIO.IN) # Infrared sensor
        GPIO.setup(16, GPIO.OUT)
        GPIO.setup(20, GPIO.OUT) # Motor
        GPIO.setup(21, GPIO.OUT)
        GPIO.setup(12, GPIO.OUT) # Servo for Turning
        GPIO.setup(26, GPIO.OUT) # Servo for Camera
        GPIO.setup(24, GPIO.OUT)
        self.pwm = GPIO.PWM(12, 50)
        self.pwm.start(8)
        self.pwm2 = GPIO.PWM(26, 50)
        self.pwm2.start(8)

    def GoAhead(self, step, delay=1e-4):
        for i in range(step):
            GPIO.output(20, GPIO.HIGH)
            time.sleep(delay)
            GPIO.output(20, GPIO.LOW)
            time.sleep(delay)

    def Turn(self, angle):
        self.pwm.ChangeDutyCycle(angle / 18. + 3)
        time.sleep(0.3)

    def Localize_Cam(self, angle=100):
        self.pwm2.ChangeDutyCycle(angle / 18. + 3)
        time.sleep(0.3)

def main():
    nav = Navi()
    for i in range(99):
        nav.Localize_Cam(angle=100-i)
        print('I am here', i)
    # for i in range(12):
    #     nav.GoAhead(100)
    #     if (GPIO.input(15) == 0): # Infrared sensor changed!!
    #         print('Detect No.'+str(i)+' plant!!!')
    #         time.sleep(3000)
    #         nav.GoAhead(2000)

    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    main()
