import water
import web_plants
import RPi.GPIO as GPIO
import time
import datetime

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 16
ECHO = 18

if __name__ == "__main__":
    water.auto_water()