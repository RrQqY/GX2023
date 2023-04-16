#coding:utf-8

from __future__ import absolute_import
import time
import serial
import cv2
import numpy as np
import struct
import sys
import RPi.GPIO as GPIO

light = 40

GPIO.setmode(GPIO.BOARD) #BMC或者BOARD模式

GPIO.setup(light, GPIO.OUT)

GPIO.output(light, GPIO.HIGH)
# time.sleep(1)
# GPIO.output(light, GPIO.LOW)

