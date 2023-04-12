/* 这里存储一些和IMU有关的函数 */
#include "gx_ss_mega.h"


String serial_str = "";
String speed_str = "";
int speed_flag = 1;            // 当前读取的是第几个电机的速度值
int speed_dir_flag = 1;        // 当前读取电机速度的方向（0为负，1为正）

/* 获取上位机下发的速度指令 */
// 从串口中读取四个电机的设定速度，并对电机转速和方向进行设定
void read_dist_order() {
  static int read_speed1, read_speed2, read_speed3, read_speed4 = 0;   
  if(serial_pi1.available() > 0){  
    // 按位读取字符串
    int speed_char = serial_pi1.read();
    serial_str += (char)speed_char;

    if (isDigit(speed_char)) {
      speed_str += (char)speed_char;
    }

    // 如果读取到负号，则设定当前方向标志为负
    if (speed_char == '-') {
      speed_dir_flag = 0;
    }

    // 如果读取到逗号，则保存当前速度，换下一个速度
    if (speed_char == ',') {
      switch(speed_flag){
        case 1: {
          if(speed_dir_flag == 1){
            read_speed1 = speed_str.toInt();
          }else if(speed_dir_flag == 0){
            read_speed1 = -speed_str.toInt();
          }            
        }
        case 2:{
          if(speed_dir_flag == 1){
            read_speed2 = speed_str.toInt();
          }else if(speed_dir_flag == 0){
            read_speed2 = -speed_str.toInt();
          }
        }
        case 3:{
          if(speed_dir_flag == 1){
            read_speed3 = speed_str.toInt();
          }else if(speed_dir_flag == 0){
            read_speed3 = -speed_str.toInt();
          }
        }
      }
      speed_str = "";
      speed_dir_flag = 1;
      speed_flag += 1;
    }
    
    // 如果读取到换行符，则说明字符串结束
    if (speed_char == '@') {
      if(speed_dir_flag == 1){
        read_speed4 = speed_str.toInt();
      }else if(speed_dir_flag == 0){
        read_speed4 = -speed_str.toInt();
      }

      if(((pre_speed1 != read_speed1) || (pre_speed2 != read_speed2) || (pre_speed3 != read_speed3) || (pre_speed4 != read_speed4))){
        // acc_state = 0;
        // acc_step = 50;
        // Serial.println(serial_str);

        speed1 = read_speed1;
        speed2 = read_speed2;
        speed3 = read_speed3;
        speed4 = read_speed4;
        
        pre_speed1 = read_speed1;
        pre_speed2 = read_speed2;
        pre_speed3 = read_speed3;
        pre_speed4 = read_speed4;

        set_speed_target(speed1, speed2, speed3, speed4);

        // Serial.println(serial_str);

        while(serial_pi1.read()>=0);      // 清空缓冲区
      }

      speed_str = "";
      serial_str = "";
      speed_dir_flag = 1;
      speed_flag = 1;
    }
  }
}


String move_str = "";
int move_dir_flag = 1;     // 当前读取电机速度的方向（0为负，1为正）
double x_move = 0.0;       // 向x方向移动的距离
double y_move = 0.0;       // 向y方向移动的距离

int move_read_flag = 0;    // 是否读到新的移动指令

/* 获取上位机下发的移动位置指令 */
// 从串口中读取设定移动位置
void read_move_order() {
  static double read_x_move, read_y_move = 0.0;
  static int start_flag = 0;

  while(1){
    if(serial_pi1.available() > 0){  
      // 按位读取字符串
      int move_char = serial_pi1.read();
      serial_str += (char)move_char;

      if (move_char == 'M') {
        start_flag = 1;
      }

      // // 如果读取到负号，则设定当前方向标志为负
      // if ((start_flag == 1) && (move_char == '-')) {
      //   move_dir_flag = 0;
      // }

      if ((start_flag == 1) && (isDigit(move_char))) {
        move_str += (char)move_char;
      }

      // 如果读取到逗号，则保存x轴位置，换y轴位置
      if ((start_flag == 1) && (move_char == ',')) {
        // if(move_dir_flag == 1){
        //   read_x_move = move_str.toInt();
        // }else if(move_dir_flag == 0){
        //   read_x_move = -move_str.toInt();
        // }   
        read_x_move = move_str.toInt();         
        move_str = "";
        // move_dir_flag = 1;
      }
      
      // 如果读取到换行符，则说明字符串结束
      if ((start_flag == 1) && (move_char == '@')) {
        // if(move_dir_flag == 1){
        //   read_y_move = move_str.toInt();
        // }else if(move_dir_flag == 0){
        //   read_y_move = -move_str.toInt();
        // }
        read_y_move = move_str.toInt();

        x_move = (read_x_move - 3000.0) / 1000.0;
        y_move = (read_y_move - 3000.0) / 1000.0;
        // Serial.print(x_move);
        // Serial.print(", ");
        // Serial.println(y_move);

        move_read_flag = 1;

        // while(serial_pi1.read()>=0);      // 清空缓冲区

        move_str = "";
        serial_str = "";
        // move_dir_flag = 1;

        return;
      }
    }
  }   
}


/*  ToF传感器安装位置：
    serial_tof1：后
    serial_tof2：前
    serial_tof3：右
    serial_tof4：左    */

double x_dist = 0.0;      // 雷达到前侧墙距离
double y_dist = 0.0;      // 雷达到右侧墙距离
// String str = "";

/* 获取ToF传感器检测距离 */ 
// 获取y方向ToF传感器检测距离（距后）
// 获取x方向ToF传感器检测距离（距右）
void read_dist_tof_y() {
  static double dist1, dist2 = 0.0;
  static int scan_flag = 1;

  int start_flag = 0;
  String serial_str = "";
  char serial_char;

  // 如果在右方半场，则用后ToF传感器3检测x_dist：x_dist = dist3
  if(scan_flag == 1) {
    while(1) {
      if(serial_tof1.available() > 0){
        // Serial.println("111111111111");
        // 按位读取字符串
        serial_char = serial_tof1.read();
      //   str += (char)serial_char;
        // 如果读取到d，则开始读取
        //  Serial.println(serial_char);
        if (serial_char == 'd') {
          start_flag = 1;
        }
        if ((start_flag == 1) && (isDigit(serial_char))) {
          serial_str += (char)serial_char;
        }
        // 如果读取到m，则说明字符串结束
        if ((start_flag == 1) && (serial_char == 'm')) {
          dist1 = serial_str.toInt() / 1000.0;
          // Serial.println(str);
          serial_str = "";
          start_flag = 0;
          // str = "";

          if (dist1 + 0.135 >= 1.2) {
            scan_flag = 2;
          }
          // Serial.print("1: ");
          // Serial.print(dist1);
          break ;
        }
      }
      // while(serial_tof1.read()>0);
    }
    y_dist = dist1 + 0.135;
  }
  // 如果在上方半场，则用前ToF传感器2检测y_dist：y_dist = 2.4 - dist2
  else if (scan_flag == 2) {
    while(1) {
      if(serial_tof2.available() > 0){
        // Serial.println("2222222222222222");
        // 按位读取字符串
        serial_char = serial_tof2.read();
        // 如果读取到d，则开始读取
        //Serial.println(serial_char);
        if (serial_char == 'd') {
          start_flag = 1;
        }
        if ((start_flag == 1) && (isDigit(serial_char))) {
          serial_str += (char)serial_char;
        }
        // 如果读取到m，则说明字符串结束
        if ((start_flag == 1) && (serial_char == 'm')) {
          dist2 = serial_str.toInt() / 1000.0;
          serial_str = "";
          start_flag = 0;

          if (dist2 + 0.135 >= 1.2) {
            scan_flag = 1;
          }
          // Serial.print("2: ");
          // Serial.print(dist2);
          break ;
        }
      }
    }
    y_dist = 2.4 - dist2 - 0.135;
  }
  // Serial.println(scan_flag);
}


// 获取x方向ToF传感器检测距离（距右）
void read_dist_tof_x() {
  static double dist3, dist4 = 0.0;
  static int scan_flag = 3;
  
  int start_flag = 0;
  String serial_str = "";
  char serial_char;

  // 如果在右方半场，则用后ToF传感器3检测x_dist：x_dist = dist3
  if(scan_flag == 3) {
    while(1) {
      if(serial_tof3.available() > 0){
        // Serial.println("111111111111");
        // 按位读取字符串
        serial_char = serial_tof3.read();
      //   str += (char)serial_char;
        // 如果读取到d，则开始读取
        //  Serial.println(serial_char);
        if (serial_char == 'd') {
          start_flag = 1;
        }
        if ((start_flag == 1) && (isDigit(serial_char))) {
          serial_str += (char)serial_char;
        }
        // 如果读取到m，则说明字符串结束
        if ((start_flag == 1) && (serial_char == 'm')) {
          dist3 = serial_str.toInt() / 1000.0;
          // Serial.println(str);
          serial_str = "";
          start_flag = 0;
          // str = "";

          if (dist3 + 0.135 >= 1.2) {
            scan_flag = 4;
          } 
          // Serial.print("3: ");
          // Serial.print(dist3);
          break ;
        }
      }
      // while(serial_tof1.read()>0);
    }
    x_dist = dist3 + 0.135;
  }
  // 如果在上方半场，则用前ToF传感器2检测y_dist：y_dist = 2.4 - dist2
  else if (scan_flag == 4) {
    while(1) {
      if(serial_tof4.available() > 0){
        // Serial.println("2222222222222222");
        // 按位读取字符串
        serial_char = serial_tof4.read();
        // 如果读取到d，则开始读取
        //Serial.println(serial_char);
        if (serial_char == 'd') {
          start_flag = 1;
        }
        if ((start_flag == 1) && (isDigit(serial_char))) {
          serial_str += (char)serial_char;
        }
        // 如果读取到m，则说明字符串结束
        if ((start_flag == 1) && (serial_char == 'm')) {
          dist4 = serial_str.toInt() / 1000.0;
          serial_str = "";
          start_flag = 0;

          if (dist4 + 0.135 >= 1.2) {
            scan_flag = 3;
          }
          // Serial.print("4: ");
          // Serial.print(dist4);
          break ;
        }
      }
    }
    x_dist = 2.4 - dist4 - 0.135;
  }
  // Serial.println(scan_flag);
}


// 获取树莓派2传回的激光雷达检测距离
// 从激光雷达获取车中心距离前侧墙壁和右侧墙壁的距离
// 格式为“D + x_dist（xxxx形式，结果/1000以m为单位） + ',' + y_dist”
void read_dist_lidar() {
  int start_flag = 0;
  String serial_str = "";
  int num_length = 0;

  while(1) {
    if(serial_pi2.available() > 0){
      // 按位读取字符串
      int serial_char = serial_pi2.read();

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


// 获取树莓派2传回的ToF传感器检测距离x_dist和y_dist
// 格式为“x + x_dist（xxxx形式，结果/1000以m为单位） + '@'”, y_dist同理
void read_dist_tof_ros() {
  double x_dist_temp = 0.0;
  double y_dist_temp = 0.0;
  static double x_dist_arr[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
  static double y_dist_arr[]{0.0, 0.0, 0.0, 0.0, 0.0, 0.0};
  double x_dist_avr = 0.0;
  double y_dist_avr = 0.0;

  String serial_str = "";
  // String str = "";
  char serial_char;
  int start_flag = 0;

  while(1) {
    if(serial_pi2.available() > 0){
      // 按位读取字符串
      int serial_char = serial_pi2.read();

      // 如果读取到R（ROS），则开始读取到达标志
      if (serial_char == 'R') {
        start_flag = 1;
      }

      if ((start_flag == 1) && (isDigit(serial_char))) {
        serial_str += (char)serial_char;
      }

      // 如果读取到逗号，则保存当前速度，换下一个速度
      if (serial_char == ',') {
        x_dist_temp = serial_str.toInt() / 1000.0 + 0.14;

        // 数据剔除
        if ((x_dist_temp > dist_max) || ((abs(x_dist_temp-x_dist) > dist_bias) && (x_dist != 0.0))) {
          x_dist_temp = x_dist;
        }
        // // 均值滤波
        // for (int i = 1; i <= 5; i ++) {
        //   x_dist_arr[i] = x_dist_arr[i - 1];
        // }
        // x_dist_arr[0] = x_dist_temp;
        // x_dist_avr = (x_dist_arr[0]+x_dist_arr[1]+x_dist_arr[2]+x_dist_arr[3]+x_dist_arr[4]+x_dist_arr[5])/6.0;    // 均值

        serial_str = "";
      }
      
      // 如果读取到换行符，则说明字符串结束
      if ((start_flag == 1) && (serial_char == '@')) {
        y_dist_temp = serial_str.toInt() / 1000.0 + 0.14;

        // 数据剔除
        if ((y_dist_temp > dist_max) || ((abs(y_dist_temp-y_dist) > dist_bias) && (y_dist != 0.0))) {
          y_dist_temp = y_dist;
        }
        // // 均值滤波
        // for (int i = 1; i <= 5; i ++) {
        //   y_dist_arr[i] = y_dist_arr[i - 1];
        // }
        // y_dist_arr[0] = y_dist_temp;
        // y_dist_avr = (y_dist_arr[0]+y_dist_arr[1]+y_dist_arr[2]+y_dist_arr[3]+y_dist_arr[4]+y_dist_arr[5])/6.0;    // 均值

        serial_str = "";
        start_flag = 0;

        break ;
      }
    }
  }
  x_dist = x_dist_temp;
  y_dist = 2.4 - y_dist_temp;
}

