/* 这里存储一些其余功能的函数 */
#include "gx_ss_mega2.h"


void delay_ms(unsigned long ms){
    unsigned long time_now = 0;

    time_now = millis();
    while(millis() < time_now + ms){
        ;
    }
}


// double max(double a, double b, double c, double d) {
//   if(a >= b && a >= c && a >= d){
//     return a;
//   }
//   else if(b >= a && b >= c && b >= d){
//     return a;
//   }
//   else if(c >= a && c >= b && c >= d){
//     return a;
//   }
//   else{
//     return a;
//   }
// }