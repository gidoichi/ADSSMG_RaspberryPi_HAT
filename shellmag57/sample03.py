#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO
import threading

from EbOled import EbOled
from  VCNL4020 import  VCNL4020

BUZZER = 18

term = False
sensor = VCNL4020()
oled = EbOled()
oled.begin()
oled.clear()
oled.display()

def prox():
  global term

  GPIO.setmode(GPIO.BCM)
  GPIO.setup(BUZZER, GPIO.OUT)
  bz = GPIO.PWM(BUZZER, 1000)

  while term == False:
    if sensor.proximity > 4000:
      bz.start(50)
    else:
      bz.stop()
    time.sleep(0.1)

  GPIO.cleanup(BUZZER)


t = threading.Thread(target=prox)
t.start()

try:
  while True:
    oled.drawString('明るさ: ' + str(sensor.luminance) +' lux')
    oled.display()
    time.sleep(0.2)
except KeyboardInterrupt:
  term = True
