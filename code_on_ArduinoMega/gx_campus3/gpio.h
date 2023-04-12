#ifndef __GPIO_H
#define __GPIO_H

// 开始按钮
#define  start_key  45
    
// 七路IO口宏定义
#define  seven_front_1  49
#define  seven_front_2  47
#define  seven_front_3  43
#define  seven_front_4  41
#define  seven_front_5  39
#define  seven_front_6  37
#define  seven_front_7  35
#define  seven_back_1   A9
#define  seven_back_2   A10
#define  seven_back_3   A11
#define  seven_back_4   A12
#define  seven_back_5   A13
#define  seven_back_6   A14
#define  seven_back_7   A15
#define  seven_left_1   30
#define  seven_left_2   31
#define  seven_left_3   32
#define  seven_left_4   36
#define  seven_left_5   38
#define  seven_left_6   42
#define  seven_left_7   A0
#define  seven_right_1  A1
#define  seven_right_2  A2
#define  seven_right_3  A3
#define  seven_right_4  A4
#define  seven_right_5  A5
#define  seven_right_6  A6
#define  seven_right_7  A7


extern void seven_init();            // 七路初始化
extern int  seven_front(int num);    // 前七路
extern int  seven_back(int num);     // 后七路
extern int  seven_left(int num);     // 左七路
extern int  seven_right(int num);    // 右七路


#endif
