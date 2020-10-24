# External module imp
import RPi.GPIO as GPIO
import datetime
import time

init = False

GPIO.setmode(GPIO.BOARD) # Broadcom pin-numbering scheme

def get_last_watered():
    try:
        f = open("last_watered.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
    
def get_last_cleaned():
    try:
        f = open("last_cleaned.txt", "r")
        return f.readline()
    except:
        return "NEVER!"
      
def get_status(pin = 11):
    GPIO.setup(pin, GPIO.IN) 
    return GPIO.input(pin)

def init_output1(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
   
def init_output2(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH) 
    
def auto_water(delay = 1, pump1_pin = 8, pump2_pin = 10, water_sensor_pin = 11): # delay = time between cycles
    consecutive_water_count = 0
    init_output1(pump1_pin)
    init_output2(pump2_pin)
    
    print("Here we go! Press CTRL+C to exit")
    try:
        while 1 and consecutive_water_count < 99999999:
            time.sleep(delay)
            wet = get_status(pin = water_sensor_pin) == 0
            if not wet:
                if consecutive_water_count < 99999999: # number of cycles
                    pump1_on(pump1_pin, 0)
                    pump2_on(pump2_pin,0)
                consecutive_water_count += 1
            else:
                consecutive_water_count = 0
    except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
        GPIO.cleanup() # cleanup all GPI

def pump1_on(pump_pin = 8, delay = 1):
    init_output1(pump_pin)
    f = open("last_watered.txt", "w")
    f.write("Last Filled {}".format(datetime.datetime.now().strftime("%m-%d-%Y, %I:%M %p")))
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(2) # time solenoid stays open
    GPIO.output(pump_pin, GPIO.HIGH)
   
def pump2_on(pump_pin = 10, delay = 1):
    init_output2(pump_pin)
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(1) # time solenoid stays open
    GPIO.output(pump_pin, GPIO.HIGH)
    
def clean_on(pump2_pin = 10, delay =1):
    init_output2(pump2_pin)
    f = open("last_cleaned.txt", "w")
    f.write("Last Cleaned {}".format(datetime.datetime.now().strftime("%m-%d-%Y, %I:%M %p")))
    f.close()
    GPIO.output(pump2_pin, GPIO.LOW)
    time.sleep(5) # time solenoid stays open
    GPIO.output(pump2_pin, GPIO.HIGH)
    