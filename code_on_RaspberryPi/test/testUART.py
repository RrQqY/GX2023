#coding:utf-8

import time
import serial

# 参数配置
Mega_PORT_NAME =  "/dev/ttyS0"		# 串口号
Mega_BAUDRATE  =  115200			    # 波特率

# 初始化串口
Mega_uart = serial.Serial(port=Mega_PORT_NAME, baudrate=Mega_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)


def get_order():
    recv = ''

    # 获得接收缓冲区字符
    count = Mega_uart.inWaiting()
    if count != 0:
        # 读取内容
        recv = Mega_uart.read(count)  #树莓派串口接收数据
    # 清空接收缓冲区
    Mega_uart.flushInput()

    if recv == '1':
        order = 1
        print('@ Get order 1')
        time.sleep(0.01)
        return order
    elif recv == '2':
        order = 2
        print('@ Get order 2')
        time.sleep(0.01)
        return order
    elif recv == '3':
        order = 3
        print('@ Get order 3')
        time.sleep(0.01)
        return order
    elif recv == '4':
        order = 4
        print('@ Get order 4')
        time.sleep(0.01)
        return order
    elif recv == '5':
        order = 25
        print('@ Get order 5')
        time.sleep(0.01)
        return order
    elif recv == '6':
        order = 6
        print('@ Get order 6')
        time.sleep(0.01)
        return order
    elif recv == '7':
        order = 7
        print('@ Get order 7')
        time.sleep(0.01)
        return order


# 任务1:扫描二维码
def order1():
    print("@ Start order 1")

# 任务2:识别货架颜色
def order2():
    print("@ Start order 2")

# 任务3:抓取物块①
def order3():
    print("@ Start order 3")

# 任务4:放下物块②
def order4():
    print("@ Start order 4")

# 任务5:抓取物块③
def order5():
    print("@ Start order 5")

# 任务6:放下物块④
def order6():
    print("@ Start order 6")

# 任务7:抓取物块⑤
def order7():
    print("@ Start order 7")



while True:
    # 从下位机获取指令
    order = get_order()

    # 开始执行指令
    if order == 1:
        order1()
    elif order == 2:
        order2()
    elif order == 3:
        order3()
    elif order == 4:
        order4()
    elif order == 5:
        order5()
    elif order == 6:
        order6()
    elif order == 7:
        order7()

    # 必要的软件延时
    time.sleep(0.1)
