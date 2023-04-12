#coding:utf-8

import time
import serial

# 参数配置
GM65_PORT_NAME =  "/dev/ttyAMA1"		# 串口号
GM65_BAUDRATE  = 9600			        # 波特率

# 初始化串口
GM65_uart = serial.Serial(port=GM65_PORT_NAME, baudrate=GM65_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

start = '7e000801000201abcd'
start_hex = start.decode('hex')
recv = ''

while True:
    # 发送拍摄开始数据段
    GM65_uart.write(start_hex)
    # 获得接收缓冲区字符
    count = GM65_uart.inWaiting()
    if count != 0:
        # 读取内容并回显
        recv = GM65_uart.read(count)  #树莓派串口接收数据
    if '+' in recv:
        pos = recv.find('+')
        target_up = recv[pos-3 : pos]
        target_down = recv[pos+1 : pos+4]
        print(target_up, target_down)
        break;
    
    # 清空接收缓冲区
    GM65_uart.flushInput()
    # 必要的软件延时
    time.sleep(0.1)
