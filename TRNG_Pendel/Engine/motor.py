import RPi.GPIO as GPIO
from time import sleep    
import time

# Diese Methode startet den Elektromotor und lässt ihn für eine bestimmte Zeit (durationRunning) laufen
# Der Zweite Parameter ist die Pause, zu dem nächsten Aufruf.
def StartEngine(durationRunning, timeToWait):
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
        # Ermöglicht den Stromfluss im Relay für den Motor
        GPIO.output(6,1)
        # Ermöglicht den Stromfluss im Relay fü den Hubmagnet
        GPIO.output(13,1)
    
    # Unterbrechung des Stromflusses im Relay für den Motor
    GPIO.output(6,0)   
    # Unterbrechung des Stromflusses im Relay für den Hubmagnet   
    GPIO.output(13,0) 
    sleep(timeToWait)
    # GPIO.cleanup()

# Diese Methode stoppt den Motor
def StopEngine():
    # Unterbrechung des Stromflusses im Relay für den Motor
    GPIO.output(6,0)   
    # Unterbrechung des Stromflusses im Relay für den Hubmagnet   
    GPIO.output(13,0)
