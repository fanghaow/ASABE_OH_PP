#! usr/bin/env python
# encoding:utf-8
import numpy as np
import matplotlib.pyplot as plt
import cv2
import time
from math import *
import os
import sys

path = 'IMAGE_JPEG/'
img = cv2.imread(path + '10002' + '.jpg') # (480, 520, 3) col, row, channel
center = [260, 270] # col, row
detect_len = 90
x = []
y = []
bgr_array = np.zeros((360,3))
for theta in range(360):
    x.append(int(center[0] + detect_len*cos(theta/180*pi)))
    y.append(int(center[1] + detect_len*sin(theta/180*pi)))
    bgr_array[theta,:] = np.array(img[x[theta], y[theta]])
# plt.plot(detect_circle[:,0], detect_circle[:,1])
plt.figure(1)
plt.subplot(2,3,1),plt.plot(bgr_array[:,0]),plt.title('blue')
plt.subplot(2,3,2),plt.plot(bgr_array[:,1]),plt.title('green')
plt.subplot(2,3,3),plt.plot(bgr_array[:,2]),plt.title('red')

gray = np.mean(bgr_array,1)
plt.subplot(2,1,2),plt.plot(gray),plt.title('gray')
extra_point = []
threhold_relative, threhold_dis = 0.45, 3
for i in range(1,len(gray)-1):
    if gray[i] < (gray[i-1] + gray[i+1])*threhold_relative:
        extra_point.append(i)
plt.show()

print(extra_point)
print(len(extra_point))
delete_list = []
for index,item in enumerate(extra_point):
    if abs(item - extra_point[index+1]) < threhold_dis:
        delete_list.append(item)
    if index >= len(extra_point)-2:
        break
plt.figure(2)
for i in delete_list:
    extra_point.remove(i)
print('茎干角度：',extra_point)
num_stick = len(extra_point)
print('茎干根数：',num_stick)
plt.plot(gray)
for i in extra_point:
    plt.scatter(i, gray[i], color='r')
plt.show()

# visualizing sticks
plt.figure(3)
path = 'IMAGE_JPEG/'
img = cv2.imread(path + '10002' + '.jpg') # (480, 520, 3) col, row, channel
for i in range(num_stick):
    img = cv2.line(img,(center[0],center[1]),(y[extra_point[i]], x[extra_point[i]]),(255,0,0),2)
plt.subplot(2,1,1),plt.imshow(img),plt.title('sticks')

# visualizng my boxs
path = 'IMAGE_JPEG/'
img = cv2.imread(path + '10002' + '.jpg') # (480, 520, 3) col, row, channel
distance = 200
col_len, row_len = 15, 15
col, row = [], []
def draw_box(img,left_top,right_down):
    (left,top) = left_top
    (right,down) = right_down
    img = cv2.rectangle(img,(left,top),(right,down),(0,255,0),3)
    return img
for i in range(num_stick):
    img = cv2.line(img,(center[0],center[1]),(y[extra_point[i]], x[extra_point[i]]),(255,0,0),3)
    theta = atan2(y[extra_point[i]] - center[0],x[extra_point[i]] - center[1])
    col.append(center[0] + int(distance*sin(theta)))
    row.append(center[1] + int(distance*cos(theta)))
    img = cv2.line(img,(center[0],center[1]),(col[i], row[i]),(0,0,250),3)
    # draw my boxes
    img = draw_box(img,(col[i]-col_len, row[i]-row_len),(col[i]+col_len, row[i]+row_len))
plt.subplot(2,1,2),plt.imshow(img),plt.title('my boxes')
plt.show()

# my rois
path = 'IMAGE_JPEG/'
img = cv2.imread(path + '10002' + '.jpg') # (480, 520, 3) col, row, channel
img_list = []
plt.figure(4)
for i in range(num_stick):
    img_list.append(img[row[i]-row_len:row[i]+row_len, col[i]-col_len:col[i]+col_len])
    plt.subplot(1,num_stick,i+1),plt.imshow(img_list[i])
plt.show()

r_mean, g_mean, b_mean = [], [], []
for i in range(num_stick):
    r_mean.append(np.mean(img_list[i][:,:,0]))
    g_mean.append(np.mean(img_list[i][:,:,1]))
    b_mean.append(np.mean(img_list[i][:,:,2]))
rgb_mean = [r_mean, g_mean, b_mean]
plt.figure(5)
for i in range(3):
    plt.subplot(3,1,i+1),plt.plot(rgb_mean[i])
    pass
plt.show()

# algrithm
mean = np.mean(r_mean) * 1.2
plt.figure(6)
plt.plot(r_mean)
plt.axhline(y = mean, color='r', linestyle='-')
plt.show()

white_list = []
for i in range(num_stick):
    if r_mean[i] > mean:
        white_list.append(i)

print('白色叶子的数量:',len(white_list))