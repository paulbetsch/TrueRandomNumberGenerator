import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

currentTime = 0
pastTime = 0

##Lightsensor Configuration
## -> GPIO Pin 18 = Digital output of the photoresistors
## -> GPIO Pin 23 = power supply of the photoresistor
lightSensorDO = 18
lightSensorV = 23
lightSensorStatus = False
GPIO.setup(lightSensorDO, GPIO.IN)
GPIO.setup(lightSensorV, GPIO.OUT)

##Buzzer Configuration
## -> GPIO Pin 21 = power supply of the Buzzer
buzzerV = 21
buzzerStatus = False
GPIO.setup(buzzerV, GPIO.OUT)

##Laser Configuration
## -> GPIO Pin 5 = power supply of the laser diode
laserV = 5
GPIO.setup(laserV, GPIO.OUT)

def LaserOn():
    GPIO.output(laserV, True)
    
def LaserOff():
    GPIO.output(laserV, False)
    
def LightSensorOn():
    GPIO.output(lightSensorV, True)
    
def LightSensorOff():
    GPIO.output(lightSensorV, False)

def BuzzerOff():
    GPIO.output(buzzerV, False)
    
def BuzzerOn():
    GPIO.output(buzzerV, True)

def ReadLightSensor():
    global lightSensorStatus
    global timeintervalls
    state = (GPIO.input(lightSensorDO) == 0)
    if not (state == lightSensorStatus):
        if(state):
            print("Lightbarrier closed Pin "+str(lightSensorDO))
        else:
            print("Lightbarrier broken Pin "+str(lightSensorDO))
            CalculateTime()
        lightSensorStatus = state


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
ShutdownLightBarrier()
    