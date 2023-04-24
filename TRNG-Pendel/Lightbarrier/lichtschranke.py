import RPi.GPIO as GPIO
import time
from multiprocessing import Process, Manager
from lsbsampler import *

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

##Lightsensor Configuration
## -> GPIO Pin 18 = Digital output of the photoresistors
## -> GPIO Pin 23 = power supply of the photoresistor
lightSensorOneDO = 18
lightSensorOneV = 23
lightSensorOneStatus = False
GPIO.setup(lightSensorOneDO, GPIO.IN)
GPIO.setup(lightSensorOneV, GPIO.OUT)

lightSensorTwoDO = 24
lightSensorTwoV = 25
lightSensorTwoStatus = False
GPIO.setup(lightSensorTwoDO, GPIO.IN)
GPIO.setup(lightSensorTwoV, GPIO.OUT)

##Buzzer Configuration
## -> GPIO Pin 21 = power supply of the Buzzer
buzzerV = 21
buzzerStatus = False
GPIO.setup(buzzerV, GPIO.OUT)

##Laser Configuration
## -> GPIO Pin 5 = power supply of the laser diode
laserOneV = 16
GPIO.setup(laserOneV, GPIO.OUT)

laserTwoV = 12
GPIO.setup(laserTwoV, GPIO.OUT)

def supplyPower(pin):
    GPIO.output(pin, True)
    
def stopPower(pin):
    GPIO.output(pin, False)
    
def stopPowerAll():
    stopPower(laserOneV)
    stopPower(laserTwoV)
    stopPower(lightSensorOneV)
    stopPower(lightSensorTwoV)
    stopPower(buzzerV)
    
def supplayPowerAll():
    supplyPower(laserOneV)
    supplyPower(lightSensorOneV)
    supplyPower(laserTwoV)
    supplyPower(lightSensorTwoV)
    supplyPower(buzzerV)

# The lightSensor will output a high voltage to signal a 1 if the
# lightbarrier is broken. Or in another context if the light resistor
# receive not enough concentration of light
def readLightSensor(lightSensorDO, lightSensorStatus, listValues):
    pastTime = 0
    currentTime = time.time_ns()
    while True:
        broken = GPIO.input(lightSensorDO) == 1
        if (broken != lightSensorStatus ):
            lightSensorStatus = broken
            if(broken):
                print("Lightbarrier broken on Pin "+str(lightSensorDO))
                pastTime = currentTime
                listValues.append(calculateTime(pastTime, time.time_ns()))
                print(listValues[-1])
            else:
                print("Lightbarrier closed on Pin "+str(lightSensorDO))
                print("Starting time")
                currentTime = time.time_ns()

def calculateTime(pastTime, currentTime):
    return currentTime - pastTime

supplyPower(laserTwoV)
supplyPower(lightSensorTwoV)
#readLightSensor(lightSensorTwoDO, lightSensorTwoStatus)

supplyPower(laserOneV)
supplyPower(lightSensorOneV)
#readLightSensor(lightSensorOneDO, lightSensorOneStatus)

sharedList = []

if __name__ == "__main__":
    # Opens a new Manger to allow interprocess communication
    with Manager() as manager:
        # Two List to exchange data from the worker threads to the main threads
        sharedList = manager.list()
        sharedList2 = manager.list()

        procs = []
        first = Process(target=readLightSensor, args=(lightSensorOneDO, lightSensorOneStatus, sharedList))
        procs.append(first)
        second = Process(target=readLightSensor, args=(lightSensorTwoDO, lightSensorTwoStatus, sharedList2))
        procs.append(second)

        # Using start() to simutainiusly run the code instead of run()
        first.start()
        second.start()

        print("sleeping")
        time.sleep(15)

        # Killing the threads after 4 Seconds
        print("killing")
        first.terminate()
        second.terminate()


        # for p in procs:
        #     p.join()
        """
        print("Main Thread")
        print(sharedList)
        print("neue Liste")
        print(sharedList2)"""
        
        print(len(sharedList))
        decListToBinaryList(sharedList)
        print(len(sharedList2))
        decListToBinaryList(sharedList2)















"""
def ControlBuzzer():
    global lightSensorStatus
    if(lightSensorStatus == True):
        BuzzerOff()
    else:
        BuzzerOn()
    
def BootupLightBarrier():
    global pastTime
    pastTime = time.time_ns()
    LightSensorOn()
    LaserOn()
    while True:
        ReadLightSensor()
        
def ShutdownLightBarrier():
    LightSensorOff()
    LaserOff()
    
def CalculateTime():
    global currentTime
    global pastTime
    currentTime = time.time_ns()
    print(time.time_ns() - pastTime)
    pastTime = currentTime 
    
BootupLightBarrier()
ShutdownLightBarrier()"""
    