/*-------- 2023.03工程训练大赛省赛Esp32代码 --------*/
#include "gx_ss_mega.h"

// 串口定义
#define serial_imu    Serial1
#define serial_pi1    Serial2
#define serial_pi2    Serial3

// 软串口定义
// SoftwareSerial serial_tof1(53, 45);      // 软串口（前RX后TX）
// SoftwareSerial serial_tof2(52, 44);
// SoftwareSerial serial_tof3(51, 43);
// SoftwareSerial serial_tof4(50, 42);
DFRobot_IICSerial serial_tof1(Wire, SUBUART_CHANNEL_1, /*IA1 = */0, /*IA0 = */0);
DFRobot_IICSerial serial_tof2(Wire, SUBUART_CHANNEL_2, /*IA1 = */0, /*IA0 = */0);
DFRobot_IICSerial serial_tof3(Wire, SUBUART_CHANNEL_1, /*IA1 = */1, /*IA0 = */0);
DFRobot_IICSerial serial_tof4(Wire, SUBUART_CHANNEL_2, /*IA1 = */1, /*IA0 = */0);

// 定义步进电机对象
AccelStepper stepper1(1, motor1STEP, motor1DIR);
AccelStepper stepper2(1, motor2STEP, motor2DIR);
AccelStepper stepper3(1, motor3STEP, motor3DIR);
AccelStepper stepper4(1, motor4STEP, motor4DIR);


// 步进电机初始化
void motor_setup() {
  // 1号步进电机
  pinMode(motor1EN, OUTPUT);        // Arduino控制2208步进引脚为输出模式
  pinMode(motor1STEP, OUTPUT);      // Arduino控制2208方向引脚为输出模式
  pinMode(motor1DIR, OUTPUT);       // Arduino控制2208使能引脚为输出模式
  digitalWrite(motor1EN, LOW);      // 将使能控制引脚设置为低电平从而让电机驱动板进入工作状态

  stepper1.setPinsInverted(HIGH, false, true);   // 步进电机初始正转向为顺时针
  stepper1.setMaxSpeed(20000.0);      // 电机最大速度20000 
  stepper1.setAcceleration(acc);    // 电机加速度100.0
  // stepper1.setSpeed(3000);            // 电机速度3000
  // stepper1.moveTo(10000);

  // 2号步进电机
  pinMode(motor2EN, OUTPUT);
  pinMode(motor2STEP, OUTPUT);
  pinMode(motor2DIR, OUTPUT);
  digitalWrite(motor2EN, LOW);

  stepper2.setPinsInverted(HIGH, false, true);
  stepper2.setMaxSpeed(20000.0);
  stepper2.setAcceleration(acc);
  // stepper2.setSpeed(3000);
  // stepper2.moveTo(10000);

  // 3号步进电机
  pinMode(motor3EN, OUTPUT);
  pinMode(motor3STEP, OUTPUT);
  pinMode(motor3DIR, OUTPUT);
  digitalWrite(motor3EN, LOW);

  stepper3.setPinsInverted(HIGH, false, true);
  stepper3.setMaxSpeed(20000.0);
  stepper3.setAcceleration(acc);
  // stepper3.setSpeed(3000);
  // stepper3.moveTo(10000);

  // 4号步进电机
  pinMode(motor4EN, OUTPUT);
  pinMode(motor4STEP, OUTPUT);
  pinMode(motor4DIR, OUTPUT);
  digitalWrite(motor4EN, LOW);

  stepper4.setPinsInverted(HIGH, false, true);
  stepper4.setMaxSpeed(20000.0);
  stepper4.setAcceleration(acc);
  // stepper4.setSpeed(3000);
  // stepper4.moveTo(10000);
}


// // 10ms定时中断函数
// void control() {
//   sei();          // 全局中断开启

//   unsigned long mMillis;
//   unsigned long cMillis = millis();

//   // 每次设定电机速度时，循环执行run_delay_time时间的runSpeed
//   while(1){
//     run_speed();
//     mMillis = millis();
//     if(mMillis-cMillis >= 6){
//       break;
//     }
//   }
// }


void setup() {
  // 步进电机初始化
  motor_setup();

  // 串口初始化
  Serial.begin(9600);

  serial_imu.begin(115200);
  serial_pi1.begin(115200);
  serial_pi2.begin(115200);
  
  serial_tof1.begin(115200);
  serial_tof2.begin(115200);
  serial_tof3.begin(115200);
  serial_tof4.begin(115200);

  // IIC初始化
  JY901.StartIIC();

  // FlexiTimer2::set(10, control);  // 10毫秒定时中断函数
  // FlexiTimer2::start();                     // 中断使能
  // delay(100);                               // 延时等待初始化完成
}


// 开始函数
void start() {
    // speed1=2000;
    // speed2=2000;
    // speed3=2000;
    // speed4=2000;

  // unsigned long stime = millis();
  
  // while(1){
  //   long stime = millis();

  //   // read_dist_order();
  //   PID_yaw();
  //   set_speed(speed1, speed2, speed3, speed4);
  
  //   // Serial.println(etime-stime);
  // }

  // set_speed_target(speed1, speed2, speed3, speed4);
  // set_speed_to_stepper();
  // // 每次设定电机速度时，循环执行run_delay_time时间的runSpeed
  // while(1){
  //   PID_yaw();
  //   set_speed_to_stepper();
  //   run_speed();
  // }

  // move_dist_time(1, 0);
  // read_move_order();
  // move_dist_time(1, 0);
  // while(1){
  //   unsigned long stime = millis();
  //   read_dist_tof_ros();
  //   unsigned long etime = millis();
  //   Serial.print(x_dist);
  //   Serial.print(", "); 
  //   Serial.print(y_dist); 
  //   Serial.print(", "); 
  //   Serial.println(etime-stime);
  // }
  // Serial.print(x_move); 

  // move_dist_dy(1);

  while(1){
    // 从串口中读取移动指令
    read_move_order();

    // 如果接收到移动指令
    if(move_read_flag == 1){
      if((x_move != 0.0) && (y_move == 0.0)){
        move_dist_dx(x_move);
      }
      else if((x_move == 0.0) && (y_move != 0.0)){
        move_dist_dy(y_move);
      }
    }
  }
}


void loop() { 
  start();                  // 运行开始阶段函数

  while(1){};
}
