#ifndef __IMU_H
#define __IMU_H

#include "SunConfig.h"       // 包含配置库

#define turn_angle_comp 1.013  // 转向角度补偿系数，yaw = ypr[0] * 180 * turn_angle_comp / M_PI，越大转的越多

extern void imu_setup();       // IMU初始化
extern float get_yaw0();       // IMU获取yaw角数据
extern float get_yaw();        // IMU获取yaw角数据（用HWT101）
extern float get_yaw_pro_left(float yaw);    // IMU yaw角数据处理

#endif
