#coding:utf-8

import numpy as np
import time
import serial
from uservo import UartServoManager

class servoActions():
    """
    舵机动作类, 动作方法如下：
    1、总线舵机:
      get_pla1: 抓取旋转货架 (场地下方) 
      put_pla2_pos: 放置货架② (场地右侧) 位置
      get_pla2_pos: 抓取货架② (场地右侧) 位置1
      put_pla3_down: 放置货架③ (场地上方) 下层
      put_pla3_up: 放置货架③ (场地上方) 上层
      depo_down: 货仓放入
      depo_up: 货仓取出         
      grasp_open: 爪子张开
      grasp_close: 爪子闭合
    2、PWM舵机
      orient_to: 云台转到指定角度
      depo_to: 货仓转到指定颜色位置

    舵机1: 正转向上
    舵机2: 正转向下
    舵机3: 正转向下
    舵机4: 正转向外
    """

    def __init__(self):
        self.row = 4        # 4个动作
        self.col = 5        # 5个舵机

        SERVO_PORT_NAME =  u'/dev/ttyUSB0'		# 舵机串口号
        SERVO_BAUDRATE = 115200			        # 舵机的波特率
        self.SERVO_base = 5					    # 舵机的ID号
        self.SERVO_ID_0 = 1					    # 舵机的ID号
        self.SERVO_ID_1 = 2
        self.SERVO_ID_2 = 3
        self.SERVO_ID_3 = 4
        # self.SERVO_ID_4 = 4
        self.SERVO_HAS_MTURN_FUNC = False	    # 舵机是否拥有多圈模式
        # 初始化串口
        self.servo_uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
                            parity=serial.PARITY_NONE, stopbits=1,\
                            bytesize=8,timeout=0)
        # 初始化舵机管理器
        self.uservo = UartServoManager(self.servo_uart, is_debug=True)

        self.decay = 1.1          # 整体速度缩放比例
        self.decay_time = 600      # 舵机减速时间
        
        # 舵机角度设定
        self.leftside_angle = -90 - 48       # 云台向右角度
        self.forward_angle = -47         # 云台向前角度
        self.back_angle = 90 + 43        # 云台向后角度
        self.rightside_angle = 44            # 云台向左角度

        self.grasp_open_angle = 65             # 爪子张开角度
        self.grasp_close_angle = 2            # 爪子闭合角度

        self.grasp_time = 0.5

        self.depo_to_pre = 'r'

        self.acc = 200
        self.dec = 600

        # -------- 与舵机驱动板通信串口配置 --------
        # 参数配置
        SERVO_PORT_NAME =  "/dev/ttyAMA2"		# 串口号
        SERVO_BAUDRATE  =  9600			        # 波特率
        # 初始化串口
        self.pwm_servo_uart = serial.Serial(port=SERVO_PORT_NAME, baudrate=SERVO_BAUDRATE,\
                                parity=serial.PARITY_NONE, stopbits=1,\
                                bytesize=8,timeout=0)


    # -------- 与货架相关的动作 --------
    def servo_start(self):
        """
        进入开始前机械臂位置
        """
        start = [[0 for i in range(5)] for j in range(1)]             
        start = [[50, -85, -40, self.grasp_close_angle]]
    
        self.uservo.set_servo_angle(self.SERVO_ID_0, start[0][0],velocity=150.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, start[0][1],velocity=100.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, start[0][2],velocity=100.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_3, start[0][3],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
        # self.uservo.wait()
        time.sleep(0.1)


    def get_pla1(self):
        """
        抓取转盘
        """
        # 抓取货架① (场地下方) 上层
        pla1_get = [[0 for i in range(5)] for j in range(4)]      # 抓取货架①
        pla1_get = [[62, 84, -26, self.grasp_open_angle]]         # 下去

        self.uservo.set_servo_angle(self.SERVO_ID_0, pla1_get[0][0],velocity=175.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, pla1_get[0][1],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, pla1_get[0][2],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_3, pla1_get[0][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        time.sleep(0.8 / self.decay)

        self.grasp_close()
        time.sleep(self.grasp_time / self.decay)

        self.depo_up()
        time.sleep(1.4 / self.decay)

        # self.depo_down()
        # time.sleep(0.2 / self.decay)

        self.grasp_open()
        time.sleep(self.grasp_time / self.decay)

        # self.depo_up()
        # time.sleep(0.2 / self.decay)

    
    def put_pla1(self):
        """
        放置转盘
        """
        # 抓取货架① (场地下方) 上层
        pla1_get = [[0 for i in range(5)] for j in range(4)]      # 抓取货架①
        pla1_get = [[67, 86, -28, self.grasp_close_angle]]        # 抓
        
        self.depo_down()
        time.sleep(2 / self.decay)

        self.grasp_close()
        time.sleep(self.grasp_time / self.decay)

        self.depo_down()
        time.sleep(0.2 / self.decay)

        self.uservo.set_servo_angle(self.SERVO_ID_0, pla1_get[0][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, pla1_get[0][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, pla1_get[0][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_3, pla1_get[0][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        time.sleep(1.5 / self.decay)

        self.grasp_open()
        time.sleep(self.grasp_time / self.decay)



    def put_pla2(self, pos):
        """
        放置货架② (场地右侧) 
        """
        # 放置货架② (场地右侧) 
        middle_angle = self.forward_angle
        left_angle = self.forward_angle - 28
        right_angle = self.forward_angle + 26

        depo_up =  [[-8, -120, -60]]

        pla2_pos1_put = [[left_angle, 45, 98, -58, self.grasp_close_angle],
                        [left_angle, 5, 70, -62, self.grasp_close_angle],       # 放下
                        [left_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回
        
        pla2_pos2_put = [[middle_angle, 50, 120, -70, self.grasp_close_angle],
                        [middle_angle, 10, 92, -88, self.grasp_close_angle],       # 放下
                        [middle_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回
        
        pla2_pos3_put = [[right_angle, 45, 98, -58, self.grasp_close_angle],
                        [right_angle, 5, 70, -62, self.grasp_close_angle],       # 放下
                        [right_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_down()
            self.orient_to(left_angle)
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_ID_0, depo_up[0][0],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, depo_up[0][1],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, depo_up[0][2],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_put[0][0],velocity=110.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_put[0][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_put[0][2],velocity=230.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_put[0][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_put[0][4],velocity=130.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(1 / self.decay)

            # self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_put[0][0],velocity=220.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_put[0][1],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_put[0][2],velocity=460.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_put[0][3],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_put[0][4],velocity=260.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # time.sleep(0.5 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.forward_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)

        
        ### 位置2
        elif pos == 2:
            self.depo_down()
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_ID_0, depo_up[0][0],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, depo_up[0][1],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, depo_up[0][2],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_put[0][0],velocity=110.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_put[0][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_put[0][2],velocity=230.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_put[0][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_put[0][4],velocity=130.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(1 / self.decay)

            # self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_put[0][0],velocity=220.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_put[0][1],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_put[0][2],velocity=460.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_put[0][3],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_put[0][4],velocity=260.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # time.sleep(0.5 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.forward_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_down()
            self.orient_to(right_angle)
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_ID_0, depo_up[0][0],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, depo_up[0][1],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, depo_up[0][2],velocity=50.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_put[0][0],velocity=110.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_put[0][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_put[0][2],velocity=230.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_put[0][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_put[0][4],velocity=130.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(1 / self.decay)

            # self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_put[0][0],velocity=220.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_put[0][1],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_put[0][2],velocity=460.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_put[0][3],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_put[0][4],velocity=260.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            # time.sleep(0.5 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.forward_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)
        

    def get_pla2(self, pos):
        """
        抓取货架② (场地右侧) 位置
        """
        # 抓取货架② (场地右侧) 
        middle_angle = self.forward_angle
        left_angle = self.forward_angle - 28
        right_angle = self.forward_angle + 26

        # pla2_pos1_get = [[left_angle, 45, 113, -30, self.grasp_open_angle],
        #                 [left_angle, 5, 70, -71, self.grasp_open_angle],       # 放下
        #                 [left_angle, 90, 135, -65, self.grasp_close_angle]]        # 缩回
        
        # pla2_pos2_get = [[middle_angle, 50, 135, -30, self.grasp_open_angle],
        #                 [middle_angle, 10, 92, -88, self.grasp_open_angle],       # 放下
        #                 [middle_angle, 90, 135, -65, self.grasp_close_angle]]        # 缩回
        
        # pla2_pos3_get = [[right_angle, 45, 113, -30, self.grasp_open_angle],
        #                 [right_angle, 5, 70, -71, self.grasp_open_angle],       # 放下
        #                 [right_angle, 90, 135, -65, self.grasp_close_angle]]        # 缩回
        
        pla2_pos1_get = [[left_angle, 45, 125, -35, self.grasp_open_angle],
                            [left_angle, 10, 81, -76, self.grasp_open_angle],       # 放下
                            [left_angle, 90, 120, -65, self.grasp_close_angle]]        # 缩回
        
        pla2_pos2_get = [[middle_angle, 70, 135, 0, self.grasp_open_angle],
                            [middle_angle, 12, 100, -96, self.grasp_open_angle],       # 放下
                            [middle_angle, 90, 135, -90, self.grasp_close_angle]]        # 缩回
        
        pla2_pos3_get = [[right_angle, 45, 125, -35, self.grasp_open_angle],
                            [right_angle, 10, 81, -76, self.grasp_open_angle],       # 放下
                            [right_angle, 90, 120, -65, self.grasp_close_angle]]        # 缩回
        
        ### 位置1
        if pos == 1:
            self.depo_up()
            self.orient_to(left_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(1 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos1_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos1_get[2][1],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos1_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos1_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos1_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.orient_to(self.forward_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置2
        elif pos == 2:
            self.grasp_open()
            self.depo_up()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_get[0][1],velocity=280.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_get[0][2],velocity=420.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_get[0][3],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_get[1][2],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_get[1][3],velocity=400.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos2_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos2_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos2_get[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos2_get[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos2_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_up()
            self.orient_to(right_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla2_pos3_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla2_pos3_get[2][1],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla2_pos3_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla2_pos3_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla2_pos3_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.orient_to(self.forward_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        

    def put_pla3_down(self, pos):
        """
        放置货架③ (场地上方) 下层位置1
        """
        # 放置货架③ (场地上方) 下层
        middle_angle = self.leftside_angle
        left_angle = self.leftside_angle - 27
        right_angle = self.leftside_angle + 27

        pla3_pos1_down_put = [[left_angle, 45, 98, -58, self.grasp_close_angle],
                        [left_angle, 5, 70, -60, self.grasp_close_angle],       # 放下
                        [left_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回
        
        pla3_pos2_down_put = [[middle_angle, 50, 120, -70, self.grasp_close_angle],
                        [middle_angle, 10, 92, -88, self.grasp_close_angle],       # 放下
                        [middle_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回
        
        pla3_pos3_down_put = [[right_angle, 45, 98, -58, self.grasp_close_angle],
                        [right_angle, 5, 70, -60, self.grasp_close_angle],       # 放下
                        [right_angle, 90, 135, -65, self.grasp_open_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_down()
            self.orient_to(left_angle)
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)

        
        ### 位置2
        elif pos == 2:
            self.depo_down()
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_down()
            self.orient_to(right_angle)
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_put[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_put[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)


    # 放置货架③ (场地上方) 上层
    def put_pla3_up(self, pos):
        """
        放置货架③ (场地上方) 上层位置1
        """
        middle_angle = self.leftside_angle
        left_angle = self.leftside_angle - 27
        right_angle = self.leftside_angle + 27

        pla3_pos1_up_put = [[left_angle, 45, 98, -58, self.grasp_close_angle],
                        [left_angle, 52, 100, -53, self.grasp_close_angle],       # 放下
                        [left_angle, 100, 135, -120, self.grasp_open_angle]]        # 缩回
        
        pla3_pos2_up_put = [[middle_angle, 50, 120, -70, self.grasp_close_angle],
                        [middle_angle, 64, 123, -65, self.grasp_close_angle],       # 放下
                        [middle_angle, 100, 123, -130, self.grasp_open_angle]]        # 缩回
        
        pla3_pos3_up_put = [[right_angle, 45, 98, -58, self.grasp_close_angle],
                        [right_angle, 52, 100, -53, self.grasp_close_angle],       # 放下
                        [right_angle, 100, 135, -120, self.grasp_open_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_down()
            self.orient_to(left_angle)
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_put[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_put[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)

        
        ### 位置2
        elif pos == 2:
            self.depo_down()
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_put[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_put[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_down()
            self.orient_to(right_angle)
            time.sleep(0.4 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.depo_up()
            time.sleep(0.2 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_put[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_put[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_put[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_put[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_put[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_put[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_put[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_put[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_put[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_put[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.7 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_put[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_put[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_put[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_put[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_put[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_down()
            time.sleep(0.4 / self.decay)


    # 抓取货架③ (场地上方) 下层
    def get_pla3_down(self, pos):
        """
        放置货架③ (场地上方) 上层位置1
        """
        middle_angle = self.leftside_angle
        left_angle = self.leftside_angle - 27
        right_angle = self.leftside_angle + 27

        pla3_pos1_down_get = [[left_angle, 45, 110, -45, self.grasp_open_angle],
                            [left_angle, 8, 70, -65, self.grasp_open_angle],       # 放下
                            [left_angle, 90, 135, -65, self.grasp_close_angle]]        # 缩回
        
        pla3_pos2_down_get = [[middle_angle, 80, 135, -10, self.grasp_open_angle],
                            [middle_angle, 10, 92, -88, self.grasp_open_angle],       # 放下
                            [middle_angle, 90, 135, -90, self.grasp_close_angle]]        # 缩回
        
        pla3_pos3_down_get = [[right_angle, 45, 110, -45, self.grasp_open_angle],
                            [right_angle, 8, 70, -65, self.grasp_open_angle],       # 放下
                            [right_angle, 90, 135, -65, self.grasp_close_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_up()
            self.orient_to(left_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_down_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_down_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_down_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_down_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_down_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

        
        ### 位置2
        elif pos == 2:
            self.depo_up()
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_get[0][1],velocity=280.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_get[0][2],velocity=420.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_get[0][3],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_get[1][2],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_down_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_down_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_down_get[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_down_get[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_down_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_up()
            self.orient_to(right_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_down_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_down_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_down_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_down_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_down_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)


    # 抓取货架③ (场地上方) 上层
    def get_pla3_up(self, pos):
        """
        放置货架③ (场地上方) 上层位置1
        """
        middle_angle = self.leftside_angle
        left_angle = self.leftside_angle - 27
        right_angle = self.leftside_angle + 27

        pla3_pos1_up_get = [[left_angle, 80, 135, -58, self.grasp_open_angle],
                        [left_angle, 45, 88, -51, self.grasp_open_angle],       # 放下
                        [left_angle, 100, 135, -120, self.grasp_close_angle]]        # 缩回
        
        pla3_pos2_up_get = [[middle_angle, 90, 135, -5, self.grasp_open_angle],
                        [middle_angle, 57, 111, -63, self.grasp_open_angle],       # 放下
                        [middle_angle, 100, 123, -130, self.grasp_close_angle]]        # 缩回
        
        pla3_pos3_up_get = [[right_angle, 80, 135, -58, self.grasp_open_angle],
                        [right_angle, 45, 88, -51, self.grasp_open_angle],       # 放下
                        [right_angle, 100, 135, -120, self.grasp_close_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_up()
            self.orient_to(left_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_up_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_up_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_up_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_up_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_up_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.8 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置2
        elif pos == 2:
            self.depo_up()
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_get[0][1],velocity=280.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_get[0][2],velocity=420.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_get[0][3],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_get[1][2],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_up_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_up_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_up_get[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_up_get[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_up_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_up()
            self.orient_to(right_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_get[1][2],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_up_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_up_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_up_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_up_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_up_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(1.2 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)


    # 抓取货架③ (场地上方) 后方上层
    def get_pla3_back(self, pos):
        """
        放置货架③ (场地上方) 后方上层位置
        """
        middle_angle = self.leftside_angle
        left_angle = self.leftside_angle - 27
        right_angle = self.leftside_angle + 27

        pla3_pos1_back_get = [[left_angle, 65, 95, -40, self.grasp_open_angle],
                            [left_angle, 5, 20, -20, self.grasp_open_angle],       # 放下
                            [left_angle, 35, -40, -165, self.grasp_close_angle]]        # 缩回
        
        pla3_pos2_back_get = [[middle_angle, 65, 95, -40, self.grasp_open_angle],
                            [middle_angle, 8, 25, -20, self.grasp_open_angle],       # 放下
                            [middle_angle, 35, -40, -65, self.grasp_close_angle]]        # 缩回
        
        pla3_pos3_back_get = [[right_angle, 65, 95, -40, self.grasp_open_angle],
                            [right_angle, 5, 20, -20, self.grasp_open_angle],       # 放下
                            [right_angle, 35, -40, -165, self.grasp_close_angle]]        # 缩回

        ### 位置1
        if pos == 1:
            self.depo_up()
            self.orient_to(left_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_back_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_back_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_back_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_back_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_back_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_back_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_back_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_back_get[1][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_back_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_back_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos1_back_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos1_back_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos1_back_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos1_back_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos1_back_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.5 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(0.9 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置2
        elif pos == 2:
            self.depo_up()
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_back_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_back_get[0][1],velocity=280.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_back_get[0][2],velocity=420.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_back_get[0][3],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_back_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_back_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_back_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_back_get[1][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_back_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_back_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos2_back_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos2_back_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos2_back_get[2][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos2_back_get[2][3],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos2_back_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.5 / self.decay)

            self.depo_up()
            time.sleep(1 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)
        
        ### 位置3
        elif pos == 3:
            self.depo_up()
            self.orient_to(right_angle)
            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_back_get[0][0],velocity=170.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_back_get[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_back_get[0][2],velocity=350.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_back_get[0][3],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_back_get[0][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.9 / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_back_get[1][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_back_get[1][1],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_back_get[1][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_back_get[1][3],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_back_get[1][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.6 / self.decay)

            self.grasp_close()
            time.sleep(self.grasp_time / self.decay)

            self.uservo.set_servo_angle(self.SERVO_base, pla3_pos3_back_get[2][0],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_0, pla3_pos3_back_get[2][1],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, pla3_pos3_back_get[2][2],velocity=250.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, pla3_pos3_back_get[2][3],velocity=100.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, pla3_pos3_back_get[2][4],velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
            time.sleep(0.5 / self.decay)

            self.orient_to(self.leftside_angle)
            self.depo_up()
            time.sleep(0.9 / self.decay)

            self.grasp_open()
            time.sleep(self.grasp_time / self.decay)


    def compensate(self, pos=1):
        """
        进入相机矫正位置 (pos=1表示场地上方加工区矫正, pos=2表示场地左方加工区矫正)
        """
        if pos == 1:
            compensate = [[0 for i in range(5)] for j in range(1)]             
            compensate = [[50, 44, 0, self.grasp_open_angle]]

            self.uservo.set_servo_angle(self.SERVO_ID_0, compensate[0][0],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, compensate[0][1],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, compensate[0][2],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, compensate[0][3],velocity=200.0, t_acc=self.acc, t_dec=self.dec)

        elif pos == 2:
            compensate = [[0 for i in range(5)] for j in range(1)]             
            compensate = [[85, 82, 0, self.grasp_open_angle]]

            self.uservo.set_servo_angle(self.SERVO_ID_0, compensate[0][0],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_1, compensate[0][1],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_2, compensate[0][2],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
            self.uservo.set_servo_angle(self.SERVO_ID_3, compensate[0][3],velocity=200.0, t_acc=self.acc, t_dec=self.dec)


    def scan(self):
        """
        进入相机颜色检测位置
        """
        scan_color = [[0 for i in range(5)] for j in range(1)]             
        scan_color = [[103, 95, 50, self.grasp_open_angle]]

        self.uservo.set_servo_angle(self.SERVO_ID_0, scan_color[0][0],velocity=100.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, scan_color[0][1],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, scan_color[0][2],velocity=200.0, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_3, scan_color[0][3],velocity=100.0, t_acc=self.acc, t_dec=self.dec)
    

    # -------- 与仓库相关的动作 --------
    def depo_down(self):
        """
        货仓放入
        """
        # 放入
        depo_down =  [[0 for i in range(5)] for j in range(4)]      # 放入左货仓
        depo_down =  [[-25, -135, -65]]
    
        self.uservo.set_servo_angle(self.SERVO_ID_0, depo_down[0][0],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, depo_down[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, depo_down[0][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)


    def depo_up(self):
        """
        货仓取出
        """
        # 取出
        depo_up = [[0 for i in range(5)] for j in range(4)]
        depo_up =  [[-8, -120, -60]]
        
        self.uservo.set_servo_angle(self.SERVO_ID_0, depo_up[0][0],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_1, depo_up[0][1],velocity=300.0 * self.decay, t_acc=self.acc, t_dec=self.dec)
        self.uservo.set_servo_angle(self.SERVO_ID_2, depo_up[0][2],velocity=150.0 * self.decay, t_acc=self.acc, t_dec=self.dec)


    def grasp_open(self):
        """
        爪子张开
        """
        self.uservo.set_servo_angle(self.SERVO_ID_3, self.grasp_open_angle,velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)


    def grasp_close(self):
        """
        爪子抓取
        """
        self.uservo.set_servo_angle(self.SERVO_ID_3, self.grasp_close_angle,velocity=200.0 * self.decay, t_acc=self.acc, t_dec=self.dec)



    def angle_to_order(self, num, angle):
        """
        角度转化为十六进制指令
        """
        if angle < 0:
            angle = angle + 360

        angle = int(angle / 300.0 * (2500 - 500) + 500)        # 将角度转化为PWM
        # 0xFF, 0x02, CH, DataL, DataH (CH：0x表示几号舵机；f4 01：500表示0°, c4 09：2500表示最大角度) 
        order = 'ff02' + '{:02x}'.format(num) + '{:04x}'.format(angle)[2:] + '{:04x}'.format(angle)[:2]
        return order


    def orient_to(self, target_angle):
        """
        云台转到指定角度
        """
        # if target_angle > 300:
        #     print("@@ angle out of range")
        #     return

        # turn_order = self.angle_to_order(2, target_angle)
        # self.pwm_servo_uart.write(turn_order.decode('hex'))
        print("turn to angle: ", target_angle)
        self.uservo.set_servo_angle(self.SERVO_base, target_angle, velocity=100.0, t_acc=self.acc, t_dec=self.dec)


    def depo_to(self, color):
        """
        货仓转到指定颜色位置
        """
        depo_order_red = self.angle_to_order(3, 0 + 10)          # 0度
        depo_order_green = self.angle_to_order(3, 120 + 10)      # 120度
        depo_order_blue = self.angle_to_order(3, 240 + 10)       # 240度

        if color == "r":
            self.pwm_servo_uart.write(depo_order_red.decode('hex'))
        elif color == "g":
            self.pwm_servo_uart.write(depo_order_green.decode('hex'))
        elif color == "b":
            self.pwm_servo_uart.write(depo_order_blue.decode('hex'))

        # 计算等待时间
        if self.depo_to_pre == 'r' and color == 'r':
            delay_time = 0.6 /  self.decay
        elif self.depo_to_pre == 'g' and color == 'g':
            delay_time = 0.6 /  self.decay
        elif self.depo_to_pre == 'b' and color == 'b':
            delay_time = 0.6 /  self.decay
        elif self.depo_to_pre == 'r' and color == 'g':
            delay_time = 0.8 /  self.decay
        elif self.depo_to_pre == 'r' and color == 'b':
            delay_time = 1.2 /  self.decay
        elif self.depo_to_pre == 'g' and color == 'r':
            delay_time = 0.8 /  self.decay
        elif self.depo_to_pre == 'g' and color == 'b':
            delay_time = 0.8 /  self.decay
        elif self.depo_to_pre == 'b' and color == 'r':
            delay_time = 1.2 /  self.decay
        elif self.depo_to_pre == 'b' and color == 'g':
            delay_time = 0.8 /  self.decay
        else:
            delay_time = 0.6 /  self.decay

        self.depo_to_pre = color

        print("delay time: ", delay_time)

        return delay_time
