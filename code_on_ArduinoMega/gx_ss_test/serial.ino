/* 这里存储一些串口有关的函数 */
#include "gx_ss_test.h"

/* -------- 获取物块颜色 --------*/
char capture_color = ' ';    // 从转盘上抓取时检测到的物体颜色

// 准备从转盘上抓取时，从串口2中读取树莓派1回传的抓取标志和颜色信息
// 格式为“C + 1/0（物体是否到达位置） + r/g/b（物体颜色）”
void read_capture_flag_color() {
    int start_flag = 0;
    int arrive_flag = 0;
    char color = ' ';

    while(1) {
        if(imu_serial.available() > 0){
            // 按位读取字符串
            int serial_char = imu_serial.read();

            // 如果读取到C（Capture），则开始读取到达标志
            if (serial_char == 'C') {
                start_flag = 1;
            }

            // 读取到达标志后，开始读取颜色
            if((start_flag == 1) && ((serial_char == '1') || (serial_char == '0'))) {
                arrive_flag = serial_char - '0';
                // start_flag == 2;
            }

            // 读取颜色
            if((start_flag == 1) && ((serial_char == 'r') || (serial_char == 'g') || (serial_char == 'b'))) {
                color = serial_char;
                // start_flag == 3;
            }
            
            // 如果读取到换行符，则说明字符串结束
            if ((start_flag == 1) && (serial_char == '\n')) {
                start_flag = 0;

                if(arrive_flag == 1) {
                  capture_color = color;

                  // Serial.print("Arrived! ");
                  // Serial.print(color);
                  // Serial.print('\n');

                  return ;
                }
            }
            // Serial.println(serial_char);
        }
    }
}


/* -------- 获取靶标中心偏差 --------*/
float x_bias = 0.0;    // 与靶标中心的x轴偏差
float y_bias = 0.0;    // 与靶标中心的y轴偏差

// 在靶标前时，从串口2中读取树莓派1回传的位置偏差信息
// 格式为“B + x_bias（xxx形式，结果/1000表示百分比） + ',' + y_bias”
void read_target_bias() {
    int start_flag = 0;
    String serial_str = "";
    int num_length = 0;

    while(1) {
        if(imu_serial.available() > 0){
            // 按位读取字符串
            int serial_char = imu_serial.read();

            // 如果读取到B（Bias），则开始读取到达标志
            if (serial_char == 'B') {
                start_flag = 1;
            }

            if ((start_flag == 1) && (isDigit(serial_char))) {
                serial_str += (char)serial_char;
                num_length ++;
            }

            // 如果读取到逗号，则保存当前速度，换下一个速度
            if (serial_char == ',') {
                x_bias = serial_str.toInt() / (pow(10, num_length));
                serial_str = "";
                num_length = 0;
            }
            
            // 如果读取到换行符，则说明字符串结束
            if ((start_flag == 1) && (serial_char == '\n')) {
                y_bias = serial_str.toInt() / (pow(10, num_length));
                serial_str = "";
                num_length = 0;
                start_flag = 0;

                // Serial.print("Bias: ");
                // Serial.print(String(x_bias, 3));
                // Serial.print(", ");
                // Serial.print(String(y_bias, 3));
                // Serial.print('\n');

                return ;
            }
            // Serial.println(serial_char);
        }
    }
}


/* -------- 获取雷达前右距离 --------*/
float x_dist = 0.0;      // 雷达到前侧墙距离
float y_dist = 0.0;      // 雷达到右侧墙距离

// 从激光雷达获取车中心距离前侧墙壁和右侧墙壁的距离
// 格式为“D + x_dist（xxxx形式，结果/1000以m为单位） + ',' + y_dist”
void read_lidar_dist() {
    int start_flag = 0;
    String serial_str = "";
    int num_length = 0;

    while(1) {
        if(pi2_serial.available() > 0){
            // 按位读取字符串
            int serial_char = pi2_serial.read();

            // 如果读取到D（Distance），则开始读取到达标志
            if (serial_char == 'D') {
                start_flag = 1;
            }

            if ((start_flag == 1) && (isDigit(serial_char))) {
                serial_str += (char)serial_char;
                num_length ++;
            }

            // 如果读取到逗号，则保存当前速度，换下一个速度
            if (serial_char == ',') {
                x_dist = serial_str.toInt() / (pow(10, num_length) - 1);
                serial_str = "";
                num_length = 0;
            }
            
            // 如果读取到换行符，则说明字符串结束
            if ((start_flag == 1) && (serial_char == '\n')) {
                y_dist = serial_str.toInt() / (pow(10, num_length) - 1);
                serial_str = "";
                num_length = 0;
                start_flag = 0;

                // Serial.print("Dist: ");
                // Serial.print(String(x_dist, 4));
                // Serial.print(", ");
                // Serial.print(String(y_dist, 4));
                // Serial.print('\n');

                return ;
            }
            // Serial.println(serial_char);
        }
    }
}