import serial
ser = serial.Serial("/dev/ttyTHS1", 9600, timeout=1)
print(ser.is_open)
while True:
    ser.write('0'.encode())
    str1 = ser.readline().decode()
    if (str1 != ''):
        print(str1)

ser.close()
