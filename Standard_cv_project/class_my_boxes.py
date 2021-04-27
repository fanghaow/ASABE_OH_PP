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
    def __init__(self, path = 'standard_competition/randomimg/10008.jpg',center = (260, 260) ,threhold_relative = 0.45 ,threhold_dis = 10):
        self.path = path 
        self.detect_len = 90
        self.center = center # (480,480)
        self.threhold_relative, self.threhold_dis = threhold_relative, threhold_dis
        self.num_stick = 8 # default
        self.step = 4
        self.img = cv2.imread(self.path)

    def visual_stick(self):
        img = cv2.imread(self.path)
        center = self.center
        step = 4 #######
        circle_len = list(range(50, 90, step))
        # Filter out clutter and determine the number of stems
        x_y = []
        theta_list = []
        for i in range(len(circle_len)):
            x, y, theta = identify_stick(img, circle_len[i], center)
            theta_list.append(theta)
            x_y.append((x, y))
        stick_result = [len(i[0]) for i in x_y]
        print('stick result: ', stick_result)
        max_num = 1
        for i in set(stick_result):
            if stick_result.count(i) >= max_num:
                max_num = stick_result.count(i)
                num_stick = i
        print('The number of sticks is: ', num_stick)
        # formula1 : Find the longest line segment
        b = stick_result.count(num_stick)
        c = -1
        for i in range(b):
            c = stick_result.index(num_stick, c + 1, len(stick_result))
            if i == 0:
                start = c
            if i == b - 1:
                end = c
        index_theta = [index for index,item in enumerate(theta_list) if len(item) == num_stick]
        for i in range(len(index_theta) - 2):
            difference = diff(np.array(theta_list[start]), np.array(theta_list[end]))
            if difference <= 40: # 40 : Outer and inside ring stem angle difference threshold
                break
            else:
                end = index_theta[-i-2]
        if difference > 40:
            end = index_theta[-1]
        # formula2 : Find the most similar angle
        # index_theta = [index for index,item in enumerate(theta_list) if len(item) == num_stick]
        # dic = {}
        # for i in index_theta:
        #     for j in index_theta:
        #         dic[(i,j)] = diff(np.array(theta_list[i]), np.array(theta_list[j]))
        # print(dic)
        # min_value = 10e8
        # for key, value in dic.items():
        #     if value < min_value and value != 0:
        #         min_value = value
        #         best_key = key
        # start, end = best_key[1], best_key[0]
        x1, y1 = x_y[start][0], x_y[start][1]
        x2, y2 = x_y[end][0], x_y[end][1]

        # visualizing sticks
        img = cv2.imread(self.path)  # (480, 520, 3) col, row, channel
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
        img = cv2.imread(self.path)  # (480, 520, 3) col, row, channel
        for i in range(self.num_stick):
            x_leave, y_leave = third_point((x1[i], y1[i]), (x2[i], y2[i]), 115 - self.start * self.step)
            box_len = 15
            img = draw_box(img, (y_leave - box_len, x_leave - box_len), (y_leave + box_len, x_leave + box_len))
        plt.imshow(img)
        plt.show()

    def classification(self, start_list, end_list):
        (x1, y1) = start_list
        (x2, y2) = end_list
        img = cv2.imread(self.path)  # (480, 520, 3) col, row, channel
        img = cv2.GaussianBlur(img, (5, 5), cv2.BORDER_DEFAULT) # Gaussian filter
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        result = []
        for order in range(len(x1)):
            xx, yy = [], []
            for i in range(60, 90): # (60, 160)
                x, y = third_point((x1[order], y1[order]), (x2[order], y2[order]), 115 - 50 - self.start * self.step + i) # 180 2 * i
                if x < img.shape[0] and y < img.shape[1]:
                    xx.append(x)  # row
                    yy.append(y)  # col
            line_data = img[xx, yy]  # img[row, col]
            #
            img = cv2.line(img, (yy[0], xx[0]), (yy[-1], xx[-1]), (255, 0, 0), 5)
            plt.imshow(img) #plt.show()
            # plt.plot(line_data[:,0]),plt.title(order),plt.show()
            #
            data = list(line_data[:, 0])
            result.append(np.mean(data))
            # plt.plot(xx)
        plt.show()
        result_rate = [i / max(result) for i in result]
        plt.plot(result), plt.title('Result')
        white_index = []
        for index,item in enumerate(result):
            if item > 100 and result_rate[index] > 0.75: # 105 : light_threhold, 0.78 : rate_threhold
                white_index.append(index)
                plt.scatter(index, item, color='r')
        plt.show()
        return white_index

    def visual_result(self, start_list, end_list ,white_index):
        (x1, y1) = start_list
        (x2, y2) = end_list
        img = cv2.imread(self.path)  # (480, 520, 3) col, row, channel
        ################################
        # TO DO: set a threhold for removing boxes which are too close!
        dist_dict = {}
        for i in white_index:
            for j in white_index:
                x_c1, y_c1 = third_point((x1[i], y1[i]), (x2[i], y2[i]), 120) # 380
                x_c2, y_c2 = third_point((x1[j], y1[j]), (x2[j], y2[j]), 120) # 380
                dist_dict[(i, j)] = diff(np.array([x_c1, y_c1]), np.array([x_c2, y_c2]))
        print('Distance dictionary : ',dist_dict)
        threhold_value = 60
        key_rm, fate_white_index = [], []
        for key,value in dist_dict.items():
            if value < threhold_value and value != 0 and key[0] not in key_rm:
                white_index.remove(key[0])
                fate_white_index.append(key[0])
                key_rm.append(key[0]); key_rm.append(key[1])
        for order in fate_white_index:
            x_leave, y_leave = third_point((x1[order], y1[order]), (x2[order], y2[order]), 120) # 380
            box_len = 20 # 50
            draw_box(img, (y_leave - box_len, x_leave - box_len), (y_leave + box_len, x_leave + box_len), color = 'r')
        ################################
        print(white_index)
        for order in white_index:
            x_leave, y_leave = third_point((x1[order], y1[order]), (x2[order], y2[order]), 130) # 380
            box_len = 20 # 50
            draw_box(img, (y_leave - box_len, x_leave - box_len), (y_leave + box_len, x_leave + box_len),  color = 'g')
        plt.imshow(img)
        plt.show()

def diff(array1,array2):
    result = np.sqrt(np.sum((array1 - array2) ** 2))
    return result

def identify_stick(img, detect_len, center):
    x = []
    y = []
    bgr_array = np.zeros((360,3))
    for theta in range(360):
        x.append(int(center[0] + detect_len*cos(theta/180*pi)))
        y.append(int(center[1] + detect_len*sin(theta/180*pi)))
        bgr_array[theta,:] = np.array(img[x[theta], y[theta]])
    gray = bgr_array[:,0] # np.mean(bgr_array, 1)
    # plt.scatter(list(range(360)),gray),plt.plot(gray),plt.title('gray_360'),plt.show()
    theta = []
    threhold_relative, threhold_dis = 0.42, 8
    for i in range(1,len(gray)-1):
        if gray[i] < (gray[i-1] + gray[i+1]) * threhold_relative and gray[i] < 160: # add 160 edge!!!
            theta.append(i)
    print('theta:',theta)
    print('length of theta:',len(theta)) 
    # plt.scatter(theta, gray[theta]),plt.plot(gray),plt.show()
    if len(theta) <= 1:
        print('No valley is found')
        return [0], [0], 0
    new_theta = [[] for i in range(len(theta))]
    j = 0
    new_theta[j].append(theta[0])
    for index in range(len(theta) - 1):
        if abs(theta[index] - theta[index+1]) <= 9:
            new_theta[j].append(theta[index+1])
        else:
            # print('i am here')
            j += 1
            new_theta[j].append(theta[index+1])
    print('new_theta:',new_theta)
    theta = []
    for lst in new_theta:
        if lst == []:
            break
        pos = np.where(gray == np.min(gray[lst]))
        if pos[0].shape[0] >= 2:
            for item in list(pos[0]):
                if item in lst:
                    pos = item
                    break
        else:
            pos = int(pos[0])
        theta.append(pos)

    # plt.scatter(theta, gray[theta]),plt.plot(gray),plt.show()
    stick_x = [int(center[0] + detect_len*cos(i/180*pi)) for i in theta]
    stick_y = [int(center[1] + detect_len*sin(i/180*pi)) for i in theta]
    return stick_x, stick_y, theta

def third_point(start_p, end_p, distance):
    (x1, y1) = start_p
    (x2, y2) = end_p
    x_new = (x2 - x1) * distance / sqrt((x2-x1)**2 + (y2-y1)**2) + x1
    y_new = (y2 - y1) * distance / sqrt((x2-x1)**2 + (y2-y1)**2) + y1
    return int(x_new), int(y_new)

def draw_box(img, left_top, right_down, color = 'r'):
    (left,top) = left_top
    (right,down) = right_down
    if color == 'r':
        img = cv2.rectangle(img,(left,top),(right,down),(255,0,0),3)
    else:
        img = cv2.rectangle(img,(left,top),(right,down),(0,255,0),3)
    return img

def main():
    rand_list = np.random.choice(120, 12, False)
    print('My random list : ',rand_list)
    time.sleep(5)
    for index,item in enumerate(rand_list): # range(5,120)
        t_start = time.time()
        my_box = boxes(path = 'standard_competition/IMAGE_JPEG/' + str(10005+index) + '.jpg')
        (x1,y1), (x2,y2) = my_box.visual_stick()
        white_index = my_box.classification((x1,y1), (x2,y2))
        my_box.visual_result((x1,y1), (x2,y2), white_index)
        # my_box.all_box((x1,y1), (x2,y2))
        t_end = time.time()
        print('It takes me %f seconds to draw'%(t_end - t_start))

if __name__ == '__main__':
    main()
