import time
import logging
import RPi.GPIO as GPIO

#SIZE OF THE BUILT IN RESISTOR
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.2

# This method checks the functionality of the lifting Magnet
def CheckMagnetFunctionality():
    functional = False

    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    # Configures Pin 13 as an Output Pin to allow to write digital 1 and 0.
    GPIO.setup(13, GPIO.OUT) 
    # Starts flow of electricity for the lifting magnet
    GPIO.output(13,0)

    ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS)
    
    #SET THE RANGE OF THE INA 219 MODULE
    ina.configure(ina.RANGE_32V)

    #Current OF THE LIFTING MAGNETE 
    current = ina.current()

    #Stop flow of electricity for the lifting magnet
    GPIO.output(13,1) 
    
    #A flow of electricity under 0.2 mA is in our context aquivilent to a not functional lifting magnet
    if current>=0.2:
        functional = True
    logging.info("Magnet working: " + str(functional))

    return functional