import time
import random
from multiprocessing import Process, Manager, Event
from KameraRaspberryPi import ObjectTracker
from Tests import TotalFailureTest

# Wird von der REST-API geleitet
__CONTROLLED_BY_API = False
__manager = ''

# Die klasse sollte intern das multiprocessing verwalten
class PendelManager:
    def __init__(self, controlledByAPI):
        self.manager = Manager()
        pass

    # Wird später aufgerufen um die Funktionalität der Lichtschranke, der Kamera und der Motorisierung des Pendels zu gewährleisten.
    def checkFunctionality(returnValue):
        checkSuccessful = False
        #camera.functionalityTest()
        #enginecontrol.startuptest()
        #camera.startuptest()
        #if(ligtbarrier and enginecontrol and camera):
        #   checkSuccessful = True
        returnValue = checkSuccessful

    # Hier soll der Motor gesteuert werden, und die Werte der Kamera und der Lichtschranke ausgewertet werden
    # Aktuell zu Testzwecken werden hier nur pseudozufallszahlen generiert
    def generateRandomBits(self, quantity, numBits):
        #resultArray which will be returned
        result = []
        with self.manager as m:
            #Process storage
            procs = []
            # Shared Memory for Random Bits
            randomValues = m.list()
            stopEvent = Event()

            videoProc = Process(target=ObjectTracker.CapturePendelum, args=(stopEvent, randomValues))
            procs.append(videoProc)

            # Start the generation of random values
            videoProc.start()

            # Do checks with numbers and generate as much as the params require
            # here
            #TODO: Do tests here

            # Stop the generation of random values
            stopEvent.set()

        return result

    # Statische Prüfung der Zufallszahlen
    def checkBSITests(binaryData):
        TotalFailureTest.TotalFailureTest(binaryData, False, 8)

# Returns the only instance of the PendelManger class
def GetInstance():
    return __manager

# Wir können feststellen ob der Manager direkt gestartet wird
if __name__ == '__main__':
    print("Executed when called directly")
    # Eventuell können wir hier eine Menüführung über CLI implementieren
    __CONTROLLED_BY_API = False
    __manager = PendelManager(__CONTROLLED_BY_API)

# oder ob er von der API aus aufgerufen wird.            
else:
    print("Executed when imported.")
    __CONTROLLED_BY_API = True
    __manager = PendelManager(__CONTROLLED_BY_API)
