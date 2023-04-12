/* 这里存储一些和底盘运动控制有关的函数 */
#include "gx_ss_test.h"


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
int   left_turn_num = 0;        // 左转次数


// 带闭环控制的运动函数
void run_speed(int speed1, int speed2, int speed3, int speed4) {
  targetPulses[0] = speed1;
  targetPulses[1] = speed2;
  targetPulses[2] = speed3;
  targetPulses[3] = speed4;
}


// 通过串口1向Esp32发送电机速度
void set_speed(int speed1, int speed4, int speed2, int speed3) {
  // speed1：左上；speed4：右上；speed2：左下；speed3：右下
  speed1 = speed1;
  speed2 = speed2;

  // 底盘电机速度字符串
  char speed1_buf[4];
  char speed2_buf[4];
  char speed3_buf[4];
  char speed4_buf[4];

  sprintf(speed1_buf, "%d", speed1);
  esp32_serial.write(speed1_buf);
  esp32_serial.write(",");
  sprintf(speed2_buf, "%d", speed2);
  esp32_serial.write(speed2_buf);
  esp32_serial.write(",");
  sprintf(speed3_buf, "%d", speed3);
  esp32_serial.write(speed3_buf);
  esp32_serial.write(",");
  sprintf(speed4_buf, "%d", speed4);
  esp32_serial.write(speed4_buf);
  esp32_serial.write("@");

  delay_ms(10);
}


// // 10ms定时中断函数
// void control() {
//   set_speed(targetPulses[0], targetPulses[1], targetPulses[2], targetPulses[3]); 
// }


// 直行
void forward() {
    // 重置PID内部参数
    PID_forward(1);      
    run_speed(-3000,-3000,-3000,-3000);         
    
    while (1) {   
    //   // 数到对应的根数退出循环
    //   if (temp_count >= line_count) {
    //     brake();
    //     return;
    //   }

      PID_forward(0);
    }
}


// 前进方向的PID
void PID_forward(int clear_flag) {
  static double newYawPulses_forward = 0;         // 四个车轮的定时中断编码器四倍频速度
  static double feedbackYawVel_forward = 0;
  static double outYawPWM_forward = 0;
  static double outYawPWM_old_forward = 0;
  // 创建1个陀螺仪速度PID控制对象
  static PID YawPID_forward = PID(PWM_MIN, PWM_MAX, Kp_yaw, Ki_yaw, Kd_yaw);

  // 每重新开始一次巡线，重置上一次的所有变量
  if(clear_flag == 1){
    outYawPWM_forward = 0;
    outYawPWM_old_forward = 0;
  }
  else{
    // 陀螺仪矫正pid控制器
    feedbackYawVel_forward = get_yaw_pro_left(get_yaw());

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

    set_speed(targetPulses[0], targetPulses[1], targetPulses[2], targetPulses[3]); 

    delay_ms(5);
  }
}