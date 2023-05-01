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


def getLightSensorOneDOPin():
    return lightSensorOneDO

def getLightSensorTwoDOPin():
    return lightSensorTwoDO

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

def supplyLightSensorOne():
    supplyPower(lightSensorOneV)

def supplyLightSensorTwo():
    supplyPower(lightSensorTwoV)

def supplyLaserOne():
    supplyPower(laserOneV)

def supplyLaserTwo():
    supplyPower(laserTwoV)

def supplyBuzzer():
    supplyPower(buzzerV)

def stopLightSensorOne():
    stopPower(lightSensorOneV)

def stopLightSensorTwo():
    stopPower(lightSensorTwoV)

def stopLaserOne():
    stopPower(laserOneV)

def stopLaserTwo():
    stopPower(laserTwoV)

def stopBuzzer():
    stopPower(buzzerV)

def piepBuzzer(amount):
    for i in range(amount):
        time.sleep(0.1)
        supplyBuzzer()
        time.sleep(0.1)
        stopBuzzer()

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

#supplyPower(laserTwoV)
#supplyPower(lightSensorTwoV)
#readLightSensor(lightSensorTwoDO, lightSensorTwoStatus)

#supplyPower(laserOneV)
#supplyPower(lightSensorOneV)
#readLightSensor(lightSensorOneDO, lightSensorOneStatus)

def runTwoLightbarriersParallel():
    with Manager() as manager:
        sharedList = manager.list()
        sharedList2 = manager.list()
        supplyLightSensorOne()
        supplyLaserOne()
        process = Process(target=readLightSensor, args=(lightSensorOneDO, lightSensorOneStatus, sharedList))
        process.start()
        
        supplyLightSensorTwo()
        supplyLaserTwo()
        processTwo = Process(target=readLightSensor, args=(lightSensorTwoDO, lightSensorTwoStatus, sharedList2))
        processTwo.start()
        
        #Abrruch Bedingung von Kameraüberwachung, abbruch wenn pendel zu langsam
        for i in range(15):
            time.sleep(1)
        
        process.terminate()
        processTwo.terminate()
        print(sharedList)
        decListToBinaryList(sharedList)

def runOneLightbarrierParallel():
    with Manager() as manager:
        sharedList = manager.list()
        supplyLightSensorOne()
        supplyLaserOne()
        process = Process(target=readLightSensor, args=(lightSensorOneDO, lightSensorOneStatus, sharedList))
        process.start()
        
        #Abrruch Bedingung von Kameraüberwachung, abbruch wenn pendel zu langsam
        for i in range(15):
            time.sleep(1)
        
        process.terminate()
        print(sharedList)
        decListToBinaryList(sharedList)
    
#runOneLightbarrierParallel()
#runTwoLightbarriersParallel()


"""
if __name__ == "__main__":
    # Opens a new Manger to allow interprocess communication
    with Manager() as manager:
        # Two List to exchange data from the worker threads to the main threads
        sharedList = manager.list()
        sharedList2 = manager.list()

        procs = []
        supplyLightSensorOne()
        supplyLaserOne()
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
        print("Main Thread")
        print(sharedList)
        print("neue Liste")
        print(sharedList2)
        
        print(len(sharedList))
        decListToBinaryList(sharedList)
        print(len(sharedList2))
        decListToBinaryList(sharedList2)
"""














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
    
