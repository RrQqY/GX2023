#ifndef __SERIAL_H
#define __SERIAL_H

extern char capture_color;

extern float x_bias;
extern float y_bias;

extern float x_dist;
extern float y_dist;


extern void read_capture_flag_color();
extern void read_target_bias();
extern void read_lidar_dist();

#endif