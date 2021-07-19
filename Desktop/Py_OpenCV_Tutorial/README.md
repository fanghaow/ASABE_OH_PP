# 1. Python环境搭建
## 1.1 下载 Python
[Python官网下载链接](https://www.python.org/)
<!-- ![1](figs/Python_web.png) -->

## 1.2 下载 opencv-python
* Windows
    * 进入cmd,输入以下命令: `pip3 install opencv-python`
    * 可选 : `pip3 install numpy matplotlib`
* Mac / Linux
    * 进入终端(Terminal)，输入以下命令: `pip3 install opencv-python`
    * Linux还可以使用命令：`sudo apt install python3-numpy`
    * 可选 : `pip3 install numpy matplotlib`

## 1.3 强烈推荐下载 Visual Studio Code
[VScode官网下载链接](https://code.visualstudio.com/)

其他的编写程序的软件也可以，如：Pycharm、Anaconda等平台，Python自带的idle也可以使用

# 2. 学习OpenCV
## 2.1 第一个opencv程序 -> cat_show
下载文件至本地，进入examples目录，输入

```python3 cat_show.py```

正常情况下你将看到：
<!-- ![1](figs/cat_show.png) -->
<img src="figs/cv2_cat.png" style="zoom:25%">

## 2.2 识别基础1 -> `Numpy`

* (1)Numpy里的向量、矩阵都是ndarray对象
```python
# 使用numpy库之前，为了简便引用，给numpy取别名np
>>> import numpy as np
# 交互式命令行只需用导入一次numpy库
```
* (2)创建一个一维矩阵（向量）、二维数组
```python
>>> a = np.array([1,2,3])
>>> print(a)
[1,2,3]
>>> print(type(a))
<class 'numpy.ndarray'>
>>> a = np.array([[1,2,3],[4,5,6]])
>>> print(a)
[[1,2,3]
 [4,5,6]]
```
* (3)创建一个0、1或单位矩阵
```python
>>> a = np.ones([2,3])
>>> print(a)
[[1. 1. 1.]
 [1. 1. 1.]]
>>> a = np.zeros([2,3])
>>> print(a)
[[0. 0. 0.]
 [0. 0. 0.]]
>>> a = np.eye(2)
>>> print(a)
[[1. 0.]
 [0. 1.]]
```
* (4)从数组范围创建矩阵
```python
# ny.arange(start, stop, step, dtype)
>>> a = np.arange(5, 11, 1, dtype=int)
>>> print(a)
[5 6 7 8 9 10]
# np.linspace(start, stop, num=50, endpoint=True, retstep=False, dtype=None)
>>> a = np.linspace(1,10,10,dtype=int)
>>> print(a)
[ 1  2  3  4  5  6  7  8  9 10]
```
* (5)矩阵维度、大小、形状
```python
>>> print(a.shape)
(6,)
>>> print(a.size)
6
>>> print(a.ndim)
1
>>> b = a.reshape((2,3))
>>> print(b)
[[ 5  6  7]
 [ 8  9 10]]
>>> print(b.shape)
(2, 3)
>>> print(b.ndim)
2
```
* (6)矩阵切片、索引
```python
>>> a = np.reshape(np.arange(1,10,1),(3,3))
>>> print(a)
[[1 2 3]
 [4 5 6]
 [7 8 9]]
>>> print(a[1,1])
5
>>> print(a[:,1])
[2 5 8]
>>> print(a[...,1])
[2 5 8]
>>> row,col = [0,1,2],[0,1,2]
>>> print(a[row,col])
[1 5 9]
>>> print(a[1:])
[[4 5 6]
 [7 8 9]]
```
* *更多Numpy库用法，请学习参考以下网站
    * 1.[Numpy官网](https://numpy.org/doc/stable/reference/)
    * 2.[NumPy教程|菜鸟教程](https://www.runoob.com/numpy/numpy-tutorial.html)
    * 3.[CS231n Numpy教程](https://cs231n.github.io/python-numpy-tutorial/)

## 2.3 识别基础2 -> `opencv`
* (1)导入库
```python
import cv2
```
* (2)读写图片
```python
# Read -> cv2.imread(filename,flag)
img = cv2.imread('images/cat.jpg',0)
"""
flag options:
1 / cv2.IMREAD_COLOR : Loads a color image. Any transparency of image will be neglected. It is the default flag.
0 / cv2.IMREAD_GRAYSCALE : Loads image in grayscale mode
-1 / cv2.IMREAD_UNCHANGED : Loads image as such including alpha channel
"""
# Show -> cv2.imshow(winname,src)
cv2.imshow('cat',img)
cv2.waitKey(3000) # [ms]

# Write -> cv2.imwrite(filename,src)
img = np.mean(img,2)
cv2.imwrite('images/cat_gray.jpg',img) # 查看"images/"文件目录下，是否多了一只灰度猫
```
