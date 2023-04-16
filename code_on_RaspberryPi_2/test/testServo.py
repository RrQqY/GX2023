#coding:utf-8

# 添加uservo.py的系统路径
from __future__ import absolute_import
import sys
sys.path.append(u"../../src")
# 导入依赖
import time
import struct
import serial
from uservo import UartServoManager

# 参数配置
# 角度定义
SERVO_PORT_NAME =  u'/dev/ttyUSB0'		# 舵机串口号
SERVO_BAUDRATE = 115200			        # 舵机的波特率
SERVO_ID_0 = 0					        # 舵机的ID号
SERVO_ID_1 = 1
SERVO_ID_2 = 2
SERVO_ID_3 = 3
SERVO_ID_5 = 5
SERVO_HAS_MTURN_FUNC = False	        # 舵机是否拥有多圈模式

# 初始化串口
uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
					 parity=serial.PARITY_NONE, stopbits=1,\
					 bytesize=8,timeout=0)
# 初始化舵机管理器
uservo = UartServoManager(uart, is_debug=True)

# print u"[单圈模式]设置舵机角度为90.0°"
# uservo.set_servo_angle(SERVO_ID, 90.0, interval=0) # 设置舵机角度 极速模式
# uservo.wait() # 等待舵机静止
# print u"-> {}".format(uservo.query_servo_angle(SERVO_ID))

uservo.set_servo_angle(SERVO_ID_0, 90.0, interval=500) # 设置舵机角度(指定周期 单位ms)
uservo.wait() # 等待舵机静止
# print u"-> {}".format(uservo.query_servo_angle(SERVO_ID))

# print u"[单圈模式]设置舵机角度为90.0°, 设置转速为200 °/s, 加速时间100ms, 减速时间100ms"
# uservo.set_servo_angle(SERVO_ID, 90.0, velocity=100.0, t_acc=self.acc, t_dec=self.dec) # 设置舵机角度(指定转速 单位°/s)
# uservo.wait() # 等待舵机静止
# print u"-> {}".format(uservo.query_servo_angle(SERVO_ID))

# print u"[单圈模式]设置舵机角度为-90.0°, 添加功率限制"
# uservo.set_servo_angle(SERVO_ID, -90.0, power=2000) # 设置舵机角度(指定功率 单位mW)
# uservo.wait() # 等待舵机静止
