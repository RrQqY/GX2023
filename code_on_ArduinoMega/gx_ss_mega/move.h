#ifndef __MOVE_H
#define __MOVE_H

// 电机速度全局变量
extern int speed1;
extern int speed2;
extern int speed3;
extern int speed4;

// 由dxdy累加的当前车身理论绝对位置
extern double x_pre;
extern double y_pre;

extern double targetDist_tof_x;
extern double targetDist_tof_y;

#define  read_tof_freq    1   // 读取ToF距离的频率

// 直走速度
#define  move_speed       3600
#define  move_speed_slow  2000

#define  run_delay_time  10    // 电机每次run时间


// 衡量距离目标点远近的位置阈值
#define  dist_threshold_far    0.15
#define  dist_threshold_close  0.00

#define  kp_speed  0.0002*0.85      // 轮子速度到车身速度的换算系数
// #define  kp_speed  0.00008      // 轮子速度到车身速度的换算系数


// 陀螺仪矫正PID参数
#define  Kp_yaw         800    // 5.2
#define  Ki_yaw         0.5      // 0.2
#define  Kd_yaw         0

// ToF矫正PID参数（直走）
#define  Kp_tof_y         20000    // 75000
#define  Ki_tof_y         0      // 0.2
#define  Kd_tof_y         0
// ToF矫正PID参数（平移）
#define  Kp_tof_x         80000    // 75000
#define  Ki_tof_x         0      // 0.2
#define  Kd_tof_x         0

#define  YawPWM_MAX     10000
#define  TofPWM_MAX     10000
#define  PWM_MIN        -1000
#define  PWM_MAX        1000

#define targetYawPulses 0        // 用于控制车身的目标朝向角

extern void PID_yaw();
extern void set_speed();
extern void set_speed_target(int target_speed1, int target_speed2, int target_speed3, int target_speed4);
extern void run_speed();
extern void set_speed_to_stepper();
extern void move_dist_time(double dx, double dy);
extern void move_dist_dx(double dx);
extern void move_dist_dy(double dy);


#endif
