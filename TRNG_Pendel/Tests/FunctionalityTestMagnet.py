from ina219 import INA219
from ina219 import DeviceRangeError
import time
import RPi.GPIO as GPIO

SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2
"""
Checks the Functionalty of the Magnet
"""
def read():
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    ina.configure(ina.RANGE_16V)


    current = ina.current()*-1
    voltage = ina.shunt_voltage()*-1
    #print("Current:" + str(current))
    #print("Voltage:" + str(voltage))

    if voltage<5:
        GPIO.output(13,1)      
        return False
    
    GPIO.output(13,1)   
    return True
        
      
def checkIt():
    GPIO.setwarnings(False)
    
    GPIO.setmode(GPIO.BCM)
    
    #Magnet
    GPIO.setup(13, GPIO.OUT)  
         
    while True:
        GPIO.output(13,0)   
        return read()
