import RPi.GPIO as GPIO
from time import sleep    
import time
import keyboard

# Diese Methode startet den Elektromotor und lässt ihn für eine bestimmte Zeit (durationRunning) laufen
# Der Zweite Parameter ist die Pause, zu dem nächsten Aufruf.
def StartEngine(durationRunning, timeToWait, isRunning):
    global ENGINE_RUNNING
    # debug option
    GPIO.setwarnings(False)
    
    # Nummerierung der GPIO Pins nach Standard
    GPIO.setmode(GPIO.BCM) 
    
    # Pin für die Motorsteuerung
    GPIO.setup(6, GPIO.OUT)  
    # Pin für den Hubmagnet
    GPIO.setup(13, GPIO.OUT)  
    
    # Die aktuelle Zeit
    now = time.time()
    
    while now > time.time()-durationRunning: 
        isRunning = True
        # Ermöglicht den Stromfluss im Relay für den Motor
        GPIO.output(6,1)
        # Ermöglicht den Stromfluss im Relay fü den Hubmagnet
        GPIO.output(13,0)
    
    # Unterbrechung des Stromflusses im Relay für den Motor
    GPIO.output(6,0)   
    # Unterbrechung des Stromflusses im Relay für den Hubmagnet   
    GPIO.output(13,1) 
    isRunning = False   
    sleep(timeToWait)
    # GPIO.cleanup()

# Diese Methode stoppt den Motor
def StopEngine():
    # Unterbrechung des Stromflusses im Relay für den Motor
    GPIO.output(6,0)   
    # Unterbrechung des Stromflusses im Relay für den Hubmagnet   
    GPIO.output(13,1)
    
def RunScript():
    global ENGINE_RUNNING
    ENGINE_RUNNING = True
    while ENGINE_RUNNING:
      StartEngine(3,6.5, True)
      time.sleep(0.1)
        
def StopScript():
    global ENGINE_RUNNING
    ENGINE_RUNNING = False   

def main():
    for i in range(0, 5):
        StartEngine(2, 7)

#main()
