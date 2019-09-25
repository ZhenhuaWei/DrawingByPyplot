#!/usr/bin/python
import os
import time
from matplotlib import pyplot


'''
https://www.runoob.com/w3cnote/matplotlib-tutorial.html
https://www.runoob.com/numpy/numpy-matplotlib.html
'''

max_data_len = 0        # 最长数据长度
data_files_cnt = 0      # 数据文件个数
data_arr_list = []      # 数据列表

data_line_arr_list = [] # 辅助直线


def get_file_name(user_dir):
    file_list = list()
    for root, dirs, files in os.walk(user_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
                file_list.append(os.path.join(root, file))
    return file_list


def get_file_data(file_name):
    data_str = []
    data = []

    fp = open(file_name, "r")
    lines = fp.readlines()#读取整个文件数据
    for line in lines: 
        row_list = line.strip('\n').replace(',', ' ').split()#去除两头的换行符，按空格分割
        data_str.extend(row_list)
    fp.close()

    data_len = len(data_str)
    for i in range(0,data_len):
        data.append(int(data_str[i]))

    data_arr_list.append(data)
    data_line_arr_list.append(min(data))
    data_line_arr_list.append(max(data))
    return data_len, data

def show_mulit_plot():
    slot = []               # x坐标时隙
    for x in range(0,max_data_len):
        slot.append(x)

    pyplot.figure(figsize=(18, 8), dpi=50)
    pyplot.grid()
    for i in range(0, data_files_cnt):
        if(len(data_arr_list[i]) != max_data_len):
            zero_list = [min(data_line_arr_list) for i in range(max_data_len- len(data_arr_list[i]))]
            data_arr_list[i].extend(zero_list)

        pyplot.plot(slot, data_arr_list[i], ".")

    #设置横坐标为year，纵坐标为population，标题为Population year correspondence
    # pyplot.xlabel('slot')
    # pyplot.ylabel('')
    pyplot.title('All Data')
    #设置纵坐标刻度
    pyplot.yticks(data_line_arr_list)
    #设置填充选项：参数分别对应横坐标，纵坐标，纵坐标填充起始值，填充颜色（可以有更多选项）
    # pyplot.fill_between(slot, data, 10, color = 'green')
    #显示图表
    pyplot.show()

def show_plot(data, file_name, results_info_folder):
    slot = []
    matplot_time_stamp = time.strftime("%Y-%m-%d %X")
    matplot_time_stamp = matplot_time_stamp.replace(" ", "-")
    matplot_time_stamp = matplot_time_stamp.replace(":", "-")
    
    pic = results_info_folder + "\\" + matplot_time_stamp + r".png"

    for x in range(0,len(data)):
        slot.append(x)

    pyplot.figure(figsize=(18, 8), dpi=50)
    pyplot.grid()
    pyplot.plot(slot, data, '.')
    pyplot.title("Path:"+file_name)
    pyplot.yticks([max(data),min(data)])
    pyplot.show(block=False)
    pyplot.savefig(pic)
    del slot, data

if __name__ == '__main__':

    time_stamp = time.strftime("%Y-%m-%d %X")
    time_stamp = time_stamp.replace(" ", "-")
    time_stamp = time_stamp.replace(":", "-")
    results_folder = r".\ada_dump"
    results_info_folder = r".\ada_dump\dump_data_log_" + time_stamp
    if not os.path.exists(results_folder):
        os.mkdir(results_folder)
    if not os.path.exists(results_info_folder):
        os.makedirs(results_info_folder)

    files_name_list = get_file_name("./")
    data_files_cnt = len(files_name_list)

    if(data_files_cnt != 0):
        for file in files_name_list:
            data_len, one_data = get_file_data(file)
            if data_len > max_data_len:
                max_data_len = data_len
            show_plot(one_data, file, results_info_folder)
        show_mulit_plot()
    else:
        print("请在文件同级目录下放置.txt文件！")
        raw_input(r"Pleasr <Enter> to Exit...")