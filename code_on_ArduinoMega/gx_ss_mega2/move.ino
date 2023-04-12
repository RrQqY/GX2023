/* 这里存储一些和底盘运动控制有关的函数 */
#include "gx_ss_mega2.h"


int speed1 = 0;
int speed2 = 0;
int speed3 = 0;
int speed4 = 0;

int pre_speed1 = 0;
int pre_speed2 = 0;
int pre_speed3 = 0;
int pre_speed4 = 0;


double acc_step = 1600000;
int acc_state = 0;

double x_pre = 0.0;
double y_pre = 0.0;

double targetDist_tof_x = 0.0;
double targetDist_tof_y = 0.0;

int change_yaw_times = 0;

// 从imu中读取当前倾角，修正电机速度
void PID_yaw() {
  static double outDelta_old = 0;
  static double feedbackYaw_old = 0;
  static double newYawPulses_yaw = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_yaw = 0;
  static double outYawPWM_yaw = 0;
  static double outYawPWM_old_yaw = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID PID_yaw = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // // 每重新开始一次巡线，重置上一次的所有变量
  // if(clear_flag == 1){
  //   outYawPWM_yaw = 0;
  //   outYawPWM_old_yaw = 0;
  // }
  // else{
  // 陀螺仪矫正pid控制器
  feedbackYawVel_yaw = get_yaw(0);
  // Serial.println(feedbackYawVel_yaw);

  // 将角度变化限制在1.5°范围内
  if((feedbackYawVel_yaw - feedbackYaw_old) > 2.5){
    feedbackYawVel_yaw =  feedbackYaw_old + 2.5;
  }
  else if((feedbackYawVel_yaw - feedbackYaw_old) < -2.5){
    feedbackYawVel_yaw =  feedbackYaw_old - 2.5;
  }
  // feedbackYaw_old = feedbackYawVel_yaw;
  // Serial.println(targetYawPulses);
  

  outYawPWM_yaw = PID_yaw.Compute(targetYawPulses, feedbackYawVel_yaw);
  // if(outYawPWM_yaw > YawPWM_MAX){
  //     outYawPWM_yaw = YawPWM_MAX;
  // }  

  // Serial.println(outYawPWM_yaw);

  // // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
  // targetPulses[0] -= (outYawPWM_yaw - outYawPWM_old_yaw)/5;
  // targetPulses[1] += (outYawPWM_yaw - outYawPWM_old_yaw)/5;
  // targetPulses[2] -= (outYawPWM_yaw - outYawPWM_old_yaw)/5;
  // targetPulses[3] += (outYawPWM_yaw - outYawPWM_old_yaw)/5;
  // 将陀螺仪矫正速度加到编码器目标速度上
  
  // Serial.print(feedbackYawVel_yaw);
  // Serial.print("@@");
  // Serial.println((outYawPWM_yaw));
  // if(!((abs(outDelta_old - (outYawPWM_yaw - outYawPWM_old_yaw)) > 2000) && ((abs(outYawPWM_yaw - outYawPWM_old_yaw)<100) || ((outYawPWM_yaw - outYawPWM_old_yaw) == -outDelta_old))) || (change_yaw_times == 1)){
  double delta_change = 0.0;
  // delta_change = outDelta_old - (outYawPWM_yaw - outYawPWM_old_yaw);


  speed1 -= (outYawPWM_yaw - outYawPWM_old_yaw);
  speed2 += (outYawPWM_yaw - outYawPWM_old_yaw);
  speed3 -= (outYawPWM_yaw - outYawPWM_old_yaw);
  speed4 += (outYawPWM_yaw - outYawPWM_old_yaw);
  // change_yaw_times = 0;

  // Serial.print(", ");
  // Serial.println(speed1);

  outDelta_old = outYawPWM_yaw - outYawPWM_old_yaw;

  // Serial.println(outYawPWM_yaw - outYawPWM_old_yaw);

  outYawPWM_old_yaw = outYawPWM_yaw;
  //Serial.println(outYawPWM_yaw);
  //set_speed(targetPulses[0], targetPulses[1], targetPulses[2], targetPulses[3]); 
  
//  }
}


// 从串口中读取ToF传感器检测的当前和目标距离的误差，修正车身横向位置（dy方向移动时）
void PID_tof_x(int clear_flag) {
  static double newTofPulses_tof_x = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackDist_tof_x = 0;
  static double outTofPWM_tof_x = 0;
  static double outTofPWM_old_tof_x = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID PID_tof_x = PID(PWM_MIN, PWM_MAX, Kp_tof_y, Ki_tof_y, Kd_tof_y);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outTofPWM_tof_x = 0;
    outTofPWM_old_tof_x = 0;
  }
  else{
    // 陀螺仪矫正pid控制器
    feedbackDist_tof_x = x_dist;

    outTofPWM_tof_x = PID_tof_x.Compute(targetDist_tof_x, feedbackDist_tof_x);
    if(outTofPWM_tof_x > TofPWM_MAX){
        outTofPWM_tof_x = TofPWM_MAX;
    }  

    // 将陀螺仪矫正速度加到编码器目标速度上
    speed1 -= (outTofPWM_tof_x - outTofPWM_old_tof_x);
    speed2 += (outTofPWM_tof_x - outTofPWM_old_tof_x);
    speed3 += (outTofPWM_tof_x - outTofPWM_old_tof_x);
    speed4 -= (outTofPWM_tof_x - outTofPWM_old_tof_x);

    outTofPWM_old_tof_x = outTofPWM_tof_x;
    //Serial.println(outYawPWM_tof);
 }
}


// 从串口中读取ToF传感器检测的当前和目标距离的误差，修正车身横向位置（dx方向移动时）
void PID_tof_y(int clear_flag) {
  static double newTofPulses_tof_y = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackDist_tof_y = 0;
  static double outTofPWM_tof_y = 0;
  static double outTofPWM_old_tof_y = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID PID_tof_y = PID(PWM_MIN, PWM_MAX, Kp_tof_x, Ki_tof_x, Kd_tof_x);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outTofPWM_tof_y = 0;
    outTofPWM_old_tof_y = 0;
  }
  else{
    // 陀螺仪矫正pid控制器
    feedbackDist_tof_y = y_dist;

    outTofPWM_tof_y = PID_tof_y.Compute(targetDist_tof_y, feedbackDist_tof_y);
    if(outTofPWM_tof_y > TofPWM_MAX){
        outTofPWM_tof_y = TofPWM_MAX;
    }  

    // 将陀螺仪矫正速度加到编码器目标速度上
    speed1 += (outTofPWM_tof_y - outTofPWM_old_tof_y);
    speed2 += (outTofPWM_tof_y - outTofPWM_old_tof_y);
    speed3 += (outTofPWM_tof_y - outTofPWM_old_tof_y);
    speed4 += (outTofPWM_tof_y - outTofPWM_old_tof_y);

    outTofPWM_old_tof_y = outTofPWM_tof_y;
    //Serial.println(outYawPWM_tof);
 }
}


// // 带加速度的电机转动速度设定
// void set_speed_acc(int set_speed1, int set_speed2, int set_speed3, int set_speed4) {
//   static double acc_speed1 = 0.0;
//   static double acc_speed2 = 0.0;
//   static double acc_speed3 = 0.0;
//   static double acc_speed4 = 0.0;

//   static int start_speed1 = 0;
//   static int start_speed2 = 0;
//   static int start_speed3 = 0;
//   static int start_speed4 = 0;

//   static int start_time = 0;
//   static int end_time = 0;

//   if(acc_state == 0){
//     start_speed1 = stepper1.speed();
//     start_speed2 = stepper2.speed();
//     start_speed3 = stepper3.speed();
//     start_speed4 = stepper4.speed();

//     start_time = millis();
//   }
  
//   if(acc_state < acc_step) {
//     acc_speed1 = (double)acc_state / (double)acc_step * (set_speed1 - start_speed1) + start_speed1;
//     acc_speed2 = (double)acc_state / (double)acc_step * (set_speed2 - start_speed2) + start_speed2;
//     acc_speed3 = (double)acc_state / (double)acc_step * (set_speed3 - start_speed3) + start_speed3;
//     acc_speed4 = (double)acc_state / (double)acc_step * (set_speed4 - start_speed4) + start_speed4;

//     stepper1.setSpeed((int)acc_speed1);    // 更新电机转动速度
//     stepper2.setSpeed((int)acc_speed2);    // 更新电机转动速度
//     stepper3.setSpeed((int)acc_speed3);    // 更新电机转动速度
//     stepper4.setSpeed((int)acc_speed4);    // 更新电机转动速度 

//     acc_state = acc_state + 1;
//     // Serial.println(acc_state);
//     // delay_ms(10);

//     if(acc_state == acc_step){
//       end_time = millis();
//       Serial.print("time: ");
//       Serial.println(end_time - start_time);
//     }
//   }
//   else {
//     // Serial.println("Finished");
//     stepper1.setSpeed(set_speed1);    // 更新电机转动速度
//     stepper2.setSpeed(set_speed2);    // 更新电机转动速度
//     stepper3.setSpeed(set_speed3);    // 更新电机转动速度
//     stepper4.setSpeed(set_speed4);    // 更新电机转动速度 
//   } 
// }


// 设定电机转动速度和方向
// void set_speed_target(int target_speed1, int target_speed2, int target_speed3, int target_speed4) {
//   // int set_speed1, set_speed2, set_speed3, set_speed4 = 0;

//   target_speed1 = -target_speed1;
//   target_speed3 = -target_speed3;

//   if(target_speed1 > 0){
//     stepper1.setPinsInverted(HIGH, false, true);    // 步进电机正转向为顺时针
//     speed1 = target_speed1;
//   }else if(target_speed1 < 0){
//     stepper1.setPinsInverted(LOW, false, true);     // 步进电机正转向为逆时针
//     speed1 = -target_speed1;
//   }else{
//     speed1 = 0;    
//   }

//   if(target_speed2 > 0){
//     stepper2.setPinsInverted(HIGH, false, true);    // 步进电机正转向为顺时针
//     speed2 = target_speed2;
//   }else if(target_speed2 < 0){
//     stepper2.setPinsInverted(LOW, false, true);     // 步进电机正转向为逆时针
//     speed2 = -target_speed2;
//   }else{
//     speed2 = 0;
//   }

//   if(target_speed3 > 0){
//     stepper3.setPinsInverted(HIGH, false, true);    // 步进电机正转向为顺时针
//     speed3 = target_speed3;
//   }else if(target_speed3 < 0){
//     stepper3.setPinsInverted(LOW, false, true);     // 步进电机正转向为逆时针
//     speed3 = -target_speed3;
//   }else{
//     speed3 = 0;
//   }

//   if(target_speed4 > 0){
//     stepper4.setPinsInverted(HIGH, false, true);    // 步进电机正转向为顺时针
//     speed4 = target_speed4;
//   }else if(target_speed4 < 0){
//     stepper4.setPinsInverted(LOW, false, true);     // 步进电机正转向为逆时针
//     speed4 = -target_speed4;
//   }else{
//     speed4 = 0;
//   }

//   // set_speed_to_stepper();
//   // stepper1.setSpeed(speed1);    // 更新电机转动速度
//   // stepper2.setSpeed(speed2);    // 更新电机转动速度
//   // stepper3.setSpeed(speed3);    // 更新电机转动速度
//   // stepper4.setSpeed(speed4);    // 更新电机转动速度 
// }

//修改电机全局速度
void set_speed_target(int target_speed1, int target_speed2, int target_speed3, int target_speed4) {
  speed1 = target_speed1;
  speed2 = target_speed2;
  speed3 = target_speed3;
  speed4 = target_speed4;
}


// 将电机速度全局变量设定到电机对象中
void set_speed_to_stepper() {
  // Serial.println("Finished");
  stepper1.setSpeed(speed1);    // 更新电机转动速度
  stepper2.setSpeed(-speed2);    // 更新电机转动速度
  stepper3.setSpeed(speed3);    // 更新电机转动速度
  stepper4.setSpeed(-speed4);    // 更新电机转动速度 
}


// 电机按照设定的转动速度和方向运行
void run_speed() {
  //boolean flag1;
  //flag1=
  stepper1.runSpeed();
  stepper2.runSpeed();
  stepper3.runSpeed();
  stepper4.runSpeed();
  //Serial.println(flag1);
}


// 设定电机速度
void set_speed(){
  //set_speed_target(target_speed1, target_speed2, target_speed3, target_speed4);
  set_speed_to_stepper();
  unsigned long mMillis;
  unsigned long cMillis = millis();

  // 每次设定电机速度时，循环执行run_delay_time时间的runSpeed
  while(1){
    run_speed();
    mMillis = millis();
    if(mMillis-cMillis >= run_delay_time){
      break;
    }
  }
}



// 直接根据时间开环移动到与当前位置相对dx，dy的位置
void move_dist_time(double dx, double dy) {
  if((dx == 0) && (dy == 0)) return;
  x_pre += dx;
  y_pre += dy;

  double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
  double ky = dy / sqrt(pow(dx,2) + pow(dy,2));
  
  double dist = sqrt(pow(dx,2) + pow(dy,2));

  // 距离目标较远，分快慢两段运动
  if(dist > dist_threshold_far){
    double s1 = dist - dist_threshold_far;
    double s2 = dist_threshold_far - dist_threshold_close;
    double t1 = s1 / (move_speed * kp_speed * 0.375);
    double t2 = s2 / (move_speed_slow * kp_speed * 0.375);

    // Serial.print(t1);
    // Serial.print(", ");
    // Serial.println(t2);

    if((t1 == 0) || (t2 == 0)) return;

    set_speed_target((-kx + ky)*move_speed, (kx + ky)*move_speed, (kx + ky)*move_speed, (-kx + ky)*move_speed);
    set_speed_to_stepper();
    //Serial.println(speed2);
    //set_speed_to_stepper();
    unsigned long delta_t1 = millis() + t1 * 1000;
    while(millis() < delta_t1){
    // while(1){
      PID_yaw();
      set_speed_to_stepper();
      set_speed();
      //run_speed();
    }

    set_speed_target((-kx + ky)*move_speed_slow, (kx + ky)*move_speed_slow, (kx + ky)*move_speed_slow, (-kx + ky)*move_speed_slow);
    set_speed_to_stepper();
    unsigned long delta_t2 = millis() + t2 * 1000;
    while(millis() < delta_t2){
      PID_yaw();
      set_speed_to_stepper();
      // run_speed();
      set_speed();

      // Serial.print(speed1);
      // Serial.print(", ");
      // Serial.println(speed1);
    }

    set_speed_target(0, 0, 0, 0);
    set_speed_to_stepper();
    set_speed();
    move_read_flag = 0;
    return;
  }
  // 距离目标较近，以慢速运动
  else if(dist > 0){
    double s2 = dist - dist_threshold_close;
    double t2 = s2 / (move_speed_slow * kp_speed * 0.375);

    if(t2 == 0) return;

    set_speed_target((-kx + ky)*move_speed_slow, (kx + ky)*move_speed_slow, (kx + ky)*move_speed_slow, (-kx + ky)*move_speed_slow);
    set_speed_to_stepper();

    unsigned long delta_t2 = millis() + t2 * 1000;
    while(millis() < delta_t2){
      PID_yaw();
      set_speed_to_stepper();
      // run_speed();
      set_speed();
    }
    set_speed_target(0, 0, 0, 0);
    set_speed_to_stepper();
    set_speed();
    move_read_flag = 0;
    return;
  }
}


// 移动x轴指定时间
// 以y_dist作为法向平移矫正
void move_time_dx(double dx) {
  int read_tof_flag = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  double start_time, present_time = 0.0;
  if(dx == 0) return;

  dx = dx * 1000;

  PID_tof_y(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();
  targetDist_tof_y = y_dist;

  // 判断移动方向正负
  if(dx >= 0){
    move_dir_flag = 1;
  }
  else if(dx < 0){
    move_dir_flag = -1;
  }
  
//   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * -rush_speed*slide_k, move_dir_flag * rush_speed*slide_k, 
                    move_dir_flag * rush_speed*slide_k, move_dir_flag * -rush_speed*slide_k);
  
  start_time = millis();
  while (1) {
    present_time = millis();
    if((present_time - start_time) >= dx){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      rush_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
    }
    
    PID_yaw();                      // 方向矫正

    if(read_tof_flag >= read_tof_freq) {
      PID_tof_y(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 移动y轴指定时间
// 以x_dist作为法向平移矫正
void move_time_dy(double dy) {
  int read_tof_flag = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  double start_time, present_time = 0.0;
  if(dy == 0) return;

  dy = dy * 1000;

  PID_tof_x(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();
  targetDist_tof_x = x_dist;

  // 判断移动方向正负
  if(dy >= 0){
    move_dir_flag = 1;
  }
  else if(dy < 0){
    move_dir_flag = -1;
  }
  
//   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * rush_speed*slide_k, move_dir_flag * rush_speed*slide_k, 
                    move_dir_flag * rush_speed*slide_k, move_dir_flag * rush_speed*slide_k);
  
  start_time = millis();
  while (1) {
    present_time = millis();
    if((present_time - start_time) >= dy){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      rush_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
    }
    
    PID_yaw();                      // 方向矫正

    if(read_tof_flag >= read_tof_freq) {
      PID_tof_x(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 移动到y位置
// 从tof传感器（激光雷达）计算得到当前绝对位置
// 以y_dist作为移动目标条件，x_dist作为法向平移矫正
void move_to_y(double dy) {
  int read_tof_flag = 0;
  int change_speed_flag = 0;
  int change_speed_flag_pre = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  // Serial.println("@@@@@@@");
  if(dy == 0) return;

  y_pre += dy;

  PID_tof_x(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();

  // 判断移动方向正负
  if((dy - y_dist) >= 0){
    move_dir_flag = 1;
  }
  else if((dy - y_dist) < 0){
    move_dir_flag = -1;
  }

  targetDist_tof_x = x_dist;
  // Serial.println(targetDist_tof_x);

  double y_target = dy;
  // Serial.println(y_dist);

//   double ky = dy / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed);
  while (1) {
    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
      // Serial.println(y_dist);
    }

    // 如果还未到指定位置
    sub_temp = move_dir_flag * (y_target - y_dist);
    // Serial.println(sub_temp);
    if(sub_temp > dist_threshold_far) {
      change_speed_flag = 1;
    }
    else if(sub_temp > dist_threshold_close) {
      change_speed_flag = 2;
    }
    else {
      change_speed_flag = 3;
    }

    if((change_speed_flag == 1) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed);
    }
    else if((change_speed_flag == 2) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow);
    }
    else if((change_speed_flag == 3) && (change_speed_flag > change_speed_flag_pre)){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    change_speed_flag_pre = change_speed_flag;
    
    if(change_speed_flag == 1){
      PID_yaw();                      // 方向矫正
    }
    
    if(read_tof_flag >= read_tof_freq) {
      // PID_tof_x(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 移动到x位置
// 从tof传感器（激光雷达）计算得到当前绝对位置
// 以x_dist作为移动目标条件，y_dist作为法向平移矫正
void move_to_x(double dx) {
  int read_tof_flag = 0;
  int change_speed_flag = 0;
  int change_speed_flag_pre = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  if(dx == 0) return;

  x_pre += dx;

  PID_tof_y(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();

  // 判断移动方向正负
  if((dx - x_dist) >= 0){
    move_dir_flag = 1;
  }
  else if((dx - x_dist) < 0){
    move_dir_flag = -1;
  }

  targetDist_tof_y = y_dist;

  double x_target = dx;
  //Serial.println(x_dist);
  
//   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * -move_speed*slide_k, move_dir_flag * move_speed*slide_k, 
                    move_dir_flag * move_speed*slide_k, move_dir_flag * -move_speed*slide_k);
  while (1) {
    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
    }

    // 如果还未到指定位置
    sub_temp = move_dir_flag * (x_target - x_dist);
    if(sub_temp > dist_threshold_far) {
      // Serial.println("--------------------------------");
      change_speed_flag = 1;
    }
    else if(sub_temp > dist_threshold_close) {
      // Serial.println("--------------------------------");
      change_speed_flag = 2;
    }
    else{
      change_speed_flag = 3;
    }

    if((change_speed_flag == 1) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * -move_speed*slide_k, move_dir_flag * move_speed*slide_k, 
                        move_dir_flag * move_speed*slide_k, move_dir_flag * -move_speed*slide_k);
    }
    else if((change_speed_flag == 2) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * -move_speed_slow*slide_k, move_dir_flag * move_speed_slow*slide_k, 
                        move_dir_flag * move_speed_slow*slide_k, move_dir_flag * -move_speed_slow*slide_k);
    }
    else if((change_speed_flag == 3) && (change_speed_flag > change_speed_flag_pre)){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    change_speed_flag_pre = change_speed_flag;
    
    if(change_speed_flag == 1){
      PID_yaw();                      // 方向矫正
    }

    if(read_tof_flag >= read_tof_freq) {
      // PID_tof_y(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 移动到与当前位置相对dx的位置
// 从tof传感器（激光雷达）计算得到当前绝对位置
// 以x_dist作为移动目标条件，y_dist作为法向平移矫正
void move_dist_dx(double dx) {
  int read_tof_flag = 0;
  int change_speed_flag = 0;
  int change_speed_flag_pre = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  if(dx == 0) return;

  x_pre += dx;

  PID_tof_y(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();
  targetDist_tof_y = y_dist;

  double x_target = x_dist + dx;
  //Serial.println(x_dist);

  // 判断移动方向正负
  if(dx >= 0){
    move_dir_flag = 1;
  }
  else if(dx < 0){
    move_dir_flag = -1;
  }
  
//   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * -move_speed*slide_k, move_dir_flag * move_speed*slide_k, 
                    move_dir_flag * move_speed*slide_k, move_dir_flag * -move_speed*slide_k);
  while (1) {
    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
    }

    // 如果还未到指定位置
    sub_temp = move_dir_flag * (x_target - x_dist);
    if(sub_temp > dist_threshold_far) {
      // Serial.println("--------------------------------");
      change_speed_flag = 1;
    }
    else if(sub_temp > dist_threshold_close) {
      // Serial.println("--------------------------------");
      change_speed_flag = 2;
    }
    else{
      change_speed_flag = 3;
    }

    if((change_speed_flag == 1) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * -move_speed*slide_k, move_dir_flag * move_speed*slide_k, 
                        move_dir_flag * move_speed*slide_k, move_dir_flag * -move_speed*slide_k);
    }
    else if((change_speed_flag == 2) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * -move_speed_slow*slide_k, move_dir_flag * move_speed_slow*slide_k, 
                        move_dir_flag * move_speed_slow*slide_k, move_dir_flag * -move_speed_slow*slide_k);
    }
    else if((change_speed_flag == 3) && (change_speed_flag > change_speed_flag_pre)){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    change_speed_flag_pre = change_speed_flag;
    
    PID_yaw();                      // 方向矫正

    if(read_tof_flag >= read_tof_freq) {
      PID_tof_y(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}



// 移动到与当前位置相对dy的位置
// 从tof传感器（激光雷达）计算得到当前绝对位置
// 以y_dist作为移动目标条件，x_dist作为法向平移矫正
void move_dist_dy(double dy) {
  int read_tof_flag = 0;
  int change_speed_flag = 0;
  int change_speed_flag_pre = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;
  if(dy == 0) return;

  y_pre += dy;

  PID_tof_x(1);          // 重置PID参数

  // 获取当前绝对位置
  read_dist_tof_ros();
  targetDist_tof_x = x_dist;
  // Serial.println(targetDist_tof_x);

  double y_target = y_dist + dy;
  // Serial.println(y_dist);

  // 判断移动方向正负
  if(dy >= 0){
    move_dir_flag = 1;
  }
  else if(dy < 0){
    move_dir_flag = -1;
  }

//   double ky = dy / sqrt(pow(dx,2) + pow(dy,2));
  set_speed_target(move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed);
  while (1) {
    // 获取当前绝对位置
    if(read_tof_flag >= read_tof_freq) {
      read_dist_tof_ros();
      // Serial.println(y_dist);
    }

    // 如果还未到指定位置
    sub_temp = move_dir_flag * (y_target - y_dist);
    // Serial.println(sub_temp);
    if(sub_temp > dist_threshold_far) {
      change_speed_flag = 1;
    }
    else if(sub_temp > dist_threshold_close) {
      change_speed_flag = 2;
    }
    else {
      change_speed_flag = 3;
    }

    if((change_speed_flag == 1) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed, move_dir_flag * move_speed);
    }
    else if((change_speed_flag == 2) && (change_speed_flag > change_speed_flag_pre)) {
      set_speed_target(move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow, move_dir_flag * move_speed_slow);
    }
    else if((change_speed_flag == 3) && (change_speed_flag > change_speed_flag_pre)){
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      send_move_end();        // 发送移动结束信号
      break;
    }

    change_speed_flag_pre = change_speed_flag;
    
    PID_yaw();                      // 方向矫正

    if(read_tof_flag >= read_tof_freq) {
      // PID_tof_x(0);                 // 水平距离矫正
      read_tof_flag = 0;
    }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 矫正x轴，移动直到上位机要求停止
void move_compensate_x(int order_head) {
  int read_tof_flag = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;

  // PID_tof_y(1);          // 重置PID参数

  // // 获取当前绝对位置
  // read_dist_tof_ros();
  // targetDist_tof_y = y_dist;

  // read_bias();

//   // 判断移动方向正负
//   if(x_bias >= 0){
//     move_dir_flag = 1;
//     // if(x_bias > 0.08){
//     //   move_dist_time(x_bias/9.0, 0);
//     // }
//   }
//   else if(x_bias < 0){
//     move_dir_flag = -1;
//     // if(x_bias < -0.08){
//     //   move_dist_time(x_bias/9.0, 0);
//     // }
//   }
  
// //   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
//   set_speed_target(move_dir_flag * -move_compensate*slide_k, move_dir_flag * move_compensate*slide_k, 
//                     move_dir_flag * move_compensate*slide_k, move_dir_flag * -move_compensate*slide_k);
  while (1) {
    // 获取当前绝对位置
    // if(read_tof_flag >= read_tof_freq) {
    //   read_dist_tof_ros();
    // }
    // if(read_tof_flag >= 5) {
    //   read_bias();
    // }
    read_bias(order_head);

    // 判断移动方向正负
    if(x_bias >= 0){
      move_dir_flag = 1;
      // if(x_bias > 0.08){
      //   move_dist_time(x_bias/9.0, 0);
      // }
    }
    else if(x_bias < 0){
      move_dir_flag = -1;
      // if(x_bias < -0.08){
      //   move_dist_time(x_bias/9.0, 0);
      // }
    }
    
  //   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
    set_speed_target(move_dir_flag * -move_compensate*slide_k, move_dir_flag * move_compensate*slide_k, 
                      move_dir_flag * move_compensate*slide_k, move_dir_flag * -move_compensate*slide_k);

    // read_bias();
    // Serial.println(x_bias);

    // 如果还未到指定位置
    if(abs(x_bias) <= dist_compensate_close) {
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      // send_move_end();        // 发送移动结束信号
      break;
    }
    
    PID_yaw();                      // 方向矫正

    // if(read_tof_flag >= read_tof_freq) {
    //   PID_tof_y(0);                 // 水平距离矫正
    //   read_tof_flag = 0;
    // }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}


// 矫正y轴，移动直到上位机要求停止
void move_compensate_y(int order_head) {
  int read_tof_flag = 0;
  int move_dir_flag = 1;
  double sub_temp = 0.0;

  // read_bias();

//   // 判断移动方向正负
//   if(y_bias >= y_bias_target){
//     move_dir_flag = 1;
//     // if(x_bias > 0.08){
//     //   move_dist_time(x_bias/9.0, 0);
//     // }
//   }
//   else if(y_bias < y_bias_target){
//     move_dir_flag = -1;
//     // if(x_bias < -0.08){
//     //   move_dist_time(x_bias/9.0, 0);
//     // }
//   }
  
// //   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
//   set_speed_target(move_dir_flag * move_compensate, move_dir_flag * move_compensate, 
//                     move_dir_flag * move_compensate, move_dir_flag * move_compensate);
  while (1) {
    read_bias(order_head);

    // 判断移动方向正负
    if(y_bias >= 0){
      move_dir_flag = 1;
      // if(x_bias > 0.08){
      //   move_dist_time(x_bias/9.0, 0);
      // }
    }
    else if(y_bias < 0){
      move_dir_flag = -1;
      // if(x_bias < -0.08){
      //   move_dist_time(x_bias/9.0, 0);
      // }
    }
    
  //   double kx = dx / sqrt(pow(dx,2) + pow(dy,2));
    set_speed_target(move_dir_flag * move_compensate, move_dir_flag * move_compensate, 
                      move_dir_flag * move_compensate, move_dir_flag * move_compensate);

    // 如果还未到指定位置
    if(abs(y_bias) <= dist_compensate_close) {
      set_speed_target(0, 0, 0, 0);
      set_speed_to_stepper();
      move_read_flag = 0;

      // Serial.println("yesssssssss");
      // send_move_end();        // 发送移动结束信号
      break;
    }
    
    PID_yaw();                      // 方向矫正

    // if(read_tof_flag >= read_tof_freq) {
    //   PID_tof_y(0);                 // 水平距离矫正
    //   read_tof_flag = 0;
    // }

    set_speed_to_stepper();
    // Serial.println(y_dist);
    // run_speed();
    set_speed();

    read_tof_flag++;
  }
}