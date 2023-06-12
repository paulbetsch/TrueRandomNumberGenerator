import RPi.GPIO as GPIO
from time import sleep    
import time

# This methode allows to control the electric motor and the lifting magnet to power the pendulum.
# durationRunning: Time the motor and lifting magnet should run
def StartEngine(durationRunning, timeToWait):
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM) 
    
    # Configure Pin 6 & 13 as output that we can send digital 1 and 0 over this pins.
    # Pin 6 is connected to the relay and can toggle the circuit for the electric motor
    # Pin 13 toggles the circuit for the lifting magnet
    GPIO.setup(6, GPIO.OUT)  
    GPIO.setup(13, GPIO.OUT)  
    
    GPIO.output(6,0)
    GPIO.output(13,0)
    # Sleeps for the provided amount of time. While sleeping the motor is running
    sleep(durationRunning) 
    
    # Break the circuit for the relay modules for electric motor & lifting magnet
    GPIO.output(6,1)   
    GPIO.output(13,1) 
