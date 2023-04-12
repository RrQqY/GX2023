/* 2022.09工程训练大赛校赛代码 */
#include "gx_campus3.h"

A4950MotorShield motors;
#define  decay   0.85


void setup()
{
  // 串口初始化
  Serial.begin(BAUDRATE);
  Serial2.begin(115200);        // 与树莓派上位机通信串口初始化
  Serial3.begin(115200);        // 与IMU通信串口初始化

  // IMU初始化
  imu_setup();

  // 底盘电机初始化
  motors.init();       //电机初始化，初始化引脚模式和pwm频率和电机死区
  delay(100);                               // 延时等待初始化完成
  FlexiTimer2::set(TIMER_PERIOD, control);  // 10毫秒定时中断函数
  FlexiTimer2::start();                     // 中断使能
  delay(100);                               // 延时等待初始化完成

  // 底盘IO初始化
  pinMode(start_key, INPUT);    // 开始按钮初始化
  seven_init();                 // 七路初始化
}


// 第一次出发
void turn1()
{
  // 从基地中斜向移出
  slant(1);
  delay_ms(400);
//  back(0);
//  delay_ms(400);

  forward_scanCode(1);
  delay_ms(1200);

  order_pi(1);
  delay_ms(2000);

  forward(4);
  delay_ms(800);

  order_pi(2);
  delay_ms(3000);

  right_to_rs();
  delay_ms(800);

  order_pi(3);
  delay_ms(22000);

  left(1);
  delay_ms(400);

  forward(1);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);

  forward(2);
  delay_ms(800);

  left_to_rs();
  delay_ms(800);

  order_pi(4);
  delay_ms(20500);

  order_pi(5);
  delay_ms(28000);

  right(1);
  delay_ms(800);

  forward(2);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);

  forward(3);
  delay_ms(800);

  right_to_ls();
  delay_ms(800);

  order_pi(6);
  delay_ms(26000);

  left(1);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);

  forward(4);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);
}

// 第二次出发
void turn2()
{
  forward(2);
  delay_ms(800);

  right_to_rs();
  delay_ms(800);

  order_pi(7);
  delay_ms(24000);

  left(1);
  delay_ms(800);

  forward(1);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);

  forward(2);
  delay_ms(800);

  left_to_rs();
  delay_ms(800);

  order_pi(4);
  delay_ms(20500);

  order_pi(5);
  delay_ms(27000);

  right(1);
  delay_ms(800);

  forward(2);
  delay_ms(800);

  left_turn(90);
  delay_ms(800);

  forward(3);
  delay_ms(800);

  right_to_ls();
  delay_ms(800);

  order_pi(8);
  delay_ms(27000);

  left(1);
  delay_ms(800);

  forward(2);
  delay_ms(800);

  order_pi(9);
  delay_ms(800);

  slant_end();
}


// 准备函数
void prepare()
{

}


// 开始函数
void start()
{
//  move_pid(255, 255, 255, 255);
//  forward(2);
//  delay_ms(800);
//  back(2);
//  delay_ms(800);
//  forward(1);
//  delay_ms(800);
//
  order_pi(0);
  turn1();
  turn2();
}


void loop()
{
//  prepare();                                        // 运行准备阶段函数
  while(1){
    if(digitalRead(start_key) == HIGH){
      start();                                      // 运行开始阶段函数
      break;
    }
    else if(digitalRead(start_key) == LOW){
      ;
    }
  }

  while(1){ 
  };
}
