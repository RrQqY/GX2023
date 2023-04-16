#ifndef __GX_SS_H
#define __GX_SS_H

#define acc  10

// 定义Esp32步进电机引脚
#define motor1EN    13     // 电机使能引脚
#define motor1STEP  12     // 电机脉冲引脚
#define motor1DIR   11     // 电机方向引脚

#define motor2EN    13
#define motor2STEP  10
#define motor2DIR   9

#define motor3EN    4
#define motor3STEP  5
#define motor3DIR   6 

#define motor4EN    13
#define motor4STEP  7
#define motor4DIR   8


//#include "SunConfig.h"
#include <FlexiTimer2.h>           // 定时中断库
#include "SunPID.h"
#include <stdlib.h>
#include <math.h>
#include <Wire.h>
#include "JY901.h"
#include "AccelStepper.h"          // 步进电机驱动库
#include "SoftwareSerial.h"        // 软串口通信库
#include <DFRobot_IICSerial.h>     // IIC转串口模块库
// #include <REG.h>
// #include <wit_c_sdk.h>

#include "utilities.h"
#include "move.h"
#include "imu.h"
#include "serial.h"

extern int read_gray();

#endif
