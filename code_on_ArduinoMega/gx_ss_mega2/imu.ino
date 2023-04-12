/* 这里存储一些和IMU有关的函数 */
#include "gx_ss_mega2.h"

// IMU获取yaw角数据（用HWT101）
double get_yaw(){
  while(serial_imu.available()){
    JY901.CopeSerialData(serial_imu.read()); //Call JY901 data cope function
  }

  return -(double)JY901.stcAngle.Angle[2]/32768*180;
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
