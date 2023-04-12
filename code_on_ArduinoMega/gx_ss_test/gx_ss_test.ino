/*-------- 2023.03工程训练大赛省赛测试代码 --------*/

#include "gx_ss_test.h"

#define esp32_serial Serial1
#define imu_serial   Serial2
#define pi2_serial   Serial3


void setup() {
  // 串口初始化
  Serial.begin(9600);
  esp32_serial.begin(9600);    // 串口1用于向Esp32发送数据以控制底盘速度
  imu_serial.begin(115200);      // 串口2用于从IMU接收数据
  pi2_serial.begin(9600);      // 串口3用于从树莓派2接收激光雷达数据 
  // 串口2用于从树莓派1接收相机数据 

  // IMU初始化
  // imu_setup();

  // MsTimer2::set(200, control);
  // MsTimer2::start();                     // 中断使能
  // delay(100);                               // 延时等待初始化完成

}


// 开始函数
void start() {
  // // 控制底盘停止运动
  // set_speed(0,0,0,0);
  // delay_ms(1000);

  // Serial.println("stop");

  // forward();


  // unsigned long stime = millis();
  set_speed(2000, 2000, 2000, 2000); 
  delay_ms(500);
  // unsigned long etime = millis();

  // Serial.println((unsigned long)(etime-stime));

  // Serial.println(speed0+i*200);
  // delay_ms(1000);
  set_speed(0,0,0,0);                   // 通过串口1向Esp32发送电机速度
    // delay_ms(5);
    // read_capture_flag_color();     // 准备从转盘上抓取时，从串口2中读取树莓派1回传的抓取标志和颜色信息
    // read_target_bias();            // 在靶标前时，从串口2中读取树莓派1回传的位置偏差信息
    // read_lidar_dist();             // 从串口3读取车中心距离前侧墙壁和右侧墙壁的距离
}


void loop() {
  start();                                      // 运行开始阶段函数
  while(1){};
}
