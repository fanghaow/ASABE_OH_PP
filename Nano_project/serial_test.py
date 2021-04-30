import time
import serial
ser = serial.Serial("/dev/ttyTHS1", 9600, timeout=0)
print(ser.is_open)
while True:
    ser.write('Start:wangfanghaosb!'.encode())
    str1 = ser.readline().decode()
    if (str1 != ''):
        print(str1)
    time.sleep(0.3)
ser.close()
