#For Raspi
import time
import cv2
import socket
import sys
import os
import serial
import struct
import RPi.GPIO as GPIO
import math
import numpy as np

# define host ip: Rpi's IP
HOST_IP_con = "192.168.43.44"  # unneeded
HOST_PORT_con = 8899
# 1.create socket object:socket=socket.socket(family,type)
datalst = []
result_lst = []

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(16, GPIO.IN)
GPIO.setup(20, GPIO.OUT)
GPIO.output(20, 0)

cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)
Port = "/dev/ttyUSB0"
Port1 = "/dev/ttyUSB1"
baudRate = 9600

try:
    ser = serial.Serial(Port, baudRate, timeout=0)
except:
    ser = serial.Serial(Port1, baudRate, timeout=0)


def socket_service():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # IP地址留空默认是本机IP地址
        s.bind(('', 8000))
        s.listen(7)
    except socket.error as msg:
        print(msg)
        sys.exit(1)

    print("连接开启，等待传图...")

    while True:
        sock, addr = s.accept()
        deal_data(sock, addr)
        break  # 我加的

    s.close()


def deal_data(sock, addr):
    print("成功连接上 {0}".format(addr))

    while True:
        fileinfo_size = struct.calcsize('128sl')
        buf = sock.recv(fileinfo_size)
        if buf:
            filename, filesize = struct.unpack('128sl', buf)
            fn = filename.decode().strip('\x00')
            # PC端图片保存路径
            new_filename = os.path.join('/home/pi/Desktop/Results', fn)

            recvd_size = 0
            fp = open(new_filename, 'wb')

            while not recvd_size == filesize:
                if filesize - recvd_size > 1024:
                    data = sock.recv(1024)
                    recvd_size += len(data)
                else:
                    data = sock.recv(1024)
                    recvd_size = filesize
                fp.write(data)
            fp.close()
        sock.close()
        break


def client(path):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 192.168.199.1和8088分别为服务端（pc）的IP地址和网络端口
        s.connect(('192.168.43.122', 8088))
    except socket.error as msg:
        print(msg)
        print(sys.exit(1))
    while True:
        filepath = path
        fhead = struct.pack(b'128sl', bytes(os.path.basename(filepath), encoding='utf-8'), os.stat(filepath).st_size)
        s.send(fhead)
        print('client filepath: {0}'.format(filepath))
        fp = open(filepath, 'rb')
        while True:
            try:
                data = fp.read(1024)
                if not data:
                    print('{0} 发送成功...'.format(filepath))
                    break
                s.send(data)
            except:
                continue
        break


def transform():
    global datalst
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP server listen @ %s:%d!" % (HOST_IP_con, HOST_PORT_con))
    host_addr = ('', HOST_PORT_con)
    # 2.bind socket to addr:socket.bind(address)
    socket_tcp.bind(host_addr)
    # 3.listen connection request:socket.listen(backlog)
    socket_tcp.listen(16)
    # 4.waite for client:connection,address=socket.accept()
    socket_con, (client_ip, client_port) = socket_tcp.accept()
    print("Connection accepted from %s." % client_ip)
    socket_con.send("Welcome to COM TCP server!".encode())
    # 5.handle
    print("Receiving package...")
    i = 1
    while True:
        try:
            data = socket_con.recv(512)
            if len(data) > 0:
                data = data.decode()
                print("Received:%s" % data)
                datalst = eval(data)
                # if str(data)[2]=='1':
                #     print('Great!')
                # elif str(data)[2]=='0':
                #     print('No!')
                socket_con.send(data)
                # time.sleep(1)
                i += 1
                if (i > 1):
                    socket_tcp.close()
                    break
                continue
        except Exception:
            socket_tcp.close()
            break
    socket_tcp.close()


def transita_service():
    global result_lst
    global HOST_PORT_con
    global datalst
    transform()
    print(datalst)
    lsita = []
    i = 0
    while i < len(datalst):
        ilst = datalst[i]
        xi = (ilst[0] + ilst[2]) / 2
        yi = (ilst[1] + ilst[3]) / 2
        length = math.sqrt((xi - 500) ** 2 + (yi - 540) ** 2)
        sita = int(math.acos((yi - 540) * (1) / length) / 3.14159 * 180)
        if xi > 500:
            sita = 360 - sita
        print(sita)
        lsita.append(sita)
        i += 1
        if 'flower' in datalst[i]:
            lsita.append('b')
        elif 'white' in datalst[i]:
            lsita.append('a')
        i += 1
    targetnum = int(len(lsita) / 2)
    result_lst = []
    result_lst.append(targetnum)
    for j in range(len(lsita)):
        result_lst.append(lsita[j])
    print(result_lst)
    datalst = []
    HOST_PORT_con += 1


order = 0
flag = 0

while True:
    str1 = ''
    try:
        str1 = ser.readline().decode()
    except:
        str1 = ''
    if ('1' in str1):
        print(str1)
        break
while True:
    str1 = ''
    str1 = ser.readline().decode()
    ret, img = cap.read()
    img = img[:, 460:1460, :]
    img = cv2.subtract(img, np.ones(img.shape, dtype=np.uint8) * 20)
    if ('1' in str1):
        print(str1)
        cv2.imwrite('/home/pi/Desktop' + '/' + str(order) + '.jpg', img)
        print('Save OK')
        client('/home/pi/Desktop' + '/' + str(order) + '.jpg')
        # socket_service()
        transita_service()
        ser.write(('Start:' + str(result_lst)[1:-1] + '!').encode())
        order += 1
        if order > 11:
            break

for i in range(12):
    socket_service()


