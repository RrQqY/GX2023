#coding:utf-8

from __future__ import absolute_import
from uservo import UartServoManager
import time
import serial
import cv2
import numpy as np
import struct
import sys
import servoActions as sa
import RPi.GPIO as GPIO

sys.path.append(u"../../src")      # 添加uservo.py的系统路径

global target_up          # 上层抓取目标顺序
global target_down        # 下层抓取目标顺序

target_up = 123
target_down = 321

# -------- 与LCD屏通信串口配置 --------
# 参数配置
LCD_PORT_NAME =  "/dev/ttyAMA3"		# 串口号
LCD_BAUDRATE  =  115200			    # 波特率

# 初始化串口
LCD_uart = serial.Serial(port=LCD_PORT_NAME, baudrate=LCD_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

time.sleep(1)

# LCD_uart.write("DIR(1);\r\n")       # 设置为横屏显示
# LCD_uart.write("BL(0);\r\n")        # 设置亮度为最亮
# LCD_uart.write("CLR(0);\r\n")       # 清屏
# # LCD_uart.write("SBC(0);\r\n")
# LCD_uart.write("DC48(0,0,'嘿嘿嘿',15,1);\r\n")

# LCD_uart.write("CLR(0);SBC(3);DC48(0,48,'Uart 显示屏',15);\r\n")

def LCD_print(target_up, target_down):
    if target_up == 123 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 123:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'123',15);PL(0,120,320,120,15);\r\n")

    elif target_up == 123 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 132:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'132',15);PL(0,120,320,120,15);\r\n")

    elif target_up == 123 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 213:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'213',15);PL(0,120,320,120,15);\r\n")

    elif target_up == 123 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 231:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'231',15);PL(0,120,320,120,15);\r\n")

    elif target_up == 123 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 312:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'312',15);PL(0,120,320,120,15);\r\n")

    elif target_up == 123 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'123',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 132 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'132',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 213 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'213',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 231 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'231',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 312 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'312',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")
    elif target_up == 321 and target_down == 321:
        LCD_uart.write("CLR(0);SBC(3);DC48(5,5,'UP_TAR:',15);DC48(240,5,'321',15);DC48(5,60,'DOWN_TAR:',15);DC48(240,60,'321',15);PL(0,120,320,120,15);\r\n")


if __name__=='__main__':
    LCD_print(213,321)