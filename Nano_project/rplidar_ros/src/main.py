#!/usr/bin/env python2
from txt_reader import reader
import numpy as np
from icp import ICP
import matplotlib.pyplot as plt
from matplotlib import animation
import time

class Odemtry():
    def __init__(self):
        self.z = np.zeros((800,1))
        self.theta = np.pi / 2
        self.thetas = []
        self.x = 0
        self.y = 0
        self.alpha = 1
        self.icp = ICP()

    def pc(self, number):
        self.src_pc = np.transpose(np.hstack((reader(number+1),self.z)))
        self.tar_pc = np.transpose(np.hstack((reader(number),self.z)))
        # print(self.src_pc.shape)
        self.src_pc = self.filter(self.src_pc)
        self.tar_pc = self.filter(self.tar_pc)

    def process(self):
        self.transform_acc = self.icp.process(self.tar_pc,self.src_pc)
        # self.tar_pc = self.src_pc
        # print("Result : ", self.transform_acc)

    def filter(self, pc):
        del_lst = []
        for i in range(pc.shape[1]):
            if np.isinf(pc[:,i]).any() or np.isnan(pc[:,i]).any():
                del_lst.append(i)
        pc = np.delete(pc, del_lst, axis=1)
        # print("Their length :", pc.shape[1])
        return pc
    
    def visualizer(self, index):
        # plt.cla()
        self.x = self.transform_acc[0,2]
        self.y = self.transform_acc[1,2]
        self.theta += np.arctan2(self.transform_acc[0,1], self.transform_acc[0,0])
        self.thetas.append(self.theta)
        print("Theta : ", self.theta)
        plt.scatter(self.x,self.y,s=10)
        arr_len = 0.15
        self.alpha -= 0.75 / 180
        map_len = 0.5
        plt.xlim((-map_len, map_len))
        plt.ylim((-map_len, map_len))
        plt.arrow(self.x, self.y, arr_len*np.cos(self.theta), arr_len*np.sin(self.theta), width=0.01,fc='red',alpha=1)
        # if (matrix == 0).all():
        #     time.sleep(0.1)
        #     print("No completed data get in")
        #     # return [load_m]
        #     origin_im = plt.scatter(ori_matrix[:,0],ori_matrix[:,1],s=3)
        #     plt.xlim(-5,5)
        #     plt.ylim(-5,5)
        #     return [origin_im]
        # time.sleep(0.01)
        return 0

def main():
    ot = Odemtry()
    map_len = 0.5
    fig = plt.figure(1)
    plt.subplot(1,2,1)
    plt.title("LiDAR sensor")
    plt.xlabel("x/[m]")
    plt.ylabel("y/[m]")
    for i in range(180):
        ot.pc(i+1)
        ot.process()
        ot.visualizer(1)
        # anim = animation.FuncAnimation(fig, ot.visualizer, frames=200, interval=60, blit=True)
    plt.subplot(1,2,2)
    plt.plot(ot.thetas)
    plt.xlabel("Point Cloud order")
    plt.ylabel("Theta/[rad]")
    # plt.yticks(np.arange(-30, 180, 20) * np.pi / 180)
    plt.show()
if __name__ == "__main__":
    main()