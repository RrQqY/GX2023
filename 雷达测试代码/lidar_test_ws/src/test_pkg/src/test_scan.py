#!/usr/bin/env python
# coding=utf-8

import rospy
from ldlidar.msg import STP
import serial


# -------- 与下位机Mega通信串口配置 --------
# 参数配置
Mega_PORT_NAME =  "/dev/ttyAMA2"		    # 串口号
Mega_BAUDRATE  =  115200			    # 波特率

# 初始化串口
Mega_uart = serial.Serial(port=Mega_PORT_NAME, baudrate=Mega_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)


def tof_callback_forward(tof_forward):
    y_dist = tof_forward.distance
    print(y_dist)
    Mega_uart.write(str(int(y_dist * 1000)) + '@')


def tof_callback_right(tof_right):
    x_dist = tof_right.distance
    print(x_dist)
    Mega_uart.write(str(int(x_dist * 1000)) + '@')


def listener():
    rospy.init_node('tof_listener', anonymous=False)
    rospy.Subscriber('laser4',  STP, tof_callback_forward)      # 前部ToF
    rospy.Subscriber('laser2',  STP, tof_callback_right)        # 右部ToF
    rospy.spin()


if __name__ == '__main__':
    listener()

