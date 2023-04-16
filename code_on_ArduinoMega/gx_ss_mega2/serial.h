#ifndef __SERIAL_H
#define __SERIAL_H

#define dist_bias  0.25    // 0.1, 两次相邻读取到的距离最大偏差，若大于则为错误值，忽略
#define dist_max   2.4    // 最大读取值，若大于则为错误值，忽略

extern double x_bias;
extern double y_bias;
extern double x_bias_temp;
extern double y_bias_temp;

extern double x_dist;
extern double y_dist;
extern double x_dist_org;
extern double y_dist_org;
extern double x_dist_temp;
extern double y_dist_temp;

extern double x_pre;
extern double y_pre;

extern double x_move;
extern double y_move;
extern int move_read_flag;

extern double x_rush;
extern double y_rush;
extern int rush_read_flag;

extern int change_read_flag;

extern void read_dist_order();
extern void read_move_order();
// extern void read_dist_tof_x();
// extern void read_dist_tof_y();
// extern void read_dist_lidar();
extern void read_dist_tof_ros();
extern void read_bias(int order_head);
extern int read_order_head();
extern double read_change_order();

#endif