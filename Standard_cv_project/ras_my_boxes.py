#! usr/bin/env python
# encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from math import *
import os
import sys

class boxes():
    def __init__(self, img, path = 'IMAGE_JPEG/10001.jpg',center = (260,260) ,threhold_relative = 0.45 ,threhold_dis = 10):
        self.path = path
        self.img = img
        self.detect_len = 90
        self.center = center
        self.threhold_relative, self.threhold_dis = threhold_relative, threhold_dis
        self.num_stick = 8 # default
        self.step = 4

    def visual_stick(self):
        img = self.img
        center = self.center
        step = 4 #######
        circle_len = list(range(60, 100, step))
        # 滤除杂波，确定茎干数目
        x_y = []
        for i in range(len(circle_len)):
            x, y, theta = identify_stick(img, circle_len[i], center)
            x_y.append((x, y))
        stick_result = [len(i[0]) for i in x_y]
        print('stick result: ', stick_result)
        max_num = 1
        for i in set(stick_result):
            if stick_result.count(i) >= max_num:
                max_num = stick_result.count(i)
                num_stick = i
        print('The number of sticks is: ', num_stick)
        # 求取最长的线段
        b = stick_result.count(num_stick)
        c = -1
        for i in range(b):
            c = stick_result.index(num_stick, c + 1, len(stick_result))
            if i == 0:
                start = c
            if i == b - 1:
                end = c
        #     print(num_stick,c)
        x1, y1 = x_y[start][0], x_y[start][1]
        x2, y2 = x_y[end][0], x_y[end][1]

        # visualizing sticks
        img = self.img  # (480, 520, 3) col, row, channel
        for i in range(num_stick):
            img = cv2.line(img, (y1[i], x1[i]), (y2[i], x2[i]), (255, 0, 0), 5)
        plt.imshow(img)
        plt.show()
        self.num_stick = len(x1)
        self.start, self.end = start, end

        return (x1,y1), (x2,y2)


    def all_box(self, start_list, end_list): # {start_list, end_list : (x1, y1), (x2, y2)}
        # visualizing my boxes
        (x1, y1) = start_list
        (x2, y2) = end_list
        img = self.img  # (480, 520, 3) col, row, channel
        for i in range(self.num_stick):
            x_leave, y_leave = third_point((x1[i], y1[i]), (x2[i], y2[i]), 115 - self.start * self.step)
            box_len = 15
            img = draw_box(img, (y_leave - box_len, x_leave - box_len), (y_leave + box_len, x_leave + box_len))
        plt.imshow(img)
        plt.show()

    def classification(self, start_list, end_list):
        (x1, y1) = start_list
        (x2, y2) = end_list
        img = self.img  # (480, 520, 3) col, row, channel
        img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT) # 高斯滤波
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        result = []
        for order in range(len(x1)):
            xx, yy = [], []
            for i in range(60, 90):
                x, y = third_point((x1[order], y1[order]), (x2[order], y2[order]), 115 - 50 - self.start * self.step + i)
                if x < img.shape[0] and y < img.shape[1]:
                    xx.append(x)  # row
                    yy.append(y)  # col
            line_data = img[xx, yy]  # img[row, col]
            #     plt.plot(line_data[:,0]),plt.title(order)
            data = list(line_data[:, 0])
            result.append(np.mean(data))
            # plt.plot(xx)
        result_rate = [i / max(result) for i in result]
        plt.plot(result), plt.title('result')
        white_index = []
        for index,item in enumerate(result):
            if item > 105 and result_rate[index] > 0.78:
                white_index.append(index)
                plt.scatter(index, item, color='r')
        plt.show()
        return white_index

    def visual_result(self, start_list, end_list ,white_index):
        (x1, y1) = start_list
        (x2, y2) = end_list
        img = self.img  # (480, 520, 3) col, row, channel
        print(white_index)
        for order in white_index:
            x_leave, y_leave = third_point((x1[order], y1[order]), (x2[order], y2[order]), 120)
            box_len = 15
            draw_box(img, (y_leave - box_len, x_leave - box_len), (y_leave + box_len, x_leave + box_len))
        plt.imshow(img)
        plt.show()

def identify_stick(img, detect_len, center):
    x = []
    y = []
    bgr_array = np.zeros((360,3))
    for theta in range(360):
        x.append(int(center[0] + detect_len*cos(theta/180*pi)))
        y.append(int(center[1] + detect_len*sin(theta/180*pi)))
        bgr_array[theta,:] = np.array(img[x[theta], y[theta]])
    gray = np.mean(bgr_array, 1)
    # plt.figure(1)
    # plt.plot(gray)
    theta = []
    threhold_relative, threhold_dis = 0.45, 10
    for i in range(1,len(gray)-1):
        if gray[i] < (gray[i-1] + gray[i+1])*threhold_relative and gray[i] < 70: # add 70 edge!!!
            theta.append(i)
#     print(theta)
#     print(len(theta))
    delete_list = []
    for index,item in enumerate(theta):
        if abs(item - theta[index+1]) < threhold_dis:
            # delete_list.append(item)
            if min(item,theta[index+1]) not in delete_list:
                delete_list.append(min(item,theta[index+1]))
            else:
                delete_list.append(theta[index+1])
        if index >= len(theta)-2:
            break

    for i in delete_list:
        theta.remove(i)

    stick_x = [int(center[0] + detect_len*cos(i/180*pi)) for i in theta]
    stick_y = [int(center[1] + detect_len*sin(i/180*pi)) for i in theta]
    return stick_x, stick_y, theta

def third_point(start_p, end_p, distance):
    (x1, y1) = start_p
    (x2, y2) = end_p
    x_new = (x2 - x1) * distance / sqrt((x2-x1)**2 + (y2-y1)**2) + x1
    y_new = (y2 - y1) * distance / sqrt((x2-x1)**2 + (y2-y1)**2) + y1
    return int(x_new), int(y_new)

def draw_box(img, left_top, right_down):
    (left,top) = left_top
    (right,down) = right_down
    img = cv2.rectangle(img,(left,top),(right,down),(0,255,0),3)
    return img

def main():
    cap = cv2.VideoCapture(0)
    while(True):
        t_start = time.time()
        ret, img = cap.read()
        my_box = boxes(img)
        (x1,y1), (x2,y2) = my_box.visual_stick()
        white_index = my_box.classification((x1,y1), (x2,y2))
        my_box.visual_result((x1,y1), (x2,y2), white_index)
        # my_box.all_box((x1,y1), (x2,y2))
        t_end = time.time()
        print('It takes me %f seconds to draw'%(t_end - t_start))

if __name__ == '__main__':
    main()
