#!/usr/bin/env python2
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
import time
import os

# global set
num = 1
time.sleep(1)
# filename = "matrix_seat.txt"
# filename = "matrix_feild.txt"
filename = "matrix.txt"

def reader(number):
    matrix = np.zeros((800,2))
    f = open(filename)
    length = 802
    # Read extra point clouds
    for i in range(number*length):
        f.readline()
    for i in range(0,800):
        line_cont  = f.readline()
        if i==0:
            # print(line_cont)
            continue
        if i==799:
            while(True):
                try:
                    f.readline()
                    end = f.readline()
                    # print(end)
                    break
                except:
                    print("Not in the end")
        line_cont = line_cont.rstrip("\n")
        line_lst = line_cont.split(" ")
        jj= 0
        for string in line_lst:
            try:
                string = float(string)
            except:
                # print("Exception :", string)
                pass
            if isinstance(string, float):
                # print(string)
                matrix[i,jj] = string
                jj += 1
    f.close()
    return matrix

# animation function.  This is called sequentially
def animate(index):
    global pre_im, is_empty
    print("Index : ", index)
    colors=np.random.rand(360)
    # load_m = plt.scatter(xx, yy, c=colors)
    plt.cla()
    global num
    matrix = reader(num)
    if (matrix == 0).all():
        time.sleep(0.1)
        print("No completed data get in")
        # return [load_m]
        origin_im = plt.scatter(ori_matrix[:,0],ori_matrix[:,1],s=3)
        plt.xlim(-5,5)
        plt.ylim(-5,5)
        return [origin_im]
    num += 1
    im = plt.scatter(matrix[:,0],matrix[:,1],s=3)
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    time.sleep(0.01)
    return [im]

def main():
    time.sleep(2)
    # try:
    #     os.remove("matrix.txt")
    # except:
    #     pass
    global xx, yy, ori_matrix
    matrix = reader(2)
    ori_matrix = matrix.copy()
    # print(matrix)
    fig = plt.figure()
    im = plt.scatter(matrix[:,0],matrix[:,1],s=3)
    plt.xlim(-5,5)
    plt.ylim(-5,5)
    xx = [2*np.cos(i) for i in range(360)]
    yy = [2*np.sin(i) for i in range(360)]
    anim = animation.FuncAnimation(fig, animate, frames=200, interval=60, blit=True)
    plt.show()

    
if __name__ =="__main__":
    main()