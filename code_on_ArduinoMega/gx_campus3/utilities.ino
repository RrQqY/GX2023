/* 这里存储一些其余功能的函数 */
#include "gx_campus3.h"


void delay_ms(long ms){
    unsigned long time_now = 0;

    time_now = millis();
    while(millis() < time_now + ms){
        ;
    }

}
