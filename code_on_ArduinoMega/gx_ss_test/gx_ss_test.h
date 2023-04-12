#ifndef __GX_SS_H
#define __GX_SS_H

#include "SunConfig.h"
// #include <FlexiTimer2.h>    // 定时中断
#include <MsTimer2.h>
#include <Wire.h>
#include "JY901.h"
#include "AccelStepper.h"   // 步进电机驱动
// #include <VL53L0X.h>        // 激光测距模块
// #include <SoftwareSerial.h>    // 软串口通信

// MPU6050
#include "I2Cdev.h"                          //i2cdevlib/Arduino/I2Cdev/
#include "MPU6050_6Axis_MotionApps612.h"     //i2cdevlib/Arduino/MPU6050/

// 自己的库
#include "utilities.h"
#include "move.h"
#include "serial.h"
#include "imu.h"

#endif
