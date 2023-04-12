#!/usr/bin/env python
# -*- coding:UTF-8 -*-
from __future__ import print_function
import  serial

if __name__ == '__main__':
        listdata = []
        lastangle = 0
        ser = serial.Serial('/dev/wheeltec_lidar', 230400)    # ubuntu，如果未修改串口别名，可通过 ll /dev 查看雷达具体端口再进行更改
        # ser = serial.Serial("COM5", 230400, timeout=5)     # window系统，需要先通过设备管理器确认串口COM号
        while True:
                 data = ser.read(3)                           # 读取3个字节数据
                 if ord(data[0]) == 0xA5 and ord(data[1]) == 0x5A and ord(data[2]) == 0x3A:      # 判断是否为数据帧头
                    data = ser.read(55)                       # 是数据帧头就读取整一帧，去掉帧头之后为55个字节

                    # for x in range(55):
                    #  print('%#.2x '%ord(data[x]),end="\t")
                    # print("\n")

                    listdata.insert(0, "转速（圈/每分钟）：")
                    listdata.insert(1, (ord(data[0])*256+ord(data[1]))*144/1000)     # 转速：高字节在前，低字节在后，复合后再转换成十进制

                    listdata.insert(2, "起始角度(度):")
                    listdata.insert(3, (ord(data[2])*256+ord(data[3]))/100.0)   # 原始角度为方便传输放大了100倍，这里要除回去
                    listdata.insert(4, "距离（mm）|光强 *16个点：")
                    j=5
                    for x in range(4, 50, 3):                                   # 2个字节的距离数据，1个信号强度数据，步长为3
                        listdata.insert(j, ord(data[x])*256+ord(data[x+1]))      # 距离
                        j += 1
                        listdata.insert(j, ord(data[x+2]))                       # 信号强度
                        j += 1

                    listdata.insert(37, "结束角度（度）:")
                    listdata.insert(38, (ord(data[52])*256+ord(data[53]))/100.0)

                    j = 39
                    
                    if lastangle-listdata[3] > 100:                  # 判断上一帧的起始角度与这一帧的角度差是否大于一定角度即为新的一圈
                       print("*******************************")
                    lastangle = listdata[3]                          # 将此帧角度赋值为上一帧，为下一次的判断做准备
                    for k in range(j):
                        print(listdata[k], end="\t")                 # 打印解析之后的数据
                    print("\n")



      


      





  
  




  
