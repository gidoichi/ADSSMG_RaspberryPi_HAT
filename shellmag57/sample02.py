#!/usr/bin/env python3
import time
import RPi.GPIO as GPIO

from EbOled import EbOled
from TP401T import TP401T

BUZZER = 18

sensor = TP401T()
oled = EbOled()
oled.begin()
oled.clear()
oled.display()

# BUZZER
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUZZER, GPIO.OUT)
bz = GPIO.PWM(BUZZER, 1000)
bz.stop()

try:
  sensor.start()
  oled.drawString('待機中です')
  oled.display()
  while sensor.state == TP401T.WAITING: # 測定開始待ち
    time.sleep(3)

  while True:
    if sensor.state == TP401T.NORMAL:
      oled.drawString('空気は正常です')
    else:
      oled.drawString('汚染されています!!')

    if sensor.state == TP401T.ALERT:
      bz.start(50)
    else:
      bz.stop()

    oled.display()
    time.sleep(3)

except KeyboardInterrupt:
  sensor.stop() # センサー停止

GPIO.cleanup()
