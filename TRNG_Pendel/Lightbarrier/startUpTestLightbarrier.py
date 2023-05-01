from lightbarrier import *
import RPi.GPIO as GPIO
import time

def testFunctionality():
    print("Starting Test for Receiver")
    failed = False

    ## Failure Test for Lightbarrier One and Laser One
    print("Lightsensor One")
    supplyLightSensorOne()
    time.sleep(0.5)
    if(GPIO.input(getLightSensorOneDOPin()) != 1):
        print(" - Lightsensor Module is not working properly \n - Lightsensor Module is configured to sensitive \n - Lightbarrier is being manipulated by another Lightsource")
        failed = True
    supplyLaserOne()
    time.sleep(0.5)
    if(GPIO.input(getLightSensorOneDOPin()) != 0):
        print(" - Lightsensor and Laser are not alligned correctly \n - Laser is not working properly")
        failed = True

    ## Reset everything to normal 
    stopPowerAll()

    ## Failure Test for Lightbarrier Two and Laser Two
    print("Lightsensor Two")
    supplyLightSensorTwo()
    time.sleep(0.5)
    if(GPIO.input(getLightSensorTwoDOPin()) != 1):
        print(" - Lightsensor Module is not working properly \n - Lightsensor Module is configured to sensitive \n - Lightbarrier is being manipulated by another Lightsource")
        failed = True
    supplyLaserTwo()
    time.sleep(0.5)
    if(GPIO.input(getLightSensorTwoDOPin()) != 0):
        print(" - Lightsensor and Laser are not alligned correctly \n - Laser is not working properly")
        failed = True
    
    stopPowerAll()

    if(failed  ):
        print("Failure of lightbarrier dected!")
        piepBuzzer(5)
        return False
    else:
        print("Failure Test for lightbarriers passed!")
        piepBuzzer(2)
        return True
    
testFunctionality()
