from lightbarrier import *
import RPi.GPIO as GPIO

def testReceiver():
    print("Starting Test for Receiver")

    amountOfErrors = 0

    ## Failure Test for Lightbarrier One and Laser One
    lightbarrier.supplyLightSensorOne()
    if(GPIO.input(lightbarrier.getLightSensorOneDOPin()) == 1):
        print("Lightsensor One working correctly!")
    else:
        print("Lightsensor One causing Problems \n It could be that: \n 1. Lightsensor Module is not working properly")
        amountOfErrors += 1

    lightbarrier.supplyLaserOne()
    if(GPIO.input(lightbarrier.getLightSensorOneDOPin()) == 0):
        print("Lightsensor One working correctly!")
    else:
        print("Lightsensor One causing Problems \n It could be that: \n 1. Lightsensor and Laser are not alligned correctly \n 2. Laser is not working properly")
        amountOfErrors += 1

    ## Reset everything to normal 
    lightbarrier.stopPowerAll()

    ## Failure Test for Lightbarrier Two and Laser Two
    lightbarrier.supplyLightSensorTwo()
    if(GPIO.input(lightbarrier.getLightSensorTwoDOPin()) == 1):
        print("Lightsensor Two working correctly!")
    else:
        print("Lightsensor Two causing Problems \n It could be that: \n 1. Lightsensor Module is not working properly")
        amountOfErrors += 1

    lightbarrier.supplyLaserTwo()
    if(GPIO.input(lightbarrier.getLightSensorTwoDOPin()) == 0):
        print("Lightsensor Two working correctly!")
    else:
        print("Lightsensor Two causing Problems \n It could be that: \n 1. Lightsensor and Laser are not alligned correctly \n 2. Laser is not working properly")
        amountOfErrors += 1

    lightbarrier.stopPowerAll()

    if(amountOfErrors > 0):
        print("Failure of lightbarrier dected!")
        lightbarrier.piepBuzzer(5)
        return False
    else:
        print("Failure Test for lightbarriers passed!")
        lightbarrier.piepBuzzer(2)
        return True
    



#testReceiver()