#!/usr/bin/env python
# encoding:utf-8
import numpy as np
import socket
import sys
import os
import time
#RPi's IP
SERVER_IP = "192.168.43.207"
SERVER_PORT = 8888
lsta = [str(20) for i in range(24)]
green, yellow = 0, 0
yellow_lst = [str(20) for i in range(12)]
green_lst = [str(20) for i in range(12)]

class data_tf_gui():
    def __init__(self):
        pass

    def readfile(self):
        while(True):
            try:
                f = open(r"/Users/fanghao_w/Desktop/vs_py_project/cpp接口/2.jpg.txt", "r") 
                time.sleep(0.5)
                break
            except:
                print('No txt found')
        text = f.readlines()
        # print(text)
        imgfile = text[-1][0:-1]
        text[0] = text[0][0:-1]
        obj_num = int(text[0])
        text.pop(-1)
        text.pop(0)

        # print(text)
        data = np.zeros((len(text), 4))
        class_name = []
        for index, line in enumerate(text):
            str_list = line.split(',')
            [str_list[3], class_str] = str_list[3].split(']')
            # print(class_str)
            class_name.append(class_str[0:-1])
            for i, item in enumerate(str_list):
                if '[' in item:
                    str_list[i] = item[1:]
                elif ']' in item:
                    str_list[i] = item[1:-1]
                else:
                    str_list[i] = item[1:]

            for j,str_num in enumerate(str_list):
                data[index][j] = int(str_num)
        #
        print('filename:',imgfile)
        print('obj_num:',obj_num)
        print('data:\n',data)
        print('class_name:',class_name)
        return obj_num, data, class_name

    def transport(self):
        global lsta
        str_lsta = ''
        for index,item in enumerate(lsta):
            str_lsta += str(item)
            if index <= 22:
                str_lsta += '/'
        
        print("Starting socket: TCP...")
        server_addr = (SERVER_IP, SERVER_PORT)
        socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        while True:
            try:
                print("Connecting to server @ %s:%d..." %(SERVER_IP, SERVER_PORT))
                socket_tcp.connect(server_addr)
                break
            except Exception:
                print("Can't connect to server,try it latter!")
                time.sleep(1)
                continue
        print("Please input 1 or 0 to turn on/off the led!")
        i = 0
        while True:
            try:
                data = socket_tcp.recv(512)
                if len(data)>0:
                    print("Received: %s" % data.decode())
                    #command=input()
                    command = str_lsta
                    socket_tcp.send(command.encode())
                    time.sleep(1)
                    i += 1
                    if i > 0:
                        break
                    #continue
            except Exception:
                socket_tcp.close()
                socket_tcp=None
                sys.exit(1)

def main():
    tf = data_tf_gui()
    for i in range(12):
        num, data, leaf_class  = tf.readfile()
        print('%%%%%%',leaf_class)
        if '0' in leaf_class:
            yellow_lst[i] = 0
        if '1' in leaf_class:
            pass
        for j, name in enumerate(leaf_class):
            if name == '0':
                yellow_lst[i] += 1
            if name == '1':
                pass
        print('#####',yellow_lst)
        strange_order = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
        for index, order in enumerate(strange_order):
            # lsta[(order1 + 1) * 2 - 1] = green_lst[index]
            global lsta
            lsta[(order + 1) * 2 - 2] = yellow_lst[index]

        print('send data:', lsta)
        tf.transport()
    

if __name__ == '__main__':
    main()
    print('success!')
