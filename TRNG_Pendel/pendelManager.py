import time
import random
from multiprocessing import Process, Queue, Manager, Event
from KameraRaspberryPi import ObjectTracker
import Tests.FunctionalityTestCamera as cameraFunc
import Tests.FunctionalityTestEngine as engineFunc
import Tests.FunctionalityTestMagnet as magnetFunc
import Tests.StartUpTest as startUp
import Tests.OnlineTest as online
import Tests.TotalFailureTest as toft

# Wird von der REST-API geleitet
__CONTROLLED_BY_API = False
__manager = ''

# Die klasse sollte intern das multiprocessing verwalten
class PendelManager:
    def __init__(self, controlledByAPI):
        self.manager = Manager()
        pass

    # Wird später aufgerufen um die Funktionalität der Lichtschranke, der Kamera und der Motorisierung des Pendels zu gewährleisten.
    def checkFunctionality(self):
        # Check if all components are ready to work
        camWorks = cameraFunc.CheckCameraFunctionality()
        engineWorks = engineFunc.CheckEngineFunctionality()
        magnetWorks = magnetFunc.CheckMagnetFunctionality()

        # Only functional if all components function correctly
        return camWorks and engineWorks and magnetWorks


    # Hier soll der Motor gesteuert werden, und die Werte der Kamera und der Lichtschranke ausgewertet werden
    # Aktuell zu Testzwecken werden hier nur pseudozufallszahlen generiert
    def generateRandomBits(self, quantity, numBits):
        #resultArray which will be returned
        result = []
        with self.manager as m:
            #Process storage
            procs = []
            # Shared Memory for Random Bits
            randomValues = Queue()
            stopEvent = Event()
            errorEvent = Event()

            videoProc = Process(target=ObjectTracker.CapturePendelum, args=(stopEvent, errorEvent, randomValues))
            procs.append(videoProc)

            # Start the generation of random values
            videoProc.start()

            # Do checks with numbers and generate as much as the params require here
            byts = []

            while not errorEvent.is_set():
                if(randomValues.qsize >= 8):
                    for i in range(0, 8):
                        byts.append(randomValues.get())
                if(len(byts) >= 128):
                    #TODO: Do tests here (maybe in diffrent processes)
                    onlineProc = Process(target=online.onlineTest, args=(byts))
                    onlineProc.start()
                    byts = []


                testProc = Process(target=online.onlineTest, args=())
                pass
            
            # Stop the generation of random values
            stopEvent.set()
            # End Process
            videoProc.terminate()

        return result

    # Statische Prüfung der Zufallszahlen
    def checkBSITests(self, binaryData):
        tf.TotalFailureTest(str(binaryData), False, 8)

# Returns the only instance of the PendelManger class
def GetInstance():
    return __manager

# Wir können feststellen ob der Manager direkt gestartet wird
if __name__ == '__main__':
    print("Executed when called directly")
    # Eventuell können wir hier eine Menüführung über CLI implementieren
    __CONTROLLED_BY_API = False
    __manager = PendelManager(__CONTROLLED_BY_API)
    
    # For Testing:
    __manager.generateRandomBits(10, 100)

# oder ob er von der API aus aufgerufen wird.            
else:
    print("Executed when imported.")
    __CONTROLLED_BY_API = True
    __manager = PendelManager(__CONTROLLED_BY_API)
