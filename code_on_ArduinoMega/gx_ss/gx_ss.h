#ifndef __GX_SS_H
#define __GX_SS_H

#include "SunConfig.h"
#include <FlexiTimer2.h>    // 定时中断
#include <Wire.h>
#include "JY901.h"
#include "AccelStepper.h"   // 步进电机驱动

// MPU6050 测试例程 请先安装库 https://github.com/jrowberg/i2cdevlib
#include "I2Cdev.h"                          //i2cdevlib/Arduino/I2Cdev/
#include "MPU6050_6Axis_MotionApps612.h"     //i2cdevlib/Arduino/MPU6050/
// Arduino Wire library is required if I2Cdev I2CDEV_ARDUINO_WIRE implementation
// is used in I2Cdev.h

#include "move.h"
#include "gpio.h"
#include "imu.h"
#include "utilities.h"
#include "serial.h"

extern A4950MotorShield motors;

extern void prepare();      // 准备函数
extern void start();        // 开始函数
extern void turn1();        // 第一次出发
extern void turn2();        // 第二次出发

#endif
