# -*- coding: utf-8 -*-
# Python 3.7
# This is a GUI program for the 2021 ASABE Student Robotics Competition.
# Please refer to Appendix C in the competition rules.
# Author: Yin Bao, Auburn University, Biosystems Engineering Department

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QLineEdit, QLCDNumber, QComboBox, QLabel
import numpy as np
import socket
import threading
import time
import random
import math

NAME_IP_LIST = []
#Change the names and IP addresses of your robots in the list.
#They will be populated in the drop down manual
NAME_IP_LIST.append(['robot1','192.168.123.164'])
# NAME_IP_LIST.append(['robot1','192.168.0.2'])
NAME_IP_LIST.append(['robot2','192.168.0.3'])
# SERVER_IP = '192.168.0.1'
SERVER_IP = '127.0.0.1'
PORT = 8888 # 50007

######
#import necessary package
import socket
import time
import sys
#define host ip: Rpi's IP
HOST_IP = "192.168.123.164"  # fanghao_w ubuntu IP:192.168.43.207
HOST_PORT = 8888
print("Starting socket: TCP...")
#1.create socket object:socket=socket.socket(family,type)
lst = []
def transport():
    socket_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("TCP server listen @ %s:%d!" %(HOST_IP, HOST_PORT) )
    host_addr = (HOST_IP, HOST_PORT)
    #2.bind socket to addr:socket.bind(address)
    socket_tcp.bind(host_addr)
    #3.listen connection request:socket.listen(backlog)
    socket_tcp.listen(1)
    #4.waite for client:connection,address=socket.accept()
    socket_con, (client_ip, client_port) = socket_tcp.accept()
    print("Connection accepted from %s." %client_ip)
    socket_con.send("Welcome to COM TCP server!".encode())
    #5.handle
    print("Receiving package...")
    i = 1
    while True:
        try:
            data=socket_con.recv(512)
            if len(data)>0:
                data = data.decode()
                print("Received:%s"%data)
                lst.append(data)
                # if str(data)[2]=='1':
                #     print('Great!')
                # elif str(data)[2]=='0':
                #     print('No!')
                socket_con.send(data.encode())
                #time.sleep(1)
                i += 1
                if(i > 1):
                    socket_tcp.close()
                    break
                continue
        except Exception:
                socket_tcp.close()
                sys.exit(1)

######
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):

        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1080, 700)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        #dropdown menu for selecting ip address of Robot 1
        self.dropdown_menu1 = QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.dropdown_menu1.setFont(font)
        self.dropdown_menu1.setGeometry(QtCore.QRect(40, 540, 240, 50))
        self.robot_index = 0
        for name_ip in NAME_IP_LIST: 
            text = name_ip[0] + ': ' + name_ip[1]
            self.dropdown_menu1.addItem(text)
        self.dropdown_menu1.currentIndexChanged.connect(self.Robot1SelectionChange)

        #dropdown menu for selecting ip address of Robot 2
        self.dropdown_menu2 = QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.dropdown_menu2.setFont(font)
        self.dropdown_menu2.setGeometry(QtCore.QRect(750, 540, 240, 50))
        self.robot_index = 0
        for name_ip in NAME_IP_LIST: 
            text = name_ip[0] + ': ' + name_ip[1]
            self.dropdown_menu2.addItem(text)
        self.dropdown_menu2.currentIndexChanged.connect(self.Robot2SelectionChange)

        self.robotIDs = [0, 0]

        font = QtGui.QFont()
        font.setPointSize(20)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(10, 10, 1060, 431))
        self.graphicsView.setObjectName("graphicsView")
        self.StandardButton = QtWidgets.QPushButton(self.centralwidget)
        self.StandardButton.setGeometry(QtCore.QRect(450, 460, 170, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.StandardButton.sizePolicy().hasHeightForWidth())
        self.StandardButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.StandardButton.setFont(font)
        self.StandardButton.setObjectName("StandardButton")
        self.AdvancedButton = QtWidgets.QPushButton(self.centralwidget)
        self.AdvancedButton.setGeometry(QtCore.QRect(450, 620, 170, 40))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.AdvancedButton.setFont(font)
        self.AdvancedButton.setObjectName("AdvancedButton")

        # Button for start timer
        self.StartButton = QtWidgets.QPushButton(self.centralwidget)
        self.StartButton.setGeometry(QtCore.QRect(560, 535, 100, 52))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.StartButton.setFont(font)
        self.StartButton.setObjectName("StartButton")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # LCD for displaying the score of Robot 1
        self.LCD1 = QLCDNumber(self.centralwidget)
        self.LCD1.setGeometry(QtCore.QRect(120, 480, 100, 40))
        self.LCD1.display(0)
        self.LCD1.setStyleSheet('QLCDNumber {background-color: green; color: red;}')          

        # LCD for displaying the score of Robot 2
        self.LCD2 = QLCDNumber(self.centralwidget)
        self.LCD2.setGeometry(QtCore.QRect(820, 480, 100, 40))
        self.LCD2.display(0)
        self.LCD2.setStyleSheet('QLCDNumber {background-color: green; color: red;}')    

        self.scoreLCDs = [self.LCD1, self.LCD2]   
        
        self.clockLCD = QLCDNumber(self.centralwidget)
        self.clockLCD.setGeometry(QtCore.QRect(400, 536, 100, 43))
        self.clockLCD.display('3:00')
        self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}')

        self.scene = QGraphicsScene()
        self.scene.setBackgroundBrush(Qt.gray)
        self.graphicsView.setScene(self.scene)
        greenBrush = QBrush(Qt.green)   
        yellowBrush = QBrush(Qt.yellow) 
        whiteBrush = QBrush(Qt.white)   
        blueBrush = QBrush(Qt.blue)     
        pinkBrush = QBrush(Qt.magenta) 
        self.blackPen = QPen(Qt.black)
        self.BrushList = [greenBrush, yellowBrush, whiteBrush, blueBrush, pinkBrush, QBrush(Qt.black)]
        self.colorNames = ['Empty', 'Stressed', 'Healthy', 'Double','Tiller','Detection']
        
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        self.AdvancedButton.clicked.connect(self.AdvBtnClickedSlot)
        self.StandardButton.clicked.connect(self.StdBtnClickedSlot)
        self.StartButton.clicked.connect(self.StartBtnClickedSlot)
        
        self.drawing_timer = QTimer()
        self.drawing_timer.setInterval(50)
        self.drawing_timer.timeout.connect(self.updateDetectionResult)
        self.drawing_timer.start()

        self.clock_seconds = 0
        self.timestamp = '0:00'
        self.clock_timer = QTimer()
        self.clock_timer.setInterval(1000)
        self.clock_timer.timeout.connect(self.updateClock)
        self.time_is_up = False

        app.aboutToQuit.connect(self.closeEvent)

        #Table 1
        self.plantTypes = np.zeros([23,3], dtype=np.uint8)
        self.plantTypes[0,:] = [6,0,0]
        self.plantTypes[1,:] = [5,0,1]
        self.plantTypes[2,:] = [4,2,0]
        self.plantTypes[3,:] = [4,1,1]
        self.plantTypes[4,:] = [3,3,0]
        self.plantTypes[5,:] = [7,0,0]
        self.plantTypes[6,:] = [6,1,0]
        self.plantTypes[7,:] = [5,1,1]
        self.plantTypes[8,:] = [4,1,2]
        self.plantTypes[9,:] = [4,0,3]
        self.plantTypes[10,:] = [8,0,0]
        self.plantTypes[11,:] = [7,1,0]
        self.plantTypes[12,:] = [6,1,1]
        self.plantTypes[13,:] = [5,2,1]
        self.plantTypes[14,:] = [4,0,4]
        self.plantTypes[15,:] = [8,0,1]
        self.plantTypes[16,:] = [7,0,1]
        self.plantTypes[17,:] = [7,0,2]
        self.plantTypes[18,:] = [6,0,3]
        self.plantTypes[19,:] = [6,0,2]
        self.plantTypes[20,:] = [5,0,4]
        self.plantTypes[21,:] = [5,0,3]
        self.plantTypes[22,:] = [5,0,2]

        # row layout in terms of plant ID,    
        # 12 plants in the row
        self.standardRowLayout = [3, 14, 9, 10, 15, 15]
        self.standardRowLayout.append(random.choice([1,6,11]))
        self.standardRowLayout.append(random.choice([1,6,11]))
        self.standardRowLayout.append(random.choice([2,5]))
        self.standardRowLayout.append(random.choice([7,12]))
        self.standardRowLayout.append(random.choice([4,8,13]))
        self.standardRowLayout.append(random.choice([4,8,13]))

        # 9 plants in the 1st row for ADVANCED 
        self.advancedRowLayout = [3, 14, 9, 10, 15]
        self.advancedRowLayout.append(random.choice([1,6,11]))
        self.advancedRowLayout.append(random.choice([7,12]))
        self.advancedRowLayout.append(random.choice([2,5]))
        self.advancedRowLayout.append(random.choice([4,8,13]))
        # 5 plants in the 2nd row for ADVANCED 
        self.pruningRowLayout = [21,18]
        self.pruningRowLayout.append(random.choice([16,17]))
        self.pruningRowLayout.append(random.choice([20,23]))
        self.pruningRowLayout.append(random.choice([19,22]))

        self.stemPatternIndices = [list(range(0,6)), list(range(0,7)), list(range(0,8)), list(range(0,9))]
        for i in range(4):
            random.shuffle(self.stemPatternIndices[i])
    
        # the plant order is the same as that in the rules. yellow, white, ...
        # plant order is left to right (top row first for advanced)
        self.robotDetectionMaps = []
        self.scoreMasks = [np.ones(24, dtype=np.uint8), np.ones(28, dtype=np.uint8)]
        self.scoreMasks[0][1:24:2] = 3  # standard
        self.scoreMasks[1][1:28:2] = 3  # advanced

        self.newDetectionAvailable = False
        self.lock = threading.Lock()

        self.StdBtnClickedSlot()

        self.clientThreads = []
        self.serverRunning = True
        self.serverThread = threading.Thread(target = self.server)
        self.serverThread.start()
        
    def randomizeRowLayout(self):
        if self.level == 0:
            self.lock.acquire()
            self.robotDetectionMaps = [np.zeros(24, dtype=np.uint8)+255, np.zeros(24, dtype=np.uint8)+255]
            print(self.robotDetectionMaps)
            self.lock.release()
            random.shuffle(self.standardRowLayout)
            self.trueMap = np.zeros(24, dtype=np.uint8)
            for i in range(12):
                self.trueMap[2*i:2*i+2] = self.plantTypes[self.standardRowLayout[i]-1,1:3]
            #######
            # result = [0, 1, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            # left, right = np.array(result[0:12], dtype=np.uint8), np.array(result[12:], dtype=np.uint8)
            # up_robot = np.hstack((left, right))
            # down_robot = np.hstack((left, right))
            # self.robotDetectionMaps = [up_robot, down_robot]
            #######
        else:
            self.lock.acquire()
            self.robotDetectionMaps = [np.zeros(28, dtype=np.uint8)+255, np.zeros(28, dtype=np.uint8)+255]
            self.lock.release()
            random.shuffle(self.advancedRowLayout)
            random.shuffle(self.pruningRowLayout)
            self.trueMap = np.zeros(28, dtype=np.uint8)
            for i in range(9):
                self.trueMap[2*i:2*i+2] = self.plantTypes[self.advancedRowLayout[i]-1,1:3]
            for i in range(9, 14):
                self.trueMap[2*i:2*i+2] = self.plantTypes[self.pruningRowLayout[i-9]-1,1:3]
        self.updateCanvas()
            
    def calculateScore(self, robotID):
        self.lock.acquire()
        diff = self.trueMap - self.robotDetectionMaps[robotID]
        self.lock.release()
        diff[diff != 0] = 1
        diff = 1 - diff
        score = np.multiply(diff, self.scoreMasks[self.level]).sum()
        self.scoreLCDs[robotID].display(score)

    def drawPlantAndDetection(self, x, y, plantID, numYellowLeafStems, numFlowerStems):  
        radius = 15
        leafSize = 10
        plantType = self.plantTypes[plantID-1]
        stemList = [0]*plantType[0]
        stemList.extend([1]*plantType[1])
        stemList.extend([2]*plantType[2])
        numStems = len(stemList)
        randStemList = [0]*numStems
        for i in range(numStems):
            randStemList[i] = stemList[self.stemPatternIndices[numStems-6][i]]

        stepSize = 2*math.pi/(numStems)
        for i in range(numStems):
            angle = stepSize*i
            self.scene.addEllipse(x+math.sin(angle)*radius, y+math.cos(angle)*radius, leafSize, leafSize, QPen(Qt.gray), self.BrushList[randStemList[i]])
        
        # draw robot detection results
        self.scene.addEllipse(x-10, y+40, leafSize, leafSize, QPen(Qt.gray), QBrush(Qt.yellow))  
        self.scene.addEllipse(x-10, y+60, leafSize, leafSize, QPen(Qt.gray), QBrush(Qt.white))
        if numYellowLeafStems == 255:
            numYellowLeafStems = 'na'
        t = self.scene.addText(str(numYellowLeafStems), QFont("Helvetica", 16))
        t.setPos(x, y+34)
        if numFlowerStems == 255:
            numFlowerStems = 'na' 
        t = self.scene.addText(str(numFlowerStems), QFont("Helvetica", 16))
        t.setPos(x, y+54)

    def updateCanvas(self):
        hor_space = 50
        ver_space = 150
        self.scene.clear()
        self.lock.acquire()
        robotResults = self.robotDetectionMaps
        self.lock.release()
        if self.level == 0:
            for y in range(2):
                for x in range(12):
                    x1 = x*hor_space+170
                    y1 = y*ver_space
                    numYellowLeafStems, numFlowerStems = robotResults[y][2*x:2*x+2]
                    self.drawPlantAndDetection(x1, y1, self.standardRowLayout[x], numYellowLeafStems, numFlowerStems)
                    plantID = self.standardRowLayout[x]
                    t = self.scene.addText(str(plantID), QFont("Helvetica", 16))
                    if plantID < 10:
                        t.setPos(x1-3, y1-5)
                    else:
                        t.setPos(x1-8, y1-5)
        else:
            for y in range(2):
                for x in range(9):
                    x1 = x*hor_space + y*10*hor_space
                    numYellowLeafStems, numFlowerStems = robotResults[y][2*x:2*x+2]
                    self.drawPlantAndDetection(x1, 0, self.advancedRowLayout[x], numYellowLeafStems, numFlowerStems)
                    plantID = self.advancedRowLayout[x]
                    t = self.scene.addText(str(plantID), QFont("Helvetica", 16))
                    if plantID < 10:
                        t.setPos(x1-3, -5)
                    else:
                        t.setPos(x1-8, -5)

                for x in range(5):
                    x1 = x*hor_space*2 + y*10*hor_space
                    numYellowLeafStems, numFlowerStems = robotResults[y][2*x+16:2*x+18]
                    self.drawPlantAndDetection(x1, ver_space, self.pruningRowLayout[x], numYellowLeafStems, numFlowerStems)
                    t = self.scene.addText(str(self.pruningRowLayout[x]), QFont("Helvetica", 16))
                    t.setPos(x1-8, ver_space-5)

            self.scene.addLine(QtCore.QLineF(9.1*hor_space, 0, 9.1*hor_space, 215))

        self.calculateScore(robotID = 0)
        self.calculateScore(robotID = 1)

    def updateClock(self):     
        if self.clock_seconds >= 300:      
            if self.clock_seconds%2 == 0:   
                self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}')
            else:
                self.clockLCD.setStyleSheet('QLCDNumber {background-color: white; color: red;}')
            self.clockLCD.display('5:00')
            self.time_is_up = True
        else:
            self.timestamp = str(self.clock_seconds//60)+':' 
            sec = self.clock_seconds%60
            self.timestamp += '0' + str(sec) if sec <10 else str(sec)
            self.clockLCD.display(self.timestamp)  
        self.clock_seconds += 1
        
    def updateDetectionResult(self):
       if self.newDetectionAvailable:
            self.updateCanvas()
            self.lock.acquire()
            self.newDetectionAvailable = False
            self.lock.release()

    def closeEvent(self):
        self.serverRunning = False
        if self.serverThread.is_alive() is True:
            self.serverThread.join()
        for t in self.clientThreads:
            if t.is_alive() is True:
                t.join()

    def client(self, robotID, c, ip, port):
        while self.serverRunning:
            try:
                c.settimeout(5)
                msg = c.recv(1024)
                text = msg.decode('utf-8')
                if text != '' and not self.time_is_up:
                    if self.level == 0 and len(text) != 24:
                        print('Wrong format! Please send 24 bytes for standard division.')
                        continue

                    if self.level == 1 and len(text) != 28:
                        print('Wrong format! Please send 28 bytes for advanced division.')
                        continue

                    self.lock.acquire()
                    self.robotDetectionMaps[robotID] = np.array(list(text), dtype=np.int8)
                    self.newDetectionAvailable = True
                    self.lock.release()

                    #file_name = 'log' + str(robotID+1)+'.txt'
                    #f = open(file_name, "a")
                    #f.write(self.ip_addr+','+self.timestamp+','+msg)
                    #f.close()
            except socket.timeout:
                print('client stopped sending updates')
                break
            except socket.error as exc:
                print(exc)
                break

            time.sleep(0.01)

        c.close()

    def server(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((SERVER_IP, PORT))
            s.setblocking(0)
            s.settimeout(1)
            s.listen(4)
            print('Gui server is waiting for connection')
            ###
            global lst
            lstk = []
            k = 0
            while True:
                transport()
                lstk.append(lst)
                k += 1
                if k > 120:
                    print('i break!!')
                    break
                result = [int(i) for i in lst[0].split('/')]
                print('result:',result)
                for index,item in enumerate(result):
                    if item == 20: # 20 代表未识别到
                        result[index] = 255
                left, right = np.array(result[0:12], dtype=np.uint8), np.array(result[12:], dtype=np.uint8)
                up_robot = np.hstack((left, right))
                na_array = np.zeros(12, dtype=np.uint8) + 255
                down_robot = np.hstack((na_array, na_array))
                self.robotDetectionMaps = [up_robot, down_robot]
                self.lock.acquire()
                self.newDetectionAvailable = True
                self.lock.release()
                print(self.robotDetectionMaps)
                lst = []
            time.sleep(1)
            ###
            robotID = -1
            while self.serverRunning:
                try:
                    (c, (ip, port)) = s.accept()
                    if ip == NAME_IP_LIST[self.robotIDs[0]][1]:
                        robotID = 0
                    elif ip == NAME_IP_LIST[self.robotIDs[1]][1]:
                        robotID = 1
                    else:
                        robotID = -1

                    if robotID != -1:
                        clientThread = threading.Thread(target = self.client, args = (robotID, c, ip, port,))
                        clientThread.start()
                        
                except socket.timeout:                    
                    if not self.serverRunning:
                        break

            s.close()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "2021 ASABE Robotics Competition"))
        self.StandardButton.setText(_translate("MainWindow", "Standard"))
        self.AdvancedButton.setText(_translate("MainWindow", "Advanced"))
        self.StartButton.setText(_translate("MainWindow", "Start"))

    def initialize(self):
        self.time_is_up = False
        self.clock_seconds = 0
        self.clockLCD.setStyleSheet('QLCDNumber {background-color: yellow; color: red;}')
        self.clock_timer.stop()
        self.clockLCD.display('0:00')
        
    def StdBtnClickedSlot(self):
        self.StandardButton.setStyleSheet("background-color: red")
        self.AdvancedButton.setStyleSheet("background-color: gray")
        self.level = 0
        self.randomizeRowLayout()
        self.initialize()
        
    def AdvBtnClickedSlot(self):
        self.AdvancedButton.setStyleSheet("background-color: red")
        self.StandardButton.setStyleSheet("background-color: gray")
        self.level = 1
        self.randomizeRowLayout()
        self.initialize()
    
    def StartBtnClickedSlot(self):
        self.clock_seconds = 0
        self.clock_timer.start()

    def Robot1SelectionChange(self):
        self.robotIDs[0] = self.dropdown_menu1.currentIndex()

    def Robot2SelectionChange(self):
        self.robotIDs[1] = self.dropdown_menu2.currentIndex()
            
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())