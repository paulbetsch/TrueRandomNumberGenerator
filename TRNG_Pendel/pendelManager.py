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
            # Shared Memory for Random Bits
            randomValues = Queue()
            stopEvent = Event()
            errorEvent = Event()

            # Start the generation of random values
            videoProc = Process(target=ObjectTracker.CapturePendelum, args=(stopEvent, errorEvent, randomValues))
            videoProc.start()

            # Do checks with numbers and generate as much as the params require here
            byts = []
            goodByts = []
            failCounter = 0

            # As long as the objectTracker has no errors, we can sample further data
            # The ObjectTracker.py is only allowed to stop the Generationprocess if any errors happen.
            while not errorEvent.is_set():

                # If eight times a byte or more are in the Queue we want to sample them
                # TODO: maybe set the transfer rate to the startsize of the Online Tests
                if(randomValues.qsize >= 8):
                    # Transfer eight objects over multiprocess communication from the ObjectTracker.py to pendelManager.py
                    for i in range(0, 8):
                        byts.append(randomValues.get())

                    # 128 bytes = 1024 bits have been transfered to the pendelManager, the quality of the bits is checked with the 
                    # Tests explained in PTG.2. provided by the BSI in Germany.
                    if(len(byts) >= 128):
                        if(online.onlineTest(byts)):
                            goodByts += byts
                            failCounter = 0
                        # If the Tests fail ten times in a row, the probality of an error in the samplingprocess is very high.
                        # Therefore the generationprocess is stopped and the API will provide an statuscode providing further information                        elif(failCounter + 1 == 10):
                            errorEvent.set()
                        else:
                            failCounter += 1
                        byts = []

                    # If the requested amount of bits has been reached, the generation process will be stopped and the stopEvent will be triggerd
                    if(goodByts == (quantity * numBits)):
                        break
                else:
                    # TODO: implement possible timeout, when no bytes are retrieved from videoProc
                    time.sleep(0.1)
            
            # TODO: prepare goodByts for return
            # TODO: errorEvent handling
            if(errorEvent.is_set()):
                pass
            else:
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
