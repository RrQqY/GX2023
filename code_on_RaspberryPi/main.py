#coding:utf-8
from __future__ import absolute_import
import RPi.GPIO as GPIO
from uservo import UartServoManager
import time
import serial
import cv2
import numpy as np
import struct
import sys
import servoActions as sa
from camera import Camera

import smbus
from Adafruit_I2C import Adafruit_I2C
from SDL_PC_BM017CS import SDL_BM017

color_list = ['red', 'green', 'blue']

sys.path.append(u"../../src")      # 添加uservo.py的系统路径
GPIO.setwarnings(False)
GPIO.cleanup()

global target_1          # 上层抓取目标顺序
global target_2          # 下层抓取目标顺序

global turnCount          # 当前执行轮数


# 初始化所有串口
# -------- 与下位机Mega通信串口配置 --------
# 参数配置
Mega_PORT_NAME =  "/dev/ttyAMA4"		    # 串口号
Mega_BAUDRATE  =  9600			    # 波特率

# 初始化串口
Mega_uart = serial.Serial(port=Mega_PORT_NAME, baudrate=Mega_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

# -------- 与GM65模块通信串口配置 --------
# 参数配置
GM65_PORT_NAME =  "/dev/ttyAMA1"		# 串口号
GM65_BAUDRATE  = 9600			        # 波特率

# 初始化串口
GM65_uart = serial.Serial(port=GM65_PORT_NAME, baudrate=GM65_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

# -------- 与LCD屏通信串口配置 --------
# 参数配置
LCD_PORT_NAME =  "/dev/ttyAMA3"		# 串口号
LCD_BAUDRATE  =  115200			    # 波特率

# 初始化串口
LCD_uart = serial.Serial(port=LCD_PORT_NAME, baudrate=LCD_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

# -------- 与Maix通信串口配置 --------
# 参数配置
Maix_PORT_NAME =  "/dev/ttyAMA0"		    # 串口号
Maix_BAUDRATE  =  115200			    # 波特率

# 初始化串口
Maix_uart = serial.Serial(port=Maix_PORT_NAME, baudrate=Maix_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)



# 初始化舵机动作控制类
servo = sa.servoActions()

# 初始化摄像头动作类
cam = Camera()

# 初始化GPIO引脚
startPin = 17
GPIO.setmode(GPIO.BCM)        # BMC或者BOARD模式
GPIO.setup(startPin, GPIO.IN)

camPin = 26
GPIO.setmode(GPIO.BCM)        # BMC或者BOARD模式
GPIO.setup(camPin, GPIO.OUT)

lightPin = 23
GPIO.setmode(GPIO.BCM)        # BMC或者BOARD模式
GPIO.setup(lightPin, GPIO.OUT)

# # 初始化BM017颜色传感器
# bm017 = SDL_BM017(True)
# bm017.setIntegrationTimeAndGain(0x00, 0x03)


def lightOn():
    """
    打开补光灯
    """
    GPIO.output(lightPin, GPIO.HIGH)

def lightOff():
    """
    关闭补光灯
    """
    GPIO.output(lightPin, GPIO.LOW)

def camOn():
    """
    打开摄像头
    """
    GPIO.output(camPin, GPIO.HIGH)

def camOff():
    """
    关闭摄像头
    """
    GPIO.output(camPin, GPIO.LOW)

def wait_start():
    """
    判断是否按下开始按钮
    """
    while True:
        if GPIO.input(startPin) == GPIO.HIGH:
            break


def LCD_print_target(target_up, target_down):
    """
    LCD屏打印二维码读取的抓取目标顺序
    """
    print_s = "CLR(0);SBC(3);DIR(1);DC48(5,5,'FIR_TAR:',15);DC48(240,5,'" + str(target_up) + "',15);DC48(5,60,'SEC_TAR:',15);DC48(240,60,'" + \
                str(target_down) + "',15);PL(0,120,320,120,15);\r\n"
    LCD_uart.write(print_s)


def send_move_order(dx, dy):
    """
    向Mega下位机发送移动指令
    """
    print('M' + str(int(dx * 1000) + 3000) + ',' + str(int(dy * 1000) + 3000) + '@')
    while True:
        Mega_uart.write('M')
        Mega_uart.flush()
        if Mega_uart.read().decode("ASCII") == 'o':
            print('Received mega received flag !!!')
            break
    # Mega_uart.write('M')
    # Mega_uart.flush()
    Mega_uart.write('M' + str(int(dx * 1000) + 3000) + ',' + str(int(dy * 1000) + 3000) + '@')
    Mega_uart.flush()


def send_rush_order(dx, dy):
    """
    向Mega下位机发送移动指定时间指令
    """
    print('R' + str(int(dx * 1000) + 3000) + ',' + str(int(dy * 1000) + 3000) + '@')
    while True:
        Mega_uart.write('R')
        Mega_uart.flush()
        if Mega_uart.read().decode("ASCII") == 'o':
            print('Received mega received flag !!!')
            break
    # Mega_uart.write('R')
    # Mega_uart.flush()
    Mega_uart.write('R' + str(int(dx * 1000) + 3000) + ',' + str(int(dy * 1000) + 3000) + '@')
    Mega_uart.flush()


def move(dx, dy):
    """
    移动指定距离
    """
    send_move_order(dx, dy)
    receive_move_end()        # 等待下位机发送移动结束标志"f"
    # time.sleep(0.2)


def rush(dx, dy):
    """
    移动指定时间
    """
    send_rush_order(dx, dy)
    receive_rush_end()        # 等待下位机发送移动结束标志"f"
    # time.sleep(0.2)


def move_start():
    """
    移动到起始位置
    """
    print('G' + '@')
    while True:
        Mega_uart.write('G')
        Mega_uart.flush()
        if Mega_uart.read().decode("ASCII") == 'o':
            print('Received mega received flag !!!')
            break
    receive_move_end()        # 等待下位机发送移动结束标志"f"
    # time.sleep(0.2)
    

def receive_move_end():
    """
    从Mega接收行走完成标志
    """
    while True:
        # if Mega_uart.inWaiting() > 0:
        if Mega_uart.read().decode("ASCII") == 'f':
            print('Received move finished flag !!!')
            return True
        

def receive_rush_end():
    """
    从Mega接收行走指定时间完成标志
    """
    while True:
        # if Mega_uart.inWaiting() > 0:
        if Mega_uart.read().decode("ASCII") == 'f':
            print('Received move finished flag !!!')
            return True


def receive_compensate_end():
    """
    从Mega接收补偿校正完成标志
    """
    # if Mega_uart.inWaiting() > 0:
    if Mega_uart.read().decode("ASCII") == 'e':
        print('Received compensate finished flag !!!')
        return True


def send_compensate_order(side):
    """
    向Mega下位机发送补偿校正指令
    """
    # print('b' + str(int(bias_x * 100) + 300) + ',' + str(int(bias_x * 100) + 300) + '@')
    # Mega_uart.write('b')
    # Mega_uart.flush()
    if side == 1:
        Mega_uart.write('a')
        Mega_uart.flush()
    elif side == 2:  
        Mega_uart.write('b')
        Mega_uart.flush() 


def send_change_order(flag):
    """
    向Mega下位机发送角度改变指令, 
    flag = 1, 记录开始前角度
    flag = 2, 记录结束后角度
    """
    print("X" + str(flag) + "@")
    # Mega_uart.write('b')
    # Mega_uart.flush()
    while True:
        Mega_uart.write('X')
        Mega_uart.flush()
        if Mega_uart.read().decode("ASCII") == 'o':
            print(Mega_uart.read().decode("ASCII"))
            break
    
    Mega_uart.write("X" + str(flag) + "@")
    Mega_uart.flush()


def send_bias(bias_x, bias_y):
    """
    向Mega下位机发送偏差值
    """
    # print('b' + str(int(bias_x * 100) + 300) + ',' + str(int(bias_x * 100) + 300) + '@')
    # Mega_uart.write('b')
    # Mega_uart.flush()
    Mega_uart.write('c' + str(int(bias_x * 1000) + 3000) + ',' + str(int(bias_y * 1000) + 3000) + '@')
    Mega_uart.flush()


def compensate(side):
    """
    在靶标前补偿校正 (1: 上侧靶标, 2: 左侧靶标(精确), 3: 左侧靶标(粗标))
    """
    if side == 1:
        # 发送补偿校正指令"a"
        send_compensate_order(side=1)
    elif side == 2 or side == 3:
        # 发送补偿校正指令"b"
        # print("yes")
        send_compensate_order(side=2)

    compensate_timeout_time = 6.4
    stime = time.time()

    while cam.cap.isOpened():
        ret, frame = cam.cap.read()
        rtime = time.time()
        if rtime - stime > compensate_timeout_time:
            print("time out")
            break

        if frame is not None:
            # 获取色块位置和颜色
            # binary, pos, color = cam.get_obj_color(frame)
            # print("pos, color: ", pos, color)
            # 获取靶标中心位置偏差
            x_bias, y_bias = cam.get_target_bias_circle(frame, side)
            
            # print("x_bias, y_bias: ", x_bias, y_bias, "time: ", etime-stime)

            # y轴矫正偏差 (让靶标出现在画面偏上方的位置) 
            y_bias = y_bias - 0.11     # 0.12

            # 向下位机发送偏差值
            send_bias(x_bias, y_bias)

            # 如果下位机发回已补偿结束标志"e", 则结束补偿
            if receive_compensate_end() == True:
                print("-------- compensate end --------")
                break

            # 结果显示
            # cv2.imshow("frame", frame)
            # cv2.imshow('binary', binary)
            cv2.waitKey(1)
  

# def get_obj_color_sensor():
#     """
#     通过颜色传感器获取当前物块颜色 (最优距离1cm)
#     """
#     bm017.getColors()

#     if bm017.red_color >= bm017.green_color and bm017.red_color >= bm017.blue_color:
#         obj_color = "r"
#     elif bm017.green_color >= bm017.red_color and bm017.green_color >= bm017.blue_color:
#         obj_color = "g"
#     elif bm017.blue_color >= bm017.red_color and bm017.blue_color >= bm017.green_color:
#         obj_color = "b"
    
#     print("obj_color= " + obj_color)
#     return obj_color
    

def get_obj_color_maix():
    """
    通过Maix开发板串口获取当前物块颜色
    """
    data = ''
    obj_color_list = []

    while True:
        data = Maix_uart.readline().decode("ASCII")
        if len(data) > 0:
            # print("data: ", data)
            if data[1] == 'r':
                obj_color_list.append("r")
                # print("obj_color= " + obj_color)

            elif data[1] == 'g':
                obj_color_list.append("g")
                # print("obj_color= " + obj_color)

            elif data[1] == 'b':
                obj_color_list.append("b")
                # print("obj_color= " + obj_color)

            else:
                obj_color_list.append("n")
                # print("obj_color= " + obj_color)

        # print("color_scaned: ", obj_color_list)
        if len(obj_color_list) >= 3:
            if (obj_color_list[0] == obj_color_list[1] == obj_color_list[2]) and (obj_color_list[0] != "n"):
                obj_color = obj_color_list[0]
                # print("obj_color= " + obj_color)
                obj_color_list = []
                return obj_color
            else :
                obj_color_list = []
                return 'n'



def order1():
    """
    任务1: 扫描二维码, 获取抓取第一、二轮物块抓取顺序
    """
    print("@ Start order 1")

    start = '7e000801000201abcd'
    start_hex = start.decode('hex')
    recv = ''
    target_1 = 0
    target_2 = 0
    target_1_str = ''
    target_2_str = ''

    timeStart = time.time()

    while True:
        # 发送拍摄开始数据段
        GM65_uart.write(start_hex)
        # 获得接收缓冲区字符
        count = GM65_uart.inWaiting()
        if count != 0:
            recv = GM65_uart.read(count)       # 树莓派串口接收数据
        if '+' in recv:
            pos = recv.find('+')
            target_1_str = recv[pos - 3 : pos]
            target_2_str = recv[pos + 1 : pos + 4]
            target_1 = int(target_1_str)
            target_2 = int(target_2_str)
            print('@ Get target: ', target_1, target_2)
            break;
        else :
            timeNow = time.time()
            if timeNow - timeStart > 2:
                print('@ Time 1 out')
                break;
        
        # 清空接收缓冲区
        GM65_uart.flushInput()
        # 必要的软件延时
        time.sleep(0.1)

    LCD_print_target(target_1, target_2)

    # target_1_list = [color_list[int(i)] for i in list(str(target_1))]
    # target_2_list = [color_list[int(i)] for i in list(str(target_2))]

    return target_1, target_2


def order2(target):
    """
    任务2: 按target顺序识别转台物块颜色, 并抓取到指定仓库中
    """
    print("@ Start order 2")
    servo.orient_to(servo.rightside_angle)        # 云台转动至上方

    # # 向Maix发送开始标志"s"
    # Maix_uart.write('s\n'.encode('ASCII'))
    # Maix_uart.flush()
    # while True:
    #     order = Maix_uart.readline()
    #     if len(order) > 0:
    #         if order[0] == 'o':
    #             break
    camOn()
    time.sleep(0.2)

    # lightOn()         # 打开补光灯
    color_target_list = []
    color_list = ['r', 'g', 'b']

    for i in range(3):
        color_target_list.append(color_list[int(str(target)[i]) - 1])

    # 等待直到检测值为'n'
    while True:
        color = get_obj_color_maix()
        if (color == 'r') or (color == 'g') or (color == 'b'):
            print("skip first color!!!!!!!!!")
            time.sleep(1)
            break
    
    Maix_uart.read_all()
    time.sleep(0.2)

    target_i = 0
    for color_target in color_target_list:
        # 仓库转动至目标位置
        servo.depo_to(color_target)
        # print("@ Turn to target: ", color_target)
        while True:
            color = get_obj_color_maix()
            if color == color_target:
                print("@ Get target color: ", color)
                # time.sleep(0.3)

                # 执行抓取
                servo.get_pla1()                          # 抓取物块①
                target_i += 1
                time.sleep(0.2)

                # servo.scan()
                # time.sleep(0.8)

                break
        
        # if target_i == 3:
        #     servo.grasp_open()
        #     servo.depo_up()

        if target_i == 3:
            servo.grasp_open()
            servo.depo_up()
            break
        else:
            servo.scan()
            time.sleep(1.8)
            print("scan again")

            # # 向Maix发送结束标志"e"
            # Maix_uart.write('e\n'.encode('ASCII'))
            # Maix_uart.flush()
            # while True:
            #     order = Maix_uart.readline()
            #     if len(order) > 0:
            #         if order[0] == 'o':
            #             break

    
            # break
    camOff()
    time.sleep(0.2)
        # else:
        #     servo.scan()
        #     time.sleep(0.8)

    # lightOff()        # 关闭补光灯


def order3(target):
    """
    任务3: 放下物块② (场地上方) 位置
    """
    print("@ Start order 3")
    servo.orient_to(servo.forward_angle)        # 云台转动至上方
    seq_i = 0
    for i in str(target):
        if int(i) == 1:
            delay_time = servo.depo_to('r')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla2(3)
        if int(i) == 2:
            delay_time = servo.depo_to('g')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla2(2)
        if int(i) == 3:
            delay_time = servo.depo_to('b')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla2(1)
    

def order4(target):
    """
    任务4: 抓取物块③ (场地上方) 位置
    """
    print("@ Start order 4")
    servo.orient_to(servo.forward_angle)        # 云台转动至上方

    seq_i = 0
    for i in str(target):
        if int(i) == 1:
            delay_time = servo.depo_to('r')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.get_pla2(3)
        if int(i) == 2:
            delay_time = servo.depo_to('g')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.get_pla2(2)
        if int(i) == 3:
            delay_time = servo.depo_to('b')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.get_pla2(1)
        
        servo.get_pla2(i)


def order5(target):
    """
    任务5: 放下物块④ (场地左侧) 下层位置
    """
    print("@ Start order 5")
    servo.orient_to(servo.leftside_angle)        # 云台转动至左侧

    seq_i = 0
    for i in str(target):
        if int(i) == 1:
            delay_time = servo.depo_to('r')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_down(3)
        if int(i) == 2:
            delay_time = servo.depo_to('g')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_down(2)
        if int(i) == 3:
            delay_time = servo.depo_to('b')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_down(1)
    

def order6(target):
    """
    任务6: 放下物块⑥ (场地左侧) 上层位置
    """
    print("@ Start order 6")
    servo.orient_to(servo.leftside_angle)        # 云台转动至左侧

    seq_i = 0
    for i in str(target):
        if int(i) == 1:
            delay_time = servo.depo_to('r')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_up(3)
        if int(i) == 2:
            delay_time = servo.depo_to('g')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_up(2)
        if int(i) == 3:
            delay_time = servo.depo_to('b')
            if seq_i == 0:
                time.sleep(delay_time + 0.2)
                seq_i += 1
            else:
                time.sleep(delay_time)
            servo.put_pla3_up(1)


# 场地坐标点参数
disc_x = 0.375           # 转盘左侧抓取点x坐标
disc_x_2 = 0.31           # 转盘左侧抓取点x坐标
disc_y = 1.765           # 转盘左侧抓取点y坐标
qrcode_x = 0.48         # 二维码识别点x坐标
qrcode_y = 0.64         # 二维码识别点y坐标
pla2_x = 1.175           # 粗加工区中间点x坐标
pla2_y = 2.04           # 粗加工区中间点y坐标
pla3_x = 1.89           # 精加工区中间点x坐标
pla3_x_back = 1.92      # 精加工区中间点返回时x坐标
pla3_y = 1.25           # 精加工区中间点y坐标
pla3_y_first = 1.41     # 精加工区中间点前一个点y坐标
back_y = 0.32            # 第一轮结束返回时y轴位置
end_x  = 2.25           # 结束区x轴位置
end_y  = 0.14           # 结束区y轴位置


def turn_1(target_1):
    """
    第一轮
    """
    move(disc_x, 0)
    time.sleep(0.2)

    move(0, disc_y)
    time.sleep(0.2)

    servo.scan()
    time.sleep(1)
    ### order2: 按target顺序识别转台物块颜色, 并抓取到指定仓库中
    order2(target_1)

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    servo.orient_to(servo.forward_angle)

    move(0, pla2_y)
    time.sleep(0.2)

    move(pla2_x, 0)
    time.sleep(0.2)

    # servo.compensate(pos=1)
    # time.sleep(1.4)

    # compensate(side=1)
    # time.sleep(0.2)

    servo.grasp_open()
    servo.depo_down()

    ### order3: 放下物块② (场地上方) 位置
    order3(target_1)
    time.sleep(0.5)

    ### order4: 抓取物块③ (场地上方) 位置
    order4(target_1)
    time.sleep(0.2)

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    servo.orient_to(servo.leftside_angle)

    move(pla3_x, 0)
    time.sleep(0.2)

    # # 向前撞墙矫正
    # rush(0, 2)
    # time.sleep(0.2)

    # # 下位机角度偏移矫正
    # time.sleep(0.2)
    # send_change_order(2)
    # time.sleep(0.4)

    # rush(0, -0.5)
    # time.sleep(0.2)

    move(0, pla3_y)
    time.sleep(0.2)

    servo.compensate(pos=1)
    time.sleep(1.4)

    compensate(side=2)
    time.sleep(0.2)

    servo.grasp_open()
    servo.depo_down()

    ### order5: 放置物块③ (场地左侧) 下层位置
    order5(target_1)
    time.sleep(0.2)

    servo.depo_up()

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    servo.orient_to(servo.rightside_angle)

    move(0, back_y)
    time.sleep(0.2)

    servo.servo_start()

    # move(disc_x + 0.03, 0)
    # time.sleep(0.2)
    move(0.2, 0)
    time.sleep(0.1)

    # 撞墙定位
    rush(-1.6, 0)
    time.sleep(0.5)

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.5)


def turn_2(target_2):
    """
    第二轮
    """
    move(disc_x_2, 0)
    time.sleep(0.2)

    move(0, disc_y)
    time.sleep(0.2)

    servo.scan()
    time.sleep(1)
    ### order2: 按target顺序识别转台物块颜色, 并抓取到指定仓库中
    order2(target_2)

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    servo.orient_to(servo.forward_angle)

    move(0, pla2_y)
    time.sleep(0.2)

    move(pla2_x, 0)
    time.sleep(0.2)

    # servo.compensate(pos=1)
    # time.sleep(1.4)

    # compensate(side=1)
    # time.sleep(0.2)

    servo.grasp_open()
    servo.depo_down()

    ### order3: 放下物块② (场地上方) 位置
    order3(target_2)
    time.sleep(0.5)

    ### order4: 抓取物块③ (场地上方) 位置
    order4(target_2)
    time.sleep(0.2)

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    servo.orient_to(servo.leftside_angle)

    move(pla3_x, 0)
    time.sleep(0.2)

    # # 向前撞墙矫正
    # rush(0, 2)
    # time.sleep(0.2)

    # # 下位机角度偏移矫正
    # time.sleep(0.2)
    # send_change_order(2)
    # time.sleep(0.4)

    # 第一次在第一个靶标校准
    move(0, pla3_y_first)
    time.sleep(0.2)

    servo.compensate(pos=1)
    time.sleep(1.4)

    compensate(side=3)     # 左侧位置带物块的补偿
    time.sleep(0.2)

    # 第二次在第二个靶标校准
    move(0, pla3_y)
    time.sleep(0.2)

    compensate(side=3)     # 左侧位置带物块的补偿
    time.sleep(0.2)

    servo.grasp_open()
    servo.depo_down()

    ### order6: 放置物块③ (场地左侧) 上层位置
    order6(target_2)
    time.sleep(0.2)

    servo.depo_up()

    # 下位机角度偏移矫正
    time.sleep(0.2)
    send_change_order(2)
    time.sleep(0.4)

    move(0, end_y + 0.3)
    time.sleep(0.2)

    rush(0, -2.2)
    time.sleep(0.2)

    servo.servo_start()
    servo.orient_to(servo.rightside_angle)

    rush(2.2, 0)
    time.sleep(0.2)

    # move(end_x, 0)
    # # time.sleep(0.2)


def main():
    turnCount = 1                           # 当前为第几回合

    # 关闭补光灯
    lightOff()

    # 机械臂进入初始位置
    servo.orient_to(servo.rightside_angle)
    servo.servo_start()
    servo.depo_to('r')

    # 等待一键启动
    wait_start()

    move(qrcode_x, 0)
    time.sleep(0.2)

    move(0, qrcode_y)
    time.sleep(0.2)

    ### order1: 识别二维码, 获取抓取顺序
    target_1, target_2 = order1()
    time.sleep(0.2)

    ##### 第一轮 #####
    turn_1(target_1)

    turnCount += 1

    ##### 第二轮 #####
    turn_2(target_2)


if __name__=='__main__':
    print("@ Start Game!!!")
    main() 

    ### 1. 测试转盘物块颜色识别和抓取
    # target_1 = 132
    # servo.scan()
    # time.sleep(1)
    # order2(target_1)

    ### 2. 测试粗加工区视觉补偿矫正
    # target_1 = 132
    # servo.orient_to(servo.forward_angle)
    # servo.compensate(pos=1)
    # time.sleep(1)
    # compensate(side=1)
    # time.sleep(1)

    ### 3. 测试粗加工区视抓取和放置
    # target_1 = 132
    # servo.orient_to(servo.forward_angle)
    # servo.grasp_open()
    # servo.depo_down()
    # time.sleep(1)
    # order3(target_1)
    # time.sleep(0.5)
    # order4(target_1)
    # time.sleep(0.2)
    
    ### 4. 测试读取MaixPy返回颜色
    # while True:
    #     color = get_obj_color_maix()
    #     print(color)