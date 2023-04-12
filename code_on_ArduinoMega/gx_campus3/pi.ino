/* 这里存储一些和与上位机通信有关的函数 */
#include "gx_campus3.h"

// 向树莓派发送命令
/* 1. 上位机扫描二维码
   2. 上位机识别货架颜色
   3. 上位机抓取货物①
   4. 上位机放下货物②
   5. 上位机抓取货物③
   6. 上位机放下货物④
   7. 上位机抓取货物⑤
   8. 上位机放下货物⑥    */
void order_pi(int order)
{
  switch(order){
    case 0: Serial2.write("0"); delay_ms(50); break;
    case 1: Serial2.write("1"); delay_ms(50); break;
    case 2: Serial2.write("2"); delay_ms(50); break;
    case 3: Serial2.write("3"); delay_ms(50); break;
    case 4: Serial2.write("4"); delay_ms(50); break;
    case 5: Serial2.write("5"); delay_ms(50); break;
    case 6: Serial2.write("6"); delay_ms(50); break;
    case 7: Serial2.write("7"); delay_ms(50); break;
    case 8: Serial2.write("8"); delay_ms(50); break;
    case 9: Serial2.write("9"); delay_ms(50); break;
  }  
}
