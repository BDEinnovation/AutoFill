import RPi.GPIO as GPIO
import time
import datetime
import math

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 16
ECHO = 18

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

def init_output1(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)
   
def init_output2(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)
    GPIO.output(pin, GPIO.HIGH)

def pump1_on(pump_pin = 8, delay = 1):
    init_output1(pump_pin)
    print("Filling Water")
    f = open("last_watered.txt", "w")
    f.write("Last Filled {}".format(datetime.datetime.now().strftime("%m-%d-%Y, %I:%M %p")))
    f.close()
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(7) # time solenoid stays open
    GPIO.output(pump_pin, GPIO.HIGH)
   
def pump2_on(pump_pin = 10, delay = 1):
    init_output2(pump_pin)
    print("Filling Concentrate")
    GPIO.output(pump_pin, GPIO.LOW)
    time.sleep(1) # time solenoid stays open
    GPIO.output(pump_pin, GPIO.HIGH)
    
def clean_on(pump2_pin = 10, delay =1):
    init_output2(pump2_pin)
    print("Cleaning.....")
    f = open("last_cleaned.txt", "w")
    f.write("Last Cleaned {}".format(datetime.datetime.now().strftime("%m-%d-%Y, %I:%M %p")))
    f.close()
    GPIO.output(pump2_pin, GPIO.LOW)
    time.sleep(5) # time solenoid stays open
    GPIO.output(pump2_pin, GPIO.HIGH)

GPIO.setup(TRIG,GPIO.OUT)                  
GPIO.setup(ECHO,GPIO.IN)   

init_output1(8)
init_output2(10)

def auto_water():
    while True:

        GPIO.output(TRIG, False)                 
        print("Waiting For Sensor To Settle")
        time.sleep(5)                            

        GPIO.output(TRIG, True)                  
        time.sleep(0.00001)                      
        GPIO.output(TRIG, False)

        pulse_start = time.time()
        timeout = pulse_start + 0.04               
        while GPIO.input(ECHO)==0 and pulse_start < timeout:             
            pulse_start = time.time()             

        pulse_end = time.time()
        timeout = pulse_end + 0.04               
        while GPIO.input(ECHO)==1 and pulse_end < timeout:              
            pulse_end = time.time()                

        pulse_duration = pulse_end - pulse_start 

        distance = pulse_duration * 17150        
        distance = math.ceil(distance)            

        print('distance',distance)

        if distance > 10:
            pump1_on(8)
            pump2_on(10)