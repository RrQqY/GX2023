#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from __future__ import print_function
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import serial

circle_data = []
circle_angle = []
circle_dist = []
circle_inten = []

flag = 0

if __name__ == '__main__':
    frame_data = []         # 读取一帧数据
    last_angle = 0

    # ser= serial.Serial('/dev/wheeltec_lidar', 230400)     # ubuntu，如果未修改串口别名，可通过 ll /dev 查看雷达具体端口再进行更改
    ser = serial.Serial("COM14", 230400, timeout=5)         # window系统，需要先通过设备管理器确认串口COM号

    while True:
        data = ser.read(3)                                             # 读取3个字节数据
        if data[0] == 0xA5 and data[1] == 0x5A and data[2] == 0x3A:    # 判断是否为数据帧头
            data = ser.read(55)                                        # 是数据帧头就读取整一帧，去掉帧头之后为55个字节

            # 转速（高字节在前，低字节在后，复合后再转换成十进制）
            frame_data.insert(0, "转速（圈/每分钟）：")
            speed = (data[0]*256+data[1])*144/1000                     
            frame_data.insert(1, speed)

            # 起始角度
            frame_data.insert(2, "start_angle:")
            start_angle = (data[2]*256+data[3])/100.0
            frame_data.insert(3, start_angle)            # 原始角度为方便传输放大了100倍，这里要除回去

            frame_data.insert(4, "距离（mm）|光强 *16个点：")
            j = 5
            for x in range(4, 50, 3):                              # 2个字节的距离数据，1个信号强度数据，步长为3
                dist = data[x]*256+data[x+1]
                frame_data.insert(j, dist)        # 距离
                j += 1
                
                inten = data[x+2]
                frame_data.insert(j, inten)       # 信号强度
                j += 1
                circle_inten.append(inten)

                if inten < 100:
                    circle_dist.append(0)
                else:
                    circle_dist.append(dist)

            # 结束角度
            frame_data.insert(37, "end_angle:")
            end_angle = (data[52]*256+data[53])/100.0
            frame_data.insert(38, end_angle)

            if start_angle - end_angle > 200:
                end_angle += 360

            for a in range(16):
                # angle = start_angle + a * 0.8
                # angle = start_angle + (end_angle - start_angle) * a / (16-1)
                # angle = end_angle + (start_angle - end_angle) * a / (16-1)
                angle = start_angle
                circle_angle.append(angle)

            # 判断上一帧的起始角度与这一帧的角度差是否大于一定角度即为新的一圈
            if last_angle - start_angle > 200:
                theta_list = circle_angle
                r_list = circle_dist

                c = plt.polar(theta_list, r_list, marker='.', ls='none')
                plt.show()

                circle_angle = []
                circle_dist = []
                circle_inten = []
                print("*******************************")
                flag += 1
            
            last_angle = start_angle                   # 将此帧角度赋值为上一帧，为下一次的判断做准备

            # for k in range():
            #     pass
            
            for k in range(39):
                print(frame_data[k], end="\t")         # 打印解析之后的数据
            print("\n")

            # print("@@@", average_angle, average_dist, average_inten)