import sys, os
import cv2
import math
import struct
import time
#import RPi.GPIO as GPIO
from time import sleep    
#import keyboard
import numpy as np
from multiprocessing import Process
import logging

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Engine import motor as m
from Tests import FunctionalityTestMagnet as magnet

#RGB Ranges
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (255, 255, 55)

#Minimum area and maximum area for the black square on the outer pendulum in pixels
MIN_AREA = 20
MAX_AREA = 5000
BIT_COUNTER = 0

#Middle of the Pendelum
X_MIDDLE = 324
Y_MIDDLE = 235
START_TIME = 0

#DATA
TIMESTAMPS = []
XCOORD_LIST = []
YCOORD_LIST = []
WINKEL_LIST = []
BIT_STRING = ""

#Dicitionaries with Pixelranges for grid
ONEANDZEROGRID_BREITE = {}
for breite in range(640 + 1):
    ONEANDZEROGRID_BREITE[breite] = breite % 2

ONEANDZEROGRID_HOEHE = {}
for hoehe in range(480 + 1):
    ONEANDZEROGRID_HOEHE[hoehe] = hoehe % 2


def write(randomBit, sharedList):
    """
    Writes a string of bits to the global variable BIT_STRING.
    Every 64 bits generated, they are passed to the script PendulumManager
    via interprocess communication.
    """
    global BIT_STRING, BIT_COUNTER
    BIT_COUNTER += 1
    
    if len(BIT_STRING) < 128:
        BIT_STRING = BIT_STRING + str(randomBit)
    else: 
        #ADD 64BIT Block to sharedList with PendelumManger
        sharedList.put(BIT_STRING)
        BIT_STRING = str(randomBit) 

def widthToBits(coordList, sharedList):
    """
    Converts the X-coordinate through the binary one-and-zero raster into a random number and saves it.
    """
    for coord in coordList:
        write(ONEANDZEROGRID_BREITE.get(int(coord)), sharedList)

def heightToBits(coordList, sharedList):
    """
    Converts the Y-coordinate through the binary one-and-zero raster into a random number and saves it.
    """
    for coord in coordList:
        write(ONEANDZEROGRID_HOEHE.get(int(coord)), sharedList)
        
def CheckIfMoving(x):
    """
    Checks if the Pendelum has movement 
    """
    if len(x) < 2:
        return False
    return True


def Capture(stopEvent, errorEvent, sharedList):
    """
    Tracks contours from a live stream from the camera, writes x, y, and angle until the PendulumManager script terminates, or an Error occurs.
    Every 8 seconds it writes its data starts the Motorprocess for 2 seconds.
    """
    def error(message):
        """
        Stops Code sets Error
        """
        logging.debug(message)
        cap.release()
        cv2.destroyAllWindows()
        print("Error: " + message)
        errorEvent.setErrorDescription("Error: " + message)
        errorEvent.setEvent()

    cap = cv2.VideoCapture(0)
    timestamp = time.time()
    START_TIME = time.time()
    m.StartEngine(3, 0)
    logging.info(f"\n Started Camera at '{str(timestamp)}'")
    while not stopEvent.is_set():
        if time.time() - timestamp > 8:
            logging.debug("\nBits per second: " + str(len(XCOORD_LIST) * 3 / (time.time() - timestamp)))
            if CheckIfMoving(XCOORD_LIST) == True:
                GenerateData(sharedList)
            else:
                error("Unable to track Pendelum movement!")
            print("Bits: " + str(BIT_COUNTER))
            if magnet.CheckMagnetFunctionality():
                # First Check successful then start engine
                timestamp = time.time()
                logging.debug("-----------------------------")
                t = Process(target=m.StartEngine, args=(2, 0))
                t.start()
            else:
                # First Check failed then start engine and check again
                t = Process(target=m.StartEngine, args=(2, 0))
                t.start()
                if magnet.CheckMagnetFunctionality():
                    timestamp = time.time()
                    logging.debug("-----------------------------")
                    t = Process(target=m.StartEngine, args=(2, 0))
                    t.start()
                else:
                    error("Magnet functionality failed")
                    break
        # Read a frame from the video capture
        ret, frame = cap.read()      
        # Convert the frame from BGR to HSV color space
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)    
        # Create a mask using lower and upper black color thresholds
        mask = cv2.inRange(hsv, LOWER_BLACK, UPPER_BLACK)     
        # Find contours in the mask image using external retrieval mode and simple chain approximation
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #Sort contours in descending order based on their area, take only the largest one
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        for contour in contours:
                # Compute the center and radius of the contour
                (x, y), radius = cv2.minEnclosingCircle(contour)
                area = cv2.contourArea(contour)
                if area >= MIN_AREA and area < MAX_AREA:
                    cv2.circle(frame, (int(X_MIDDLE), int(Y_MIDDLE)), 2, (255, 255, 255), 1)
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), 2)
                    dx = float(x) - X_MIDDLE
                    dy = float(y) - Y_MIDDLE 
                    distanz = math.sqrt(dx ** 2 + dy ** 2)
                    if distanz < 220 and distanz > 0:
                        winkel = math.acos(dx/distanz) * Sign(dy) # Winkel berechnung in Bogenmaß
                        XCOORD_LIST.append(float(x))
                        YCOORD_LIST.append(float(y))
                        WINKEL_LIST.append(winkel)
                        TIMESTAMPS.append(time.time())
                else:
                    if MAX_AREA < area:
                        error("Camera disturbance, remove disturbing Objects")

    cap.release()
    cv2.destroyAllWindows()



def GenerateData(sharedList):
    
    """
    Performs desired methods for digitization.
    """
    global XCOORD_LIST, YCOORD_LIST, WINKEL_LIST
    widthToBits(XCOORD_LIST, sharedList)
    heightToBits(YCOORD_LIST, sharedList)
    LsbFloat(WINKEL_LIST, sharedList)

    #Reset Lists after generation of Data 
    XCOORD_LIST, YCOORD_LIST, WINKEL_LIST = [], [], []


def Sign(zahl):
    """
    Checks if the given number has a negative sign.
    """
    return -1 if (zahl < 0) else 1     

    
def LsbFloat(floatList, sharedList):  
    """
    Writes the LSB (Least Significant Bit) of a float (from floatList) to a file.
    """
    for i in floatList:
        binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', i))
        if len(binary_str) > 8:
            lsb = binary_str[-1]
            write(lsb, sharedList)

def CapturePendelum(stopEvent, errorEvent, sharedList):
    """
    Main method
    Starts the pendulum.
    """
    try:
        Capture(stopEvent,errorEvent ,sharedList)
    except Exception:
        """
        Error handling for unknown/unexpected errors.
        """
        errorEvent.setErrorDescription("Oops something went wrong, review logs")
        logging.info(Exception)
        errorEvent.setEvent()
