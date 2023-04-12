#ifndef __MOVE_H
#define __MOVE_H

// 电机负反馈PID参数
#define  Kp             12      // 8
#define  Ki             0.3    // 0.3
#define  Kd             0
// 陀螺仪矫正PID参数
#define  Kp_yaw         6.4    // 5.2
#define  Ki_yaw         0
#define  Kd_yaw         0
// 转弯PID参数
#define  Kp_yaw_turn    2
#define  Ki_yaw_turn    0
#define  Kd_yaw_turn    0

#define  YawPWM_MAX            60
#define  YawPWM_turn_MAX       8


extern float targetPulses[4];
extern float targetYawPulses;        // 用于控制车身的目标朝向角
extern int   left_turn_num;

extern void control();
extern void run_speed(int speed1, int speed2, int speed3, int speed4);
extern void set_speed(int speed1, int speed2, int speed3, int speed4);
extern void forward();

#endif
