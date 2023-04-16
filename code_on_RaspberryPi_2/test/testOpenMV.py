#coding:utf-8

import time
import serial
import RPi.GPIO as GPIO

# 参数配置
SERVO_PORT_NAME =  "/dev/ttyAMA3"		# 串口号
SERVO_BAUDRATE  =  9600			    # 波特率

# 初始化串口
SERVO_uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
                        parity=serial.PARITY_NONE, stopbits=1,\
                        bytesize=8,timeout=0)

recv = ''

lightPin = 40
GPIO.setmode(GPIO.BOARD)        # BMC或者BOARD模式
GPIO.setup(lightPin, GPIO.OUT)

# GPIO.output(lightPin, GPIO.HIGH)        # 打开补光灯
# time.sleep(0.4)


recv = ''
seq_up = 0
seq_down = 0
seq_up_str = ''
seq_down_str = ''

timeStart = time.time()

start_flag = "WL"
time.sleep(0.2)
SERVO_uart.write(start_flag.encode('utf-8'))

while True:
    # 获得接收缓冲区字符
    count = SERVO_uart.inWaiting()
    if count != 0:
        recv = SERVO_uart.read(count)    # 树莓派串口接收数据
        if 'WL_' in recv:
            pos = recv.find('_')
            seq_up_str = recv[pos + 1 : pos + 4]
            seq_down_str = recv[pos + 4 : pos + 7]
            seq_up = int(seq_up_str)
            seq_down = int(seq_down_str)
            print('@ Get color sequence: ', seq_up, seq_down)
            break
        else:
            timeNow = time.time()
            if timeNow - timeStart > 1.5:
                print('@ Time 2 out')
                break

    # 清空接收缓冲区
    SERVO_uart.flushInput()
    # 必要的软件延时
    time.sleep(0.1)