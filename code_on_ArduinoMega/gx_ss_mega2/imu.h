#ifndef __IMU_H
#define __IMU_H

#define turn_angle_comp 1.013  // 转向角度补偿系数，yaw = ypr[0] * 180 * turn_angle_comp / M_PI，越大转的越多

extern double yaw_list[];

extern double yaw_start;
extern double yaw_end;
extern double yaw_bias;
// extern void imu_setup();       // IMU初始化
// extern double get_yaw0();       // IMU获取yaw角数据
extern double get_yaw(int origin_flag = 0);        // IMU获取yaw角数据（用HWT101）

#endif