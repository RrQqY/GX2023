#!/usr/bin/python

#SwitchDoc Labs 2/22/14
# example driver for BM017 and TCS34725

import time
import smbus
from Adafruit_I2C import Adafruit_I2C
from SDL_PC_BM017CS import SDL_BM017


bm017 = SDL_BM017(True)

bm017.debug = True

bm017.readStatus()

bm017.isSDL_BM017There()

bm017.getColors()
bm017.readStatus()

bm017.disableDevice()
bm017.setIntegrationTimeAndGain(0x00, 0x03)

bm017.getColors()
bm017.readStatus()

bm017.readStatus()

# this will turn on the LED if LEDON is connected to INT and LEDVDD is connected to VDD_LED

bm017.setInterrupt(True)
time.sleep(1.0)
bm017.setInterrupt(False)


