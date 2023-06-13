import sys, os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import time
#import logging
import RPi.GPIO as GPIO
from ErrorEvent import ErrorEvent
from multiprocessing import Process, Queue, Manager, Event, RawArray
from ctypes import c_char
from KameraRaspberryPi import ObjectTracker
import Tests.FunctionalityTestCamera as cameraFunc
import Tests.FunctionalityTestMagnet as magnetFunc
import Tests.StartUpTest as startUp
import Tests.OnlineTest as online
import Tests.TotalFailureTest as toft

BsiInitTestsPassed = None
__manager = None

# Die klasse sollte intern das multiprocessing verwalten
class PendelManager:
    def __init__(self):
        self.manager = Manager()
        pass
    
    def __cut_string(self, string, position, length):
        # Determine the start and end indices for slicing
        start_index = position
        end_index = position + length
        
        # Perform the string slicing
        cut_out_string = string[start_index:end_index]
        
        return cut_out_string

    def __prepareBinaryStringForReturn(self, binaryString, quantity, numBits):
        result = []
        numHexDigits = (numBits + 3) // 4
        
        position = 0
        # Get as many Random Numbers as required
        for i in range(0, quantity):
            # Get Random Bits from NoiseSource
            randomBits = self.__cut_string(binaryString, position, numBits)
            # Convert them into hex number
            randomHex = hex(int(randomBits, 2))
            # If necesarry remove leading "0x"
            hexStr = str(randomHex)[2:]
            # Prepend the necessary number of leading zeroes to the hex string
            hexStr = hexStr.zfill(numHexDigits)
            # Append the Hex Number to the array
            result.append(hexStr)
            # change position for next iteration:
            position += numBits
        return result

    def __hexArrayToBinaryString(self, hex_array):
        binaryString = ""

        for hex_string in hex_array:
            for hex_digit in hex_string:
                # Convert the hex digit to a 4-bit binary string
                decimal = int(hex_digit, 16) 
                binary_digit = bin(decimal)[2:]
                while(len(binary_digit) < 4):
                    binary_digit = '0' + binary_digit
                # Convert the binary digit string to a binary array
                binaryString += binary_digit
        
        return binaryString

    # Wird später aufgerufen um die Funktionalität der Lichtschranke, der Kamera und der Motorisierung des Pendels zu gewährleisten.
    def checkFunctionality(self):
        global BsiInitTestsPassed
        BsiInitTestsPassed = False
        # Check if all components are ready to work
        # Only functional if all components function correctly
        if(cameraFunc.CheckCameraFunctionality() and magnetFunc.CheckMagnetFunctionality()):
            #print("functional: going into generation")
            # Check if noise source works correctly
            hexNums = self.generateRandomBits(10, 100)
            #print(hexNums)
            # convert hexNums to binary
            binaryData = self.__hexArrayToBinaryString(hexNums)
            #print(binaryData)
            BsiInitTestsPassed = self.checkBSITests(binaryData)
        else:
            BsiInitTestsPassed = False
        return BsiInitTestsPassed
    # Hier soll der Motor gesteuert werden, und die Werte der Kamera und der Lichtschranke ausgewertet werden
    # Aktuell zu Testzwecken werden hier nur pseudozufallszahlen generiert
    def generateRandomBits(self, quantity, numBits):
        #resultArray which will be returned
        result = []
        
        self.manager = Manager()
        
        with self.manager as m:
            # Shared Memory for Random Bits
            randomValues = Queue()
            stopEvent = Event()
            errorEvent = ErrorEvent(RawArray(c_char, 255))
            # Start the generation of random values
            videoProc = Process(target=ObjectTracker.CapturePendelum, args=(stopEvent, errorEvent, randomValues))
            videoProc.start()
            # Do checks with numbers and generate as much as the params require here
            bits = ""
            goodBytes = ""
            failCounter = 0
            checkedBefore = False

            # As long as the objectTracker has no errors, we can sample further data
            # The ObjectTracker.py is only allowed to stop the Generationprocess if any errors happen.
            while not errorEvent.isEventSet():

                # If eight times a byte or more are in the Queue we want to sample them
                if(randomValues.qsize() >= 8):
                    # Transfer eight objects over multiprocess communication from the ObjectTracker.py to pendelManager.py
                    for i in range(0, 8):
                        bits += randomValues.get()
                    # 128 bytes = 1024 bits have been transfered to the pendelManager, the quality of the bits is checked with the 
                    # Tests explained in PTG.2. provided by the BSI in Germany.
                    if(len(bits) >= 1024): 
                        if(checkedBefore):
                            # If the random bits out of the iteration before have passed the Online Tests.
                            # It is very likely that the next 1024 bits are also randoms.
                            # Therefore we will take the next 1024 and prepare it for the output
                            goodBytes += bits
                            print("goodBits" + str(len(goodBytes)))
                            checkedBefore = False
                        elif(online.onlineTest(bits)):
                            checkedBefore = True
                            failCounter = 0
                        elif(failCounter < 3):
                            failCounter += 1
                        else:
                            # If the Tests fail ten times in a row, the probality of an error in the samplingprocess is very high.
                            # Therefore the generationprocess is stopped and the API will provide an statuscode providing further information                        elif(failCounter + 1 == 10):
                            errorEvent.setErrorDescription("Online Test has failed 3 Times in a row")
                            errorEvent.setEvent()
                        bits = ""

                    # If the requested amount of bits has been reached, the generation process will be stopped and the stopEvent will be triggerd
                    if(len(goodBytes) >= (quantity * numBits)):
                        # Reset Lifting Magnet to prevent overheating
                        GPIO.output(13,1)
                        # Stop the generation of random values
                        stopEvent.set()
                        break
                else:
                    # polling rate at 0.1 seconds for main process
                    time.sleep(0.1)
            
            # ErrorEvent handling
            if(errorEvent.isEventSet()):
                stopEvent.set()
                raise Exception(errorEvent.getErrorDescription())
            else:
                pass

            #prepare goodByts for return (split into quantitty times numBits and change to hex numbers)
            result = self.__prepareBinaryStringForReturn(goodBytes, quantity, numBits)

            # End Process
            videoProc.terminate()

        return result

    # Statische Prüfung der Zufallszahlen
    def checkBSITests(self, binaryData):
        return toft.TotalFailureTest(str(binaryData), False, 8) and startUp.StartUpTest(str(binaryData))

# Returns the only instance of the PendelManger class
def GetInstance():
    return __manager

# Wir können feststellen ob der Manager direkt gestartet wird
if __name__ == '__main__':
    if(__manager == None):
        __manager = PendelManager()

    # For Testing:
    functional = __manager.checkFunctionality()
    if(functional):   
        print("Functional") 
        print(__manager.generateRandomBits(4, 256))
    else:
        print("Not Functional")

# oder ob er von der API aus aufgerufen wird.            
else:
    if(__manager == None):
        __manager = PendelManager()
