/* 这里存储一些和底盘运动控制有关的函数 */
#include "gx_campus3.h"

// 创建4个编码器对象
Encoder ENC[4] = {
    Encoder(ENCODER_A, DIRECTION_A), Encoder(ENCODER_B, DIRECTION_B),
    Encoder(ENCODER_C, DIRECTION_C), Encoder(ENCODER_D, DIRECTION_D)};
long newPulses[4] = {0, 0, 0, 0};         // 四个车轮的定时中断编码器四倍频速度

// 编码器PID参数
float targetPulses[4] = {0, 0, 0, 0};     // 用于控制电机的目标脉冲数
float feedbackVel[4] = {0, 0, 0, 0};
double outPWM[4] = {0, 0, 0, 0};
// 创建4个速度PID控制对象
/*PID(float min_val, float max_val, float kp, float ki, float kd)
 * float min_val = min output PID value
 * float max_val = max output PID value
 * float kp = PID - P constant PID控制的比例、积分、微分系数
 * float ki = PID - I constant
 * float di = PID - D constant
 * Input	(double)输入参数feedbackVel，待控制的量
 * Output	(double)输出参数outPWM，指经过PID控制系统的输出量
 * Setpoint	(double)目标值targetVel，希望达到的数值
 */
PID VeloPID[4] = { PID(PWM_MIN, PWM_MAX, Kp, Ki, Kd), PID(PWM_MIN, PWM_MAX, Kp, Ki, Kd),
                   PID(PWM_MIN, PWM_MAX, Kp, Ki, Kd), PID(PWM_MIN, PWM_MAX, Kp, Ki, Kd)};


float targetYawPulses = 0;      // 用于控制车身的目标朝向角
int   is_brake = 0;                   // 为1则表示正在急停，为0则表示正常运动
int   is_turning = 0;                 // 为1则表示正在旋转，为0则表示正常运动
int   move_state = 1;                 // 运动状态，1为直行，2为后退，3为左移，4为右移
int   left_turn_num = 0;              // 左转次数

// 创建1个电池电压对象
Battery battery3S;


// 10ms定时中断函数，核心函数
void control() {
  sei();          // 全局中断开启

  // 获取电机速度
  #ifdef PINS_REVERSE
    newPulses[0] = -ENC[0].read();  // A
    newPulses[1] = ENC[1].read();   // B
    newPulses[2] = -ENC[2].read();  // C
    newPulses[3] = ENC[3].read();   // D
  #else
    newPulses[0] = ENC[0].read();   // A
    newPulses[1] = -ENC[1].read();  // B
    newPulses[2] = ENC[2].read();   // C
    newPulses[3] = -ENC[3].read();  // D
  #endif
  
  // 底盘电机编码器负反馈pid控制器
  for (int i = 0; i < WHEEL_NUM; i++) {
    feedbackVel[i] = (float)newPulses[i];
    outPWM[i] = VeloPID[i].Compute(targetPulses[i], feedbackVel[i]);
    ENC[i].write(0);    // 复位电机编码器速度为0
  }
  
  if(is_brake == 1) {        // 如果急停
    motors.motorsBrake();
  }
  else{                      // 如果正常运动
    if (battery3S.is_Volt_Low() == false) {
      motors.setSpeeds(outPWM[0], outPWM[1], outPWM[2], outPWM[3]);
    }
  }

}

// 带闭环控制的运动函数
void move_pid(int speed1, int speed2, int speed3, int speed4)
{
    if((speed1 != 0) || (speed2 != 0) || (speed3 != 0) || (speed4 != 0)){
      is_brake = 0;        // 取消急停模式
      
      targetPulses[0] = -speed1;
      targetPulses[1] = -speed2;
      targetPulses[2] = -speed3;
      targetPulses[3] = -speed4;
    }
}

// 直行
void forward(int line_count)
{
    int temp_count = 0;                     // 当前所在线数
    int flag = 0;                           // 开始计数标志

    move_state = 1;
    is_turning = 0;

    PID_forward(1);               // 重置PID内部参数
    
    // 先走一段，跨过黑线
    move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
    delay_ms(500);
    
    while (1) {   
      if ((seven_left(4) == LOW) && (seven_right(4) == LOW)) {                      // 检测到白色背景，开启计数准备
        flag = 1;
      }

      if (((flag == 1) && ((seven_left(7) == HIGH) && (seven_right(1) == HIGH))) && (temp_count == line_count - 1)) {   // 前部七路检测到黑线，先减速
        move_pid(forward_speed_slow, forward_speed_slow, forward_speed_slow, forward_speed_slow);
      }

      if ((flag == 1) && ((seven_left(4) == HIGH) || (seven_right(4) == HIGH))) {   // 由白色变为黑色线，计数一次
        delay_ms(10);
        if ((flag == 1) && ((seven_left(4) == HIGH) || (seven_right(4) == HIGH))) {   // 由白色变为黑色线，计数一次
          temp_count ++;          
  //        Serial.println(temp_count);                 
          flag = 0;
          if(temp_count < line_count){
            move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
            delay_ms(500);        // 先走一段，跨过黑线
          }
        }
      }
      
      // 数到对应的根数退出循环
      if (temp_count >= line_count) {
        brake();

        return;
      }

      PID_forward(0);
    }
}


// 后退
void back(int line_count)
{
    int temp_count = 0;                     // 当前所在线数
    int flag = 0;                           // 开始计数标志

    brake();
    resetPara();
    move_state = 2;
    is_turning = 0;

    PID_back(1);               // 重置PID内部参数
    
    // 先走一段，跨过黑线
    move_pid(-back_speed, -back_speed, -back_speed, -back_speed);
    delay_ms(500);
    
    while (1) {   
      if ((seven_left(4) == LOW) && (seven_right(4) == LOW)) {                      // 检测到白色背景，开启计数准备
        flag = 1;
      }

      if ((flag == 1) && ((seven_left(1) == HIGH) && (seven_right(7) == HIGH))) {   // 前部七路检测到黑线，先减速
        move_pid(-back_speed_slow, -back_speed_slow, -back_speed_slow, -back_speed_slow);
      }

      if ((flag == 1) && ((seven_left(4) == HIGH) && (seven_right(4) == HIGH))) {   // 由白色变为黑色线，计数一次
        delay_ms(20);
        if ((flag == 1) && ((seven_left(4) == HIGH) && (seven_right(4) == HIGH))) {   // 由白色变为黑色线，计数一次
          temp_count ++;          
  //        Serial.println(temp_count);                 
          flag = 0;
          if(temp_count < line_count){
            move_pid(-back_speed, -back_speed, -back_speed, -back_speed);
            delay_ms(500);        // 先走一段，跨过黑线
          }
        }
      }
      
      // 数到对应的根数退出循环
      if (temp_count >= line_count) {
        brake();
        return;
      }

      PID_back(0);
    }
}

// 急停
void brake()
{
    is_brake = 1;        // 设置为急停模式
    motors.setSpeeds(0,0,0,0);
    targetPulses[0] = 0;targetPulses[1] = 0;targetPulses[2] = 0;targetPulses[3] = 0;
    outPWM[0] = 0;outPWM[1] = 0;outPWM[2] = 0;outPWM[3] = 0;
//    Serial.println("@@@brake");
}

// 向左平移
void left(int line_count)
{
    int temp_count = 0;                     // 当前所在线数
    int flag = 0;                           // 开始计数标志

    brake();
    resetPara();
    move_state = 3;
    is_turning = 0;

    PID_left(1);               // 重置PID内部参数
    
    // 先走一段，跨过黑线
    move_pid(-left_speed, left_speed, left_speed, -left_speed);
    delay_ms(500);
    
    while (1) {   
      if ((seven_front(4) == LOW) && (seven_back(4) == LOW)) {                      // 检测到白色背景，开启计数准备
        flag = 1;
      }

      if ((flag == 1) && ((seven_front(1) == HIGH) && (seven_back(7) == HIGH))) {   // 前部七路检测到黑线，先减速
        move_pid(-left_speed_slow, left_speed_slow, left_speed_slow, -left_speed_slow);
      }

      if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
        delay_ms(20);
        if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
          temp_count ++;          
  //        Serial.println(temp_count);                 
          flag = 0;
          if(temp_count < line_count){
            move_pid(-left_speed, left_speed, left_speed, -left_speed);
            delay_ms(500);        // 先走一段，跨过黑线
          }
        }
      }
      
      // 数到对应的根数退出循环
      if (temp_count >= line_count) {
        brake();
        return;
      }

      PID_left(0);
    }
}

// 向右平移
void right(int line_count)
{
    int temp_count = 0;                     // 当前所在线数
    int flag = 0;                           // 开始计数标志

    brake();
    resetPara();
    move_state = 4;
    is_turning = 0;

    PID_right(1);               // 重置PID内部参数
    
    // 先走一段，跨过黑线
    move_pid(right_speed, -right_speed, -right_speed, right_speed);
    delay_ms(500);
    
    while (1) {   
      if ((seven_front(4) == LOW) && (seven_back(4) == LOW)) {                      // 检测到白色背景，开启计数准备
        flag = 1;
      }

      if ((flag == 1) && ((seven_front(7) == HIGH) && (seven_back(1) == HIGH))) {   // 前部七路检测到黑线，先减速
        move_pid(right_speed_slow, -right_speed_slow, -right_speed_slow, right_speed_slow);
      }

      if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
        delay_ms(20);
        if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
          temp_count ++;          
  //        Serial.println(temp_count);                 
          flag = 0;
          if(temp_count < line_count){
            move_pid(right_speed, -right_speed, -right_speed, right_speed);
            delay_ms(500);        // 先走一段，跨过黑线
          }
        }
      }
      
      // 数到对应的根数退出循环
      if (temp_count >= line_count) {
        brake();
        return;
      }

      PID_right(0);
    }
}


//// 用于陀螺仪矫正的10ms定时中断函数（测试用）
//void yaw_control() {
//  sei();      // 全局中断开启
//  // pid控制器
//  feedbackYawVel = get_yaw();
//  Serial.println(feedbackYawVel);
//  outYawPWM = YawPID.Compute(targetYawPulses, feedbackYawVel);
//
//  //电池电压正常的情况下启动电机并设置速度
//  if(is_brake == 1) {        // 如果急停
//    motors.motorsBrake();
//  }
//  else{                      // 如果正常运动
//    if (battery3S.is_Volt_Low() == false) {
//      if(outYawPWM > YawPWM_MAX){
//          outYawPWM = YawPWM_MAX;
//      }
//      motors.setSpeeds(-outYawPWM, outYawPWM, -outYawPWM, outYawPWM);
//    }
//  }
//}

// // 左转（用PID）
// void left_turn(float left_angle)
// {
//    is_brake = 0;
//    is_turning = 1;
//    targetYawPulses -= left_angle;

//    static float angle = 0;
//    static float target_angle = targetYawPulses;

//    move_pid(-left_turn_speed, left_turn_speed, -left_turn_speed, left_turn_speed);

//    while (1) {   
//       angle = get_yaw();
      
//       // 数到对应的根数退出循环
//       if (angle <= target_angle + pre_stop_turn) {
//         brake();
//         return;
//       }

//       PID_left_turn();
//     }
//   //  Serial.println("left_turn");
// }

// // 右转（用PID）
// void right_turn(float right_angle)
// {
//    is_brake = 0;
//    is_turning = 1;
//    targetYawPulses += right_angle;

//    static float angle = 0;
//    static float target_angle = targetYawPulses;

//    move_pid(right_turn_speed, -right_turn_speed, right_turn_speed, -right_turn_speed);

//    while (1) {   
//       angle = get_yaw();
      
//       // 数到对应的根数退出循环
//       if (angle >= target_angle - pre_stop_turn) {
//         brake();
//         return;
//       }

//       PID_right_turn();
//     }
//   //  Serial.println("right_turn");
// }

// 左转（不用PID）
void left_turn(float left_angle)
{
   is_brake = 0;
   is_turning = 1;
   targetYawPulses -= left_angle;

   static float angle = 0;
   static float target_angle = 0;
   target_angle = targetYawPulses + 3;
   
   // 开始左转
   move_pid(-left_turn_speed, left_turn_speed, -left_turn_speed, left_turn_speed);
//   Serial.println("left_turn");

   while (1) {   
      angle = get_yaw_pro_left(get_yaw());
//      Serial.println(angle);
      
      // 提前减速
      if (angle <= target_angle + pre_stop_turn) {
        move_pid(-(left_turn_speed-pre_slow_turn_speed), (left_turn_speed-pre_slow_turn_speed), 
                 -(left_turn_speed-pre_slow_turn_speed), (left_turn_speed-pre_slow_turn_speed));
      }
      // 数到对应的根数退出循环
      if (angle <= target_angle) {
        brake();
        left_turn_num ++;
        return;
      }

      delay_ms(10);
    }
}

// 右转（不用PID）
void right_turn(float right_angle)
{
   is_brake = 0;
   is_turning = 1;
   targetYawPulses += right_angle;

   static float angle = 0;
   static float target_angle = 0;
   target_angle = targetYawPulses - 3;
  
   // 开始右转
   move_pid(right_turn_speed, -right_turn_speed, right_turn_speed, -right_turn_speed);

   while (1) {   
      angle = get_yaw_pro_left(get_yaw());
      
      // 提前减速
      if (angle >= target_angle - pre_stop_turn) {
        move_pid((right_turn_speed-pre_slow_turn_speed), -(right_turn_speed-pre_slow_turn_speed), 
                 (right_turn_speed-pre_slow_turn_speed), -(right_turn_speed-pre_slow_turn_speed));
      }
      // 数到对应的根数退出循环
      if (angle >= target_angle) {
        brake();
        left_turn_num --;
        return;
      }

      delay_ms(10);
    }
  //  Serial.println("right_turn");
}


// 对正函数（在十字节点处，姿态端正时将四七路中间灰度对线）
void align()
{
  /*    陀螺仪部分    */
  // 陀螺仪PID参数
  static float newYawPulses_align = 0;         // 四个车轮的定时中断编码器四倍频速度
  static float feedbackYawVel_align = 0;
  static double outYawPWM_align = 0;
  static double outYawPWM_old_align = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_align = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  /*    水平方向矫正    */
  while(1){
    // 如果偏右
    if((seven_front(1) == HIGH) || (seven_front(2) == HIGH) || (seven_front(3) == HIGH)){
      move_pid(-left_speed_align, left_speed_align, left_speed_align, -left_speed_align);

      // 陀螺仪矫正pid控制器
      feedbackYawVel_align = get_yaw_pro_left(get_yaw());
    //  Serial.println(feedbackYawVel);
      outYawPWM_align = YawPID_align.Compute(targetYawPulses, feedbackYawVel_align);
      if(outYawPWM_align > YawPWM_MAX){
          outYawPWM_align = YawPWM_MAX;
      }  
    
      // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
      targetPulses[0] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[1] += (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[2] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[3] += (outYawPWM_align - outYawPWM_old_align)/5;

      outYawPWM_old_align = outYawPWM_align;

      delay_ms(5);
    }
    // 如果偏左
    else if((seven_front(5) == HIGH) || (seven_front(6) == HIGH) || (seven_front(7) == HIGH)){
      move_pid(right_speed_align, -right_speed_align, -right_speed_align, right_speed_align);

      // 陀螺仪矫正pid控制器
      feedbackYawVel_align = get_yaw_pro_left(get_yaw());
    //  Serial.println(feedbackYawVel);
      outYawPWM_align = YawPID_align.Compute(targetYawPulses, feedbackYawVel_align);
      if(outYawPWM_align > YawPWM_MAX){
          outYawPWM_align = YawPWM_MAX;
      }  
    
      // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
      targetPulses[0] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[1] += (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[2] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[3] += (outYawPWM_align - outYawPWM_old_align)/5;

      outYawPWM_old_align = outYawPWM_align;
      // 陀螺仪矫正pid控制器
      feedbackYawVel_align = get_yaw_pro_left(get_yaw());
    //  Serial.println(feedbackYawVel);
      outYawPWM_align = YawPID_align.Compute(targetYawPulses, feedbackYawVel_align);
      if(outYawPWM_align > YawPWM_MAX){
          outYawPWM_align = YawPWM_MAX;
      }  
    
      // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
      targetPulses[0] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[1] += (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[2] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[3] += (outYawPWM_align - outYawPWM_old_align)/5;

      outYawPWM_old_align = outYawPWM_align;
      delay_ms(5);
    }
    else if(seven_front(4) == HIGH){
      delay_ms(1);
      if(seven_front(4) == HIGH){
        break;  
      }
    }
  }
  delay_ms(100);
  brake();
  
  /*    垂直方向矫正    */
  while(1){
    // 如果偏上
    if((seven_right(1) == HIGH) || (seven_right(2) == HIGH) || (seven_right(3) == HIGH)){
      move_pid(forward_speed_align, forward_speed_align, forward_speed_align, forward_speed_align);

      // 陀螺仪矫正pid控制器
      feedbackYawVel_align = get_yaw_pro_left(get_yaw());
    //  Serial.println(feedbackYawVel);
      outYawPWM_align = YawPID_align.Compute(targetYawPulses, feedbackYawVel_align);
      if(outYawPWM_align > YawPWM_MAX){
          outYawPWM_align = YawPWM_MAX;
      }  
    
      // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
      targetPulses[0] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[1] += (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[2] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[3] += (outYawPWM_align - outYawPWM_old_align)/5;

      outYawPWM_old_align = outYawPWM_align;

      delay_ms(5);
    }
    // 如果偏下
    else if((seven_right(5) == HIGH) || (seven_right(6) == HIGH) || (seven_right(7) == HIGH)){
      move_pid(-back_speed_align, -back_speed_align, -back_speed_align, -back_speed_align);

      // 陀螺仪矫正pid控制器
      feedbackYawVel_align = get_yaw_pro_left(get_yaw());
    //  Serial.println(feedbackYawVel);
      outYawPWM_align = YawPID_align.Compute(targetYawPulses, feedbackYawVel_align);
      if(outYawPWM_align > YawPWM_MAX){
          outYawPWM_align = YawPWM_MAX;
      }  
    
      // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
      targetPulses[0] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[1] += (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[2] -= (outYawPWM_align - outYawPWM_old_align)/5;
      targetPulses[3] += (outYawPWM_align - outYawPWM_old_align)/5;

      outYawPWM_old_align = outYawPWM_align;
      
      delay_ms(5);
    }
    else if(seven_right(4) == HIGH){
      delay_ms(5);
      if(seven_right(4) == HIGH){
        break;  
      }
    }
  }
  delay_ms(100);
  brake();

  return ;
}

//// 用于七路水平矫正的10ms定时中断函数（测试用）
//void seven_control() 
//{
//  sei();      // 全局中断开启
//  // pid控制器
//  feedbackSevenVel = get_seven(1);
//  Serial.println(feedbackSevenVel);
//  outSevenPWM = SevenPID.Compute(targetSevenPulses, feedbackSevenVel);
//
//  //电池电压正常的情况下启动电机并设置速度
//  if(is_brake == 1) {        // 如果急停
//    motors.motorsBrake();
//  }
//  else{                      // 如果正常运动
//    if (battery3S.is_Volt_Low() == false) {
//      if(outSevenPWM > SevenPWM_MAX){
//          outSevenPWM = SevenPWM_MAX;
//      }
//      motors.setSpeeds(outSevenPWM, -outSevenPWM, -outSevenPWM, outSevenPWM);
//    }
//  }
//}

// 前进方向的PID
void PID_forward(int clear_flag)
{
  /*    七路部分    */
  // 七路PID参数
  // static double targetSevenPulses_forward = 0;      // 用于控制车身的目标朝向角
  // static double feedbackSevenVel_forward = 0;
  double outSevenPWM_forward = 0;
  static double outSevenPWM_old_forward = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID SevenPID_forward = PID(PWM_MIN, PWM_MAX, Kp_seven, Ki_seven, Kd_seven);

  // 陀螺仪PID参数
  static double newYawPulses_forward = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_forward = 0;
  static double outYawPWM_forward = 0;
  static double outYawPWM_old_forward = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_forward = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // // 七路水平矫正pid控制器
  // feedbackSevenVel_forward = get_seven(1);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outSevenPWM_forward = 0;
    outSevenPWM_old_forward = 0;
    outYawPWM_forward = 0;
    outYawPWM_old_forward = 0;
  }
  else{
    //  Serial.println(targetSevenPulses);
    outSevenPWM_forward = SevenPID_forward.Compute(0, get_seven(1));
    // outSevenPWM_forward = SevenPID_forward.Compute(targetSevenPulses_forward, feedbackSevenVel_forward);
    if(outSevenPWM_forward > SevenPWM_MAX){
        outSevenPWM_forward = SevenPWM_MAX;
    }
    
    // 将七路矫正速度加到编码器目标速度上，除5（6.4）是为了将PWM转换为编码器脉冲数
    targetPulses[0] += (outSevenPWM_forward - outSevenPWM_old_forward)/5;
    targetPulses[1] -= (outSevenPWM_forward - outSevenPWM_old_forward)/5;
    targetPulses[2] -= (outSevenPWM_forward - outSevenPWM_old_forward)/5;
    targetPulses[3] += (outSevenPWM_forward - outSevenPWM_old_forward)/5;
    
    outSevenPWM_old_forward = outSevenPWM_forward;

    // Serial.println(outSevenPWM_forward);

    /*    陀螺仪部分    */
    // 陀螺仪矫正pid控制器
    feedbackYawVel_forward = get_yaw_pro_left(get_yaw());
  //  Serial.println(feedbackYawVel);
    outYawPWM_forward = YawPID_forward.Compute(targetYawPulses, feedbackYawVel_forward);
    if(outYawPWM_forward > YawPWM_MAX){
        outYawPWM_forward = YawPWM_MAX;
    }  
  
    // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outYawPWM_forward - outYawPWM_old_forward)/5;
    targetPulses[1] += (outYawPWM_forward - outYawPWM_old_forward)/5;
    targetPulses[2] -= (outYawPWM_forward - outYawPWM_old_forward)/5;
    targetPulses[3] += (outYawPWM_forward - outYawPWM_old_forward)/5;

    outYawPWM_old_forward = outYawPWM_forward;

    delay_ms(5);
  }
}


// 后退方向的PID
void PID_back(int clear_flag)
{
  /*    七路部分    */
  // 七路PID参数
  static double newSevenPulses_back = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double targetSevenPulses_back = 0;      // 用于控制车身的目标朝向角
  static double feedbackSevenVel_back = 0;
  static double outSevenPWM_back = 0;
  static double outSevenPWM_old_back = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID SevenPID_back = PID(PWM_MIN, PWM_MAX, Kp_seven, Ki_seven, Kd_seven);

  // 陀螺仪PID参数
  static double newYawPulses_back = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_back = 0;
  static double outYawPWM_back = 0;
  static double outYawPWM_old_back = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_back = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outSevenPWM_back = 0;
    outSevenPWM_old_back = 0;
    outYawPWM_back = 0;
    outYawPWM_old_back = 0;
  }
  else{
    // 七路水平矫正pid控制器
    feedbackSevenVel_back = get_seven(2);
      
  //  Serial.println(targetSevenPulses);
    outSevenPWM_back = SevenPID_back.Compute(targetSevenPulses_back, feedbackSevenVel_back);
    if(outSevenPWM_back > SevenPWM_MAX){
        outSevenPWM_back = SevenPWM_MAX;
    }
    
    // 将七路矫正速度加到编码器目标速度上，除5（6.4）是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outSevenPWM_back - outSevenPWM_old_back)/5;
    targetPulses[1] += (outSevenPWM_back - outSevenPWM_old_back)/5;
    targetPulses[2] += (outSevenPWM_back - outSevenPWM_old_back)/5;
    targetPulses[3] -= (outSevenPWM_back - outSevenPWM_old_back)/5;

    outSevenPWM_old_back = outSevenPWM_back;

    /*    陀螺仪部分    */
    // 陀螺仪矫正pid控制器
    feedbackYawVel_back = get_yaw_pro_left(get_yaw());
  //  Serial.println(feedbackYawVel);
    outYawPWM_back = YawPID_back.Compute(targetYawPulses, feedbackYawVel_back);
    if(outYawPWM_back > YawPWM_MAX){
        outYawPWM_back = YawPWM_MAX;
    }  
  
    // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outYawPWM_back - outYawPWM_old_back)/5;
    targetPulses[1] += (outYawPWM_back - outYawPWM_old_back)/5;
    targetPulses[2] -= (outYawPWM_back - outYawPWM_old_back)/5;
    targetPulses[3] += (outYawPWM_back - outYawPWM_old_back)/5;

    outYawPWM_old_back = outYawPWM_back;

    delay_ms(10);
  }
}

// 左移方向的PID
void PID_left(int clear_flag)
{
  /*    七路部分    */
  // 七路PID参数
  static double newSevenPulses_left = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double targetSevenPulses_left = 0;      // 用于控制车身的目标朝向角
  static double feedbackSevenVel_left = 0;
  static double outSevenPWM_left = 0;
  static double outSevenPWM_old_left = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID SevenPID_left = PID(PWM_MIN, PWM_MAX, Kp_seven, Ki_seven, Kd_seven);

  // 陀螺仪PID参数
  static double newYawPulses_left = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_left = 0;
  static double outYawPWM_left = 0;
  static double outYawPWM_old_left = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_left = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outSevenPWM_left = 0;
    outSevenPWM_old_left = 0;
    outYawPWM_left = 0;
    outYawPWM_old_left = 0;
  }
  else{
    // 七路水平矫正pid控制器
    feedbackSevenVel_left = get_seven(3);
      
  //  Serial.println(targetSevenPulses);
    outSevenPWM_left = SevenPID_left.Compute(targetSevenPulses_left, feedbackSevenVel_left);
    if(outSevenPWM_left > SevenPWM_MAX){
        outSevenPWM_left = SevenPWM_MAX;
    }
    
    // 将七路矫正速度加到编码器目标速度上，除5（6.4）是为了将PWM转换为编码器脉冲数
    targetPulses[0] += (outSevenPWM_left - outSevenPWM_old_left)/6.4;
    targetPulses[1] += (outSevenPWM_left - outSevenPWM_old_left)/6.4;
    targetPulses[2] += (outSevenPWM_left - outSevenPWM_old_left)/6.4;
    targetPulses[3] += (outSevenPWM_left - outSevenPWM_old_left)/6.4;

    outSevenPWM_old_left = outSevenPWM_left;

    /*    陀螺仪部分    */
    // 陀螺仪矫正pid控制器
    feedbackYawVel_left = get_yaw_pro_left(get_yaw());
  //  Serial.println(feedbackYawVel);
    outYawPWM_left = YawPID_left.Compute(targetYawPulses, feedbackYawVel_left);
    if(outYawPWM_left > YawPWM_MAX){
        outYawPWM_left = YawPWM_MAX;
    }  
  
    // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outYawPWM_left - outYawPWM_old_left)/5;
    targetPulses[1] += (outYawPWM_left - outYawPWM_old_left)/5;
    targetPulses[2] -= (outYawPWM_left - outYawPWM_old_left)/5;
    targetPulses[3] += (outYawPWM_left - outYawPWM_old_left)/5;

    outYawPWM_old_left = outYawPWM_left;

    delay_ms(10);
  }
}

// 右移方向的PID
void PID_right(int clear_flag)
{  
  /*    七路部分    */
  // 七路PID参数
  static double newSevenPulses_right = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double targetSevenPulses_right = 0;      // 用于控制车身的目标朝向角
  static double feedbackSevenVel_right = 0;
  static double outSevenPWM_right = 0;
  static double outSevenPWM_old_right = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID SevenPID_right = PID(PWM_MIN, PWM_MAX, Kp_seven, Ki_seven, Kd_seven);

  // 陀螺仪PID参数
  static double newYawPulses_right = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_right = 0;
  static double outYawPWM_right = 0;
  static double outYawPWM_old_right = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_right = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outSevenPWM_right = 0;
    outSevenPWM_old_right = 0;
    outYawPWM_right = 0;
    outYawPWM_old_right = 0;
  }
  else{
    // 七路水平矫正pid控制器
    feedbackSevenVel_right = get_seven(4);
      
  //  Serial.println(targetSevenPulses);
    outSevenPWM_right = SevenPID_right.Compute(targetSevenPulses_right, feedbackSevenVel_right);
    if(outSevenPWM_right > SevenPWM_MAX){
        outSevenPWM_right = SevenPWM_MAX;
    }
    
    // 将七路矫正速度加到编码器目标速度上，除5（6.4）是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outSevenPWM_right - outSevenPWM_old_right)/6.4;
    targetPulses[1] -= (outSevenPWM_right - outSevenPWM_old_right)/6.4;
    targetPulses[2] -= (outSevenPWM_right - outSevenPWM_old_right)/6.4;
    targetPulses[3] -= (outSevenPWM_right - outSevenPWM_old_right)/6.4;

    outSevenPWM_old_right = outSevenPWM_right;

    /*    陀螺仪部分    */
    // 陀螺仪矫正pid控制器
    feedbackYawVel_right = get_yaw_pro_left(get_yaw());
  //  Serial.println(feedbackYawVel);
    outYawPWM_right = YawPID_right.Compute(targetYawPulses, feedbackYawVel_right);
    if(outYawPWM_right > YawPWM_MAX){
        outYawPWM_right = YawPWM_MAX;
    }  
  
    // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outYawPWM_right - outYawPWM_old_right)/5;
    targetPulses[1] += (outYawPWM_right - outYawPWM_old_right)/5;
    targetPulses[2] -= (outYawPWM_right - outYawPWM_old_right)/5;
    targetPulses[3] += (outYawPWM_right - outYawPWM_old_right)/5;

    outYawPWM_old_right = outYawPWM_right;

    delay_ms(10);
  }
}


// 左转的PID
void PID_left_turn()
{
  /*    陀螺仪部分    */
  // 陀螺仪PID参数
  static double newYawPulses_left_turn = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_left_turn = 0;
  static double outYawPWM_left_turn = 0;
  static double outYawPWM_old_left_turn = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_left_turn = PID(PWM_MIN, 14, Kp_yaw_turn, Ki_yaw_turn, Kd_yaw_turn);

  // 陀螺仪矫正pid控制器
  feedbackYawVel_left_turn = get_yaw_pro_left(get_yaw());
  outYawPWM_left_turn = YawPID_left_turn.Compute(targetYawPulses, feedbackYawVel_left_turn);
  if(outYawPWM_left_turn > YawPWM_turn_MAX){
      outYawPWM_left_turn = YawPWM_turn_MAX;
  }  
 
  // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
  targetPulses[0] -= (outYawPWM_left_turn - outYawPWM_old_left_turn)/25;
  targetPulses[1] += (outYawPWM_left_turn - outYawPWM_old_left_turn)/25;
  targetPulses[2] -= (outYawPWM_left_turn - outYawPWM_old_left_turn)/25;
  targetPulses[3] += (outYawPWM_left_turn - outYawPWM_old_left_turn)/25;

  outYawPWM_old_left_turn = outYawPWM_left_turn;
}

// 右转的PID
void PID_right_turn()
{
  /*    陀螺仪部分    */
  // 陀螺仪PID参数
  static double newYawPulses_right_turn = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_right_turn = 0;
  static double outYawPWM_right_turn = 0;
  static double outYawPWM_old_right_turn = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_right_turn = PID(PWM_MIN, 14, Kp_yaw_turn, Ki_yaw_turn, Kd_yaw_turn);

  // 陀螺仪矫正pid控制器
  feedbackYawVel_right_turn = get_yaw_pro_left(get_yaw());
//  Serial.println(feedbackYawVel);
  outYawPWM_right_turn = YawPID_right_turn.Compute(targetYawPulses, feedbackYawVel_right_turn);
  if(outYawPWM_right_turn > YawPWM_turn_MAX){
      outYawPWM_right_turn = YawPWM_turn_MAX;
  }  
 
  // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
  targetPulses[0] += (outYawPWM_right_turn - outYawPWM_old_right_turn)/25;
  targetPulses[1] -= (outYawPWM_right_turn - outYawPWM_old_right_turn)/25;
  targetPulses[2] += (outYawPWM_right_turn - outYawPWM_old_right_turn)/25;
  targetPulses[3] -= (outYawPWM_right_turn - outYawPWM_old_right_turn)/25;

  outYawPWM_old_right_turn = outYawPWM_right_turn;
}


// 获得七路读取值（加权和）
int get_seven(int witch)
{ 
  int sense_value = 0;
  double error = 0;

  switch(witch){
      case 1: sense_value = 1 * seven_front(1) + 4 * seven_front(2) + 7 * seven_front(3) + 10 * seven_front(4) + 
                      13 * seven_front(5) + 16 * seven_front(6) + 19 * seven_front(7); break;
      case 2: sense_value = 1 * seven_back(1) + 4 * seven_back(2) + 7 * seven_back(3) + 10 * seven_back(4) + 
                      13 * seven_back(5) + 16 * seven_back(6) + 19 * seven_back(7); break;
      case 3: sense_value = 1 * seven_left(1) + 4 * seven_left(2) + 7 * seven_left(3) + 10 * seven_left(4) + 
                      13 * seven_left(5) + 16 * seven_left(6) + 19 * seven_left(7); break;
      case 4: sense_value = 1 * seven_right(1) + 4 * seven_right(2) + 7 * seven_right(3) + 10 * seven_right(4) + 
                      13 * seven_right(5) + 16 * seven_right(6) + 19 * seven_right(7); break;
      default: sense_value = 0; break;
  }

  switch (sense_value) {
      case 1:  error = -4; break;          // 1
      case 5:  error = -3.8; break;        // 1 2
      case 4:  error = -3.6;   break;      // 2
      case 12:  error = -3.6; break;       // 1 2 3
      case 11:  error = -3.4;   break;     // 2 3
      case 7:  error = -3; break;        // 3
      case 21: error = -3;   break;      // 2 3 4 
      case 17:  error = -2.6;    break;    // 3 4
      case 10: error = 0;    break;        // 4
      case 30:  error = 0;  break;         // 3 4 5
      case 23: error = 2.6;    break;      // 4 5
      case 13: error = 3;  break;        // 5
      case 39: error = 3;    break;      // 4 5 6
      case 29: error = 3.4;  break;        // 5 6
      case 16: error = 3.6;  break;        // 6
      case 48: error = 3.6;  break;        // 5 6 7
      case 35: error = 3.8;  break;        // 6 7
      case 19: error = 4;  break;          // 7
      default: if(error == 4) error = 4.2;
               else if(error == -4) error = -4.2;
               break;
    }

  return error;
}

// 重置所有PID变量
void resetPara()
{
    VeloPID[0].UpdateParameters();
    VeloPID[1].UpdateParameters();
    VeloPID[2].UpdateParameters();
    VeloPID[3].UpdateParameters();
//    YawPID.UpdateParameters();
//    SevenPID.UpdateParameters();
    targetPulses[0] = 0;targetPulses[1] = 0;targetPulses[2] = 0;targetPulses[3] = 0;
    outPWM[0] = 0;outPWM[1] = 0;outPWM[2] = 0;outPWM[3] = 0;
//    newYawPulses = 0;
//    newSevenPulses = 0; targetSevenPulses = 0; 
}


// 右移至右七路压线
void right_to_rs()
{
    brake();
    resetPara();
    move_state = 4;
    is_turning = 0;

    PID_right(1);               // 重置PID内部参数

    move_pid(right_speed_slow, -right_speed_slow, -right_speed_slow, right_speed_slow);
    delay_ms(200);
    
    while (1) {   
      if ((seven_right(1) == HIGH) && (seven_right(7) == HIGH)) {   // 由白色变为黑色线，计数一次  
        delay_ms(10);           
        if ((seven_right(1) == HIGH) && (seven_right(7) == HIGH)) {   // 由白色变为黑色线，计数一次          
  //        Serial.println(temp_count);  
          delay_ms(20);
          brake();
          forward_align_ls();
          return;               
        }         
      }

      PID_right(0);
    }
}

// 右移至左七路压线
void right_to_ls()
{
    brake();
    resetPara();
    move_state = 4;
    is_turning = 0;

    PID_right(1);               // 重置PID内部参数

    move_pid(right_speed_slow, -right_speed_slow, -right_speed_slow, right_speed_slow);
    delay_ms(200);
    
    while (1) {   
      if ((seven_left(1) == HIGH) && (seven_left(7) == HIGH)) {   // 由白色变为黑色线，计数一次 
        delay_ms(10);       
        if ((seven_left(1) == HIGH) && (seven_left(7) == HIGH)) {   // 由白色变为黑色线，计数一次       
  //        Serial.println(temp_count);  
          brake();
          forward_align_rs();
          return;               
        }           
      }

      PID_right(0);
    }
}

// 左移至右七路压线
void left_to_rs()
{
    brake();
    resetPara();
    move_state = 3;
    is_turning = 0;

    PID_left(1);               // 重置PID内部参数

    move_pid(-left_speed_slow, left_speed_slow, left_speed_slow, -left_speed_slow);
    delay_ms(200);
    
    while (1) {   
      if ((seven_right(1) == HIGH) && (seven_right(7) == HIGH)) {   // 由白色变为黑色线，计数一次   
        delay_ms(10);        
        if ((seven_right(1) == HIGH) && (seven_right(7) == HIGH)) {   // 由白色变为黑色线，计数一次         
  //        Serial.println(temp_count);  
          brake();
          forward_align_ls();
          return;               
        }          
      }

      PID_left(0);
    }
}

// 左移至左七路压线
void left_to_ls()
{
    brake();
    resetPara();
    move_state = 3;
    is_turning = 0;

    PID_left(1);               // 重置PID内部参数

    move_pid(-left_speed_slow, left_speed_slow, left_speed_slow, -left_speed_slow);
    delay_ms(200);
    
    while (1) {   
      if ((seven_left(1) == HIGH) && (seven_left(7) == HIGH)) {   // 由白色变为黑色线，计数一次
        delay_ms(10);        
        if ((seven_left(1) == HIGH) && (seven_left(7) == HIGH)) {   // 由白色变为黑色线，计数一次       
  //        Serial.println(temp_count);  
          brake();
          forward_align_rs();
          return;               
        }   
      }

      PID_left(0);
    }
}


// 直行方向上矫准（用左七路）
void forward_align_ls()
{
    move_state = 1;
    is_turning = 0;

    PID_forward(1);               // 重置PID内部参数
    PID_back(1);                  // 重置PID内部参数

    while (1) {   
      if ((seven_left(1) == HIGH) || (seven_left(2) == HIGH) || (seven_left(3) == HIGH)) {   // 由白色变为黑色线，计数一次
        if (seven_left(4) == HIGH) {   // 由白色变为黑色线，计数一次       
          delay_ms(50);              
          if (seven_left(4) == HIGH) {   // 由白色变为黑色线，计数一次                   
            brake();
            return;
          }
        }
        move_pid(-back_speed_slow, -back_speed_slow, -back_speed_slow, -back_speed_slow);
        PID_back(0);
      }
      else if ((seven_left(5) == HIGH) || (seven_left(6) == HIGH) || (seven_left(7) == HIGH)) {   // 由白色变为黑色线，计数一次
        if (seven_left(4) == HIGH) {   // 由白色变为黑色线，计数一次                 
          delay_ms(50);              
          if (seven_left(4) == HIGH) {   // 由白色变为黑色线，计数一次                 
            brake();
            return;
          }
        }
        move_pid(forward_speed_slow, forward_speed_slow, forward_speed_slow, forward_speed_slow);
        PID_forward(0);
      }
      else {
        brake();
        return;
      }
    }
}

// 直行方向上矫准（用右七路）
void forward_align_rs()
{
    move_state = 1;
    is_turning = 0;

    PID_forward(1);               // 重置PID内部参数
    PID_back(1);                  // 重置PID内部参数

    while (1) {   
      if ((seven_right(1) == HIGH) || (seven_right(2) == HIGH) || (seven_right(3) == HIGH)) {   // 由白色变为黑色线，计数一次
        if (seven_right(4) == HIGH) {   // 由白色变为黑色线，计数一次     
  //        Serial.println(temp_count);                 
          delay_ms(50);              
          if (seven_right(4) == HIGH) {   // 由白色变为黑色线，计数一次     
  //        Serial.println(temp_count);                 
            brake();
            return;
          }
        }
        move_pid(forward_speed_slow, forward_speed_slow, forward_speed_slow, forward_speed_slow);
        PID_forward(0);
      }
      else if ((seven_right(5) == HIGH) || (seven_right(6) == HIGH) || (seven_right(7) == HIGH)) {   // 由白色变为黑色线，计数一次
        if (seven_right(4) == HIGH) {   // 由白色变为黑色线，计数一次     
  //        Serial.println(temp_count);                 
          delay_ms(50);              
          if (seven_right(4) == HIGH) {   // 由白色变为黑色线，计数一次     
  //        Serial.println(temp_count);                 
            brake();
            return;
          }
        }
        move_pid(-back_speed_slow, -back_speed_slow, -back_speed_slow, -back_speed_slow);
        PID_back(0);
      }
      else {
        brake();
        return;
      }
    }
}

//---------------------------------------------------------------------------------------------------
// 斜走
void slant(int line_count)
{
    int temp_count = 0;                     // 当前所在线数
    int flag = 0;                           // 开始计数标志

    move_state = 5;
    is_turning = 0;

    PID_slant(1);               // 重置PID内部参数
    
    // 先走一段，跨过黑线
    move_pid(forward_speed_slant-left_speed, forward_speed_slant+left_speed, forward_speed_slant+left_speed, forward_speed_slant-left_speed);
    delay_ms(1000);
    
    while (1) {   
      if ((seven_front(4) == LOW) && (seven_back(4) == LOW)) {                      // 检测到白色背景，开启计数准备
        flag = 1;
      }

      if ((flag == 1) && ((seven_front(1) == HIGH) && (seven_back(7) == HIGH))) {   // 前部七路检测到黑线，先减速
        move_pid(forward_speed_slant_slow-left_speed_slow, forward_speed_slant_slow+left_speed_slow, forward_speed_slant_slow+left_speed_slow, forward_speed_slant_slow-left_speed_slow);
      }

      if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
        delay_ms(20);
        if ((flag == 1) && ((seven_front(4) == HIGH) && (seven_back(4) == HIGH))) {   // 由白色变为黑色线，计数一次
          temp_count ++;          
  //        Serial.println(temp_count);                 
          flag = 0;
          if(temp_count < line_count){
            move_pid(forward_speed_slant-left_speed, forward_speed_slant+left_speed, forward_speed_slant+left_speed, forward_speed_slant-left_speed);
            delay_ms(500);        // 先走一段，跨过黑线
          }
        }
      }
      
      // 数到对应的根数退出循环
      if (temp_count >= line_count) {
        brake();
        return;
      }

      PID_slant(0);
    }
}
// 斜向的PID
void PID_slant(int clear_flag)
{
  /*    七路部分    */
  // 七路PID参数
  // static double targetSevenPulses_forward = 0;      // 用于控制车身的目标朝向角
  // static double feedbackSevenVel_forward = 0;
  double outSevenPWM_slant = 0;
  static double outSevenPWM_old_slant = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID SevenPID_slant = PID(PWM_MIN, PWM_MAX, Kp_seven, Ki_seven, Kd_seven);

  // 陀螺仪PID参数
  static double newYawPulses_slant = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_slant = 0;
  static double outYawPWM_slant = 0;
  static double outYawPWM_old_slant = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_slant = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // // 七路水平矫正pid控制器
  // feedbackSevenVel_forward = get_seven(1);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outSevenPWM_slant = 0;
    outSevenPWM_old_slant = 0;
    outYawPWM_slant = 0;
    outYawPWM_old_slant = 0;
  }
  else{
//    //  Serial.println(targetSevenPulses);
//    outSevenPWM_forward = SevenPID_forward.Compute(0, get_seven(1));
//    // outSevenPWM_forward = SevenPID_forward.Compute(targetSevenPulses_forward, feedbackSevenVel_forward);
//    if(outSevenPWM_forward > SevenPWM_MAX){
//        outSevenPWM_forward = SevenPWM_MAX;
//    }
//    
//    // 将七路矫正速度加到编码器目标速度上，除5（6.4）是为了将PWM转换为编码器脉冲数
//    targetPulses[0] += (outSevenPWM_forward - outSevenPWM_old_forward)/5;
//    targetPulses[1] -= (outSevenPWM_forward - outSevenPWM_old_forward)/5;
//    targetPulses[2] -= (outSevenPWM_forward - outSevenPWM_old_forward)/5;
//    targetPulses[3] += (outSevenPWM_forward - outSevenPWM_old_forward)/5;
//    
//    outSevenPWM_old_forward = outSevenPWM_forward;

    // Serial.println(outSevenPWM_forward);

    /*    陀螺仪部分    */
    // 陀螺仪矫正pid控制器
    feedbackYawVel_slant = get_yaw_pro_left(get_yaw());
  //  Serial.println(feedbackYawVel);
    outYawPWM_slant = YawPID_slant.Compute(targetYawPulses, feedbackYawVel_slant);
    if(outYawPWM_slant > YawPWM_MAX){
        outYawPWM_slant = YawPWM_MAX;
    }  
  
    // 将陀螺仪矫正速度加到编码器目标速度上，除5是为了将PWM转换为编码器脉冲数
    targetPulses[0] -= (outYawPWM_slant - outYawPWM_old_slant)/5;
    targetPulses[1] += (outYawPWM_slant - outYawPWM_old_slant)/5;
    targetPulses[2] -= (outYawPWM_slant - outYawPWM_old_slant)/5;
    targetPulses[3] += (outYawPWM_slant - outYawPWM_old_slant)/5;

    outYawPWM_old_slant = outYawPWM_slant;

    delay_ms(5);
  }
}


void forward_end(int line_count){
  int temp_count = 0;                     // 当前所在线数
  int flag = 0;                           // 开始计数标志

  move_state = 1;
  is_turning = 0;

  PID_forward(1);               // 重置PID内部参数
  
  // 先走一段，跨过黑线
  move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
  delay_ms(500);
  
  while (1) {   
    if ((seven_back(1) == LOW) && (seven_back(7) == LOW)) {                      // 检测到白色背景，开启计数准备
      flag = 1;
    }

    if ((flag == 1) && ((seven_back(1) == HIGH) && (seven_back(7) == HIGH))) {   // 由白色变为黑色线，计数一次
      delay_ms(10);
      if ((flag == 1) && ((seven_back(1) == HIGH) && (seven_back(7) == HIGH))) {   // 由白色变为黑色线，计数一次
        temp_count ++;          
//        Serial.println(temp_count);                 
        flag = 0;
        if(temp_count < line_count){
          move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
          delay_ms(500);        // 先走一段，跨过黑线
        }
      }
    }
    
    // 数到对应的根数退出循环
    if (temp_count >= line_count) {
      brake();

      return;
    }

    PID_forward(0);
  }
}

void forward_scanCode(int line_count){
  int temp_count = 0;                     // 当前所在线数
  int flag = 0;                           // 开始计数标志

  move_state = 1;
  is_turning = 0;

  PID_forward(1);               // 重置PID内部参数
  
  // // 先走一段，跨过黑线
   move_pid(12, 12, 12, 12);
  // delay_ms(500);
  
  while (1) {   
    if ((seven_back(1) == LOW) && (seven_back(7) == LOW)) {                      // 检测到白色背景，开启计数准备
      flag = 1;
    }

    if ((flag == 1) && ((seven_back(1) == HIGH) && (seven_back(7) == HIGH))) {   // 由白色变为黑色线，计数一次
      delay_ms(10);
      if ((flag == 1) && ((seven_back(1) == HIGH) && (seven_back(7) == HIGH))) {   // 由白色变为黑色线，计数一次
        temp_count ++;          
//        Serial.println(temp_count);                 
        flag = 0;
      }
    }
    
    // 数到对应的根数退出循环
    if (temp_count >= line_count) {
      brake();

      return;
    }

    PID_forward(0);
  }
}

//出发
void base_start(){
 // 先走一段，跨过黑线
 move_pid(-left_speed, left_speed, left_speed, -left_speed);
 delay_ms(500);
 left(1);
 delay_ms(200);
 forward(2);
 delay_ms(200);
}


//返回
void base_end(){
 forward_end(2);
 delay_ms(200);
 move_pid(right_speed, -right_speed, -right_speed, right_speed);
 delay_ms(1500);
 move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
 delay_ms(200);
}


//斜着返回
void slant_end(){
 move_pid(forward_speed_slant+right_speed, forward_speed_slant-right_speed, forward_speed_slant-right_speed, forward_speed_slant+right_speed);
 delay_ms(2200);
 move_pid(right_speed, -right_speed, -right_speed, right_speed);
 delay_ms(500);
 move_pid(forward_speed, forward_speed, forward_speed, forward_speed);
 delay_ms(500);
 brake();
}
