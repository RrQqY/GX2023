/* 这里存储一些和IO接口有关的函数封装，以便其他文件直接调用 */
#include "gx_campus3.h"

// 七路初始化
void seven_init()
{
    pinMode(seven_front_1, INPUT);
    pinMode(seven_front_2, INPUT);
    pinMode(seven_front_3, INPUT);
    pinMode(seven_front_4, INPUT);
    pinMode(seven_front_5, INPUT);
    pinMode(seven_front_6, INPUT);
    pinMode(seven_front_7, INPUT);
    pinMode(seven_back_1, INPUT);
    pinMode(seven_back_2, INPUT);
    pinMode(seven_back_3, INPUT);
    pinMode(seven_back_4, INPUT);
    pinMode(seven_back_5, INPUT);
    pinMode(seven_back_6, INPUT);
    pinMode(seven_back_7, INPUT);
    pinMode(seven_left_1, INPUT);
    pinMode(seven_left_2, INPUT);
    pinMode(seven_left_3, INPUT);
    pinMode(seven_left_4, INPUT);
    pinMode(seven_left_5, INPUT);
    pinMode(seven_left_6, INPUT);
    pinMode(seven_left_7, INPUT);
    pinMode(seven_right_1, INPUT);
    pinMode(seven_right_2, INPUT);
    pinMode(seven_right_3, INPUT);
    pinMode(seven_right_4, INPUT);
    pinMode(seven_right_5, INPUT);
    pinMode(seven_right_6, INPUT);
    pinMode(seven_right_7, INPUT);
}

// 前七路
int seven_front(int num)
{
    switch(num){
      case 1: return digitalRead(seven_front_1); break;
      case 2: return digitalRead(seven_front_2); break;
      case 3: return digitalRead(seven_front_3); break;
      case 4: return digitalRead(seven_front_4); break;
      case 5: return digitalRead(seven_front_5); break;
      case 6: return digitalRead(seven_front_6); break;
      case 7: return digitalRead(seven_front_7); break;
      default: break;
    }
}

// 后七路
int seven_back(int num)
{
    switch(num){
      case 1: return digitalRead(seven_back_1); break;
      case 2: return digitalRead(seven_back_2); break;
      case 3: return digitalRead(seven_back_3); break;
      case 4: return digitalRead(seven_back_4); break;
      case 5: return digitalRead(seven_back_5); break;
      case 6: return digitalRead(seven_back_6); break;
      case 7: return digitalRead(seven_back_7); break;
      default: break;
    }
}

// 左七路
int seven_left(int num)
{
    switch(num){
      case 1: return digitalRead(seven_left_1); break;
      case 2: return digitalRead(seven_left_2); break;
      case 3: return digitalRead(seven_left_3); break;
      case 4: return digitalRead(seven_left_4); break;
      case 5: return digitalRead(seven_left_5); break;
      case 6: return digitalRead(seven_left_6); break;
      case 7: return digitalRead(seven_left_7); break;
      default: break;
    }
}

// 右七路
int seven_right(int num)
{
    switch(num){
      case 1: return digitalRead(seven_right_1); break;
      case 2: return digitalRead(seven_right_2); break;
      case 3: return digitalRead(seven_right_3); break;
      case 4: return digitalRead(seven_right_4); break;
      case 5: return digitalRead(seven_right_5); break;
      case 6: return digitalRead(seven_right_6); break;
      case 7: return digitalRead(seven_right_7); break;
      default: break;
    }
}
