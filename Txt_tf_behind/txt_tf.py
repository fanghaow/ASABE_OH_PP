import sys
import numpy as np

f = open(r"/Users/fanghao_w/Desktop/vs_py_project/cpp接口/2.jpg.txt", "r") 
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

print('filename:',imgfile)
print('obj_num:',obj_num)
print('data:\n',data)
print('class_name:',class_name)