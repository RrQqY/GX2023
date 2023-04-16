import RPi.GPIO as GPIO
import time
from PIL import Image

delay=2 #延时 2ms

pin_step = 14
pin_dir  = 15
 
GPIO.setmode(GPIO.BCM) #设置引脚的编码方式
   
def init():
    GPIO.setwarnings(False)
    GPIO.setup(pin_step, GPIO.OUT)
    GPIO.setup(pin_dir, GPIO.OUT)
 

def setStep(w1, w2):
  GPIO.output(pin_step, w1)
  GPIO.output(pin_dir, w2)


def zhengzhuan(delay):  
    setStep(1, 1)
    time.sleep(delay)
  

def fanzhuan(delay): 
    setStep(1, 0)
    time.sleep(delay)

p = int(input()) #输入想转的角度：1.360度  2.180度 3.135度 4.45度
init() 
while True:
  if p != 0:
    if p == 1:
        for i in range(0,512,1): #正转360度, 延时1秒, 反转360度
           zhengzhuan(int(delay) / 1000.0)
        time.sleep(1)
        for i in range(0,512,1):
            fanzhuan(int(delay) / 1000.0)

    if p == 2:
        for i in range(0,256,1): #正转180度, 延时1秒, 反转180度
            zhengzhuan(int(delay) / 1000.0)
        time.sleep(1)
        for i in range(0,256,1):
            fanzhuan(int(delay) / 1000.0)

    if p == 3:
        for i in range(0,192,1): #正转135度, 延时1秒, 反转135度
            fanzhuan(int(delay) / 1000.0)
        time.sleep(1)
        for i in range(0,192,1):
            zhengzhuan(int(delay) / 1000.0)

    if p == 4:
        for i in range(0,64,1):  #正转45度, 延时1秒, 反转45度
            fanzhuan(int(delay) / 1000.0)
        time.sleep(1)
        for i in range(0,64,1):
           zhengzhuan(int(delay) / 1000.0)
  break

GPIO.cleanup()
