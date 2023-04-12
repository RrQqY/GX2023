/* 这里存储一些和IMU有关的函数 */
#include "gx_ss_mega2.h"

double yaw_list[] = {0.0, 0.0, 0.0, 0.0, 0.0, 0.0};

double yaw_start = 0.0;
double yaw_end = 0.0;
double yaw_bias = 0.0;

// IMU获取yaw角数据（用HWT101）
double get_yaw(int origin_flag = 0){
  double yaw_pre = 0.0;
  double yaw_res = 0.0;
  while(serial_imu.available()){
    JY901.CopeSerialData(serial_imu.read()); //Call JY901 data cope function
  }
  
  yaw_pre = -(double)JY901.stcAngle.Angle[2]/32768*180;

  // 滑动加权滤波
  for(int i = 1; i < 6; i++){
    yaw_list[i] = yaw_list[i-1];
  }

  // 与上一次角度大于5°的则为异常值，删去
  if(abs(yaw_pre - yaw_list[1]) < 2.5){
    yaw_list[0] = yaw_pre;
  }
  else{
    yaw_list[0] = yaw_list[1];
  }

  yaw_res = (6.0*yaw_list[0] + 5.0*yaw_list[1] + 4.0*yaw_list[2] + 3.0*yaw_list[3] + 2.0*yaw_list[4] + 1.0*yaw_list[5]) / 21.0 - yaw_bias;
  // Serial.print(yaw_list[0]);
  // Serial.print("@");
  // Serial.print(yaw_list[1]);
  // Serial.print("@");
  // Serial.println(yaw_res);
  if(origin_flag == 1){
    // 读五次值, 取平均, 去除异常值
    double values[5] = {};
    int i = 0;
    double sum = 0.0;
    double average = 0.0;
    // 读五次值
    for (i = 0; i < 5; i++) {
        values[i] = -(double)JY901.stcAngle.Angle[2]/32768*180;
        delay_ms(20);
        // Serial.println(values[i]);
    }
    // 计算平均值
    for (i = 0; i < 5; i++) {
        sum += values[i];
    }
    average = sum / 5.0;
    // 去除异常值
    for (i = 0; i < 5; i++) {
        if (abs(values[i] - average) > 2) {
            // 如果某个值是异常值，则用平均值代替
            values[i] = 400;
        }
    }
    // 计算去除异常值后的平均值
    sum = 0.0;
    int num = 0;
    for (i = 0; i < 5; i++) {
      if(values[i] != 400){
        sum += values[i];
        num += 1;
      }
    }
    average = sum / double(num);

    return average;
  }
  else{
    return yaw_res;
  }
}

// double get_yaw(){
//     JY901.GetAngle();
//     return (double)JY901.stcAngle.Angle[2]/32768*180;
// }


// // IMU yaw角数据处理
// // 由于IMU返回值为(-180~180)，而targetYaw为累计值可能超过180，需要对IMU返回数据进行处理
// double get_yaw_pro(double yaw){
//   double yaw = 0.0;
//   double yaw_pro = 0.0;
  
//   // 读取原始yaw角数据
//   JY901.GetAngle();
//   yaw = (double)JY901.stcAngle.Angle[2]/32768*180;

//   // 当出发第一周时（转第2、3、4、5个左转）
//   if((left_turn_num > 1) && (left_turn_num <= 5)){
//     if(left_turn_num == 2){    // 第2个左转，此时目标为-180度，会出现-180和180的跳变，额外判断
//       if(yaw < 0){
//         return yaw;
//       }
//       else if(yaw > 0){
//         yaw_pro = yaw - 360;
//         return yaw_pro;
//       }
//     }
//     else{
//       yaw_pro = yaw - 360;
//       return yaw_pro;
//     }
//   } 
//   // 当出发第二周时（转第6、7、8个左转）
//   else if((left_turn_num > 5) && (left_turn_num <= 9)){
//     if(left_turn_num == 6){    // 第6个左转，此时目标为-180度，会出现-180和180的跳变，额外判断
//       if(yaw < 0){
//         yaw_pro = yaw - 360;
//         return yaw_pro;
//       }
//       else if(yaw > 0){
//         yaw_pro = yaw - 360*2;
//         return yaw_pro;
//       }
//     }
//     else{
//       yaw_pro = yaw - 360*2;
//       return yaw_pro;
//     }
//   }
//   else{
//     return yaw;
//   }
// }
