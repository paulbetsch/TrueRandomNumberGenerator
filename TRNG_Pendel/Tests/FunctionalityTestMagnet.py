from ina219 import INA219
from ina219 import DeviceRangeError
import time
import logging
import RPi.GPIO as GPIO

#SIZE OF THE BUILT IN RESISTOR
SHUNT_OHMS = 0.1
#
MAX_EXPECTED_AMPS = 0.2

def read():
    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    
    #SET THE RANGE OF THE INA 219 MODULE
    ina.configure(ina.RANGE_32V)

    #Current OF THE LIFTING MAGNETE 
    current = ina.current()
    #print("current: " +str(current))
    
    #IF CUURENT LOWER 0.2 mA
    if current<0.2:
        #RESET THE LIFTING MAGNETE
        GPIO.output(13,1)
        
        logging.error("Error: Magnet not working")
        return False
       
    #RESET THE LIFTING MAGNETE
    GPIO.output(13,1)   
    return True

# This method checks the functionality of the lifting Magnet
def CheckMagnetFunctionality():
    GPIO.setwarnings(False)

    #SET PINLAYOUT
    GPIO.setmode(GPIO.BCM)

    #SET PIN 13
    GPIO.setup(13, GPIO.OUT) 
         
    while True:
        
        #POWER TO THE MAGNETE
        GPIO.output(13,0)
        #AVOID THAT THE SCRIPTS OVERRUNS THE MEASURE-PROCESS
        time.sleep(0.01)
        
        functional = read()
        logging.info("Magnet: " + str(functional))
        return functional
