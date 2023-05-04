from multiprocessing import Process, Manager
from random import *
from Lightbarrier import lightbarrier, startUpTestLightbarrier
from KameraRaspberryPi import ObjectTracker

# Wird von der REST-API geleitet
CONTROLLED_BY_API = False

# Die klasse sollte intern das multiprocessing verwalten
class PendelManager:
    # TODO implement multiprocessing for small private functions
    def __init__(self, controlledByAPI):
        self.manager = Manager()
        pass

    # Wird später aufgerufen um die Funktionalität der Lichtschranke, der Kamera und der Motorisierung des Pendels zu gewährleisten.
    def checkFunctionality(returnValue):
        checkSuccessful = False
        #lightbarrier.functionalityTest()
        #enginecontrol.startuptest()
        #camera.startuptest()
        #if(ligtbarrier and enginecontrol and camera):
        #   checkSuccessful = True
        returnValue = checkSuccessful

    # Hier soll der Motor gesteuert werden, und die Werte der Kamera und der Lichtschranke ausgewertet werden
    # Aktuell zu Testzwecken werden hier nur pseudozufallszahlen generiert
    def generateRandomBits(self, quantity, numBits):
        # TODO hier sollten die anderen Processe gestartet werden
        with self.manager as m:
            procs = []
            # TODO Wir müssen öffentliche run methoden für die einzelnen Scripte nutzen
            # engineProc = Process(target=EngineControl.run())
            #procs.append(engineProc)
            videoProc = Process(target=ObjectTracker.__main__(), args=resultValue)
            procs.append(videoProc)
            ligtProc = Process(target=lightbarrier.__main__(), args=resultValue)
            procs.append(ligtProc)

            # TODO: Kontrolle der Prozesse; Erst Zahlen generieren und dann den Test
            
            # Aufbereitung der Daten für die API
            # counter for len of result array
            i = 0
            # len of result array given by parameter
            quantity # = request.args.get('quantity', default=1, type=int)
            #len of the random Bits
            numBits # = request.args.get('numBits', default=1, type=int)
            # calculate the len of the result numbers to fill in leading zeroes if wanted.
            numHexDigits = (numBits + 3) // 4
            #resultArray which will be returned
            result = []

            # Get as many Random Numbers as required
            for i in range(0, quantity):
                # Get Random Bits from NoiseSource
                #TODO: change to method from noise source
                randomBits = random.getrandbits(numBits)
                # Convert them into hex number
                randomHex = hex(int(randomBits))
                # If necesarry remove leading "0x"
                hexStr = str(randomHex)[2:]
                # Prepend the necessary number of leading zeroes to the hex string
                hexStr = hexStr.zfill(numHexDigits)
                # Append the Hex Number to the array
                result.append(hexStr)
        return result

    # Statische Prüfung der Zufallszahlen
    def checkBSITests():
        print()

# Wir können feststellen ob der Manager direkt gestartet wird
# TODO überlegen ob wir hier ein singelton pattern umsetzen möchten
if __name__ == '__main__':
    print("Executed when called directly")
    CONTROLLED_BY_API = False

# oder ob er von der API aus aufgerufen wird.            
else:
    CONTROLLED_BY_API = True
    print("Executed when imported.")
