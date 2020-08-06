# -*- coding: utf-8 -*-
"""
@author: Gus
Retrieved from
https://pimylifeup.com/raspberry-pi-rfid-rc522/
"""
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

try:
        text = input('New data:')
        print("Now place your tag to write")
        reader.write(text)
        print("Written")
finally:
        GPIO.cleanup()
