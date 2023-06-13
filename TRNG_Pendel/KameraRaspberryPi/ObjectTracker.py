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

#RGB Reichweite für die Analyse der Bewegungen des schwarzen Pendels
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (255, 255, 55)

#Minimale Fläche bei der schwarze Pixel als schwarzer Punkte des Pendels erkannt werden
MIN_AREA = 20
MAX_AREA = 5000
BIT_COUNTER = 0

X_MIDDLE = 324
Y_MIDDLE = 235
START_TIME = 0
#Daten
TIMESTAMPS = []
XCOORD_LIST = []
YCOORD_LIST = []
WINKEL_LIST = []
BIT_STRING = ""

#Dicitionaries mit Pixelranges
ONEANDZEROGRID_BREITE = {}
for breite in range(640 + 1):
    ONEANDZEROGRID_BREITE[breite] = breite % 2

ONEANDZEROGRID_HOEHE = {}
for hoehe in range(480 + 1):
    ONEANDZEROGRID_HOEHE[hoehe] = hoehe % 2


def write(randomBit, sharedList):
    """
    Schreibt ein Strings an Bits in die übergebene File sowie in die globale Variable BIT_STRING
    Wenn 64 Bit generiert wurden, werden diese per Interprozess Kommunikation an das Skript
    Pendelmanager übergeben
    """
    global BIT_STRING, BIT_COUNTER
    BIT_COUNTER += 1
    #with open("bits.txt", 'a') as f:
    #    f.write(str(randomBit))

    if len(BIT_STRING) < 128:
        BIT_STRING = BIT_STRING + str(randomBit)
    else: 
        sharedList.put(BIT_STRING)
        BIT_STRING = str(randomBit) 

def widthToBitsPaul(coordList, sharedList):
    """
    Wandelt die X-Koordinate über das BreitenEinserUndNullerRaster in eine Zufallszahl um und speichert diese
    """
    for coord in coordList:
        write(ONEANDZEROGRID_BREITE.get(int(coord)), sharedList)

def heightToBitsPaul(coordList, sharedList):
    """
    Wandelt die Y-Koordinate über das BreitenEinserUndNullerRaster in eine Zufallszahl um und speichert diese
    """
    for coord in coordList:
        write(ONEANDZEROGRID_HOEHE.get(int(coord)), sharedList)
        
def CheckIfMoving(x):
    """
    Checks if the Pendelum has enough movement (only Len needs to be checked - if not moving no contours get tracked)
    """
    if len(x) < 2:
        return False
    return True


def Capture(stopEvent, errorEvent, sharedList):
    """
    Tracked Konturen aus einem Live Stream, schreibt Koordinaten x, y und abstand, winkel (polares Koordinaten System)
    Solange bis "q" im geöffneten Fenster gedrückt wird oder die Gewünschte anzahl an Bits (numbits) erreicht wurde 
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
                # First Check failed than start engine and check again
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
        
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_BLACK, UPPER_BLACK)
        #Finde Konturen
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
        # Sortiere Konturen nach Fläche in absteigender Reihenfolge, nur die größten 2 Nehmen
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        for contour in contours:
                # Compute the center and radius of the contour
                (x, y), radius = cv2.minEnclosingCircle(contour)
                area = cv2.contourArea(contour)
                if area >= MIN_AREA and area < MAX_AREA:
                    #center = (float(x), float(y))
                    #radius = int(radius)
                    #Kreis zum Mittelpunkt
                    cv2.circle(frame, (int(X_MIDDLE), int(Y_MIDDLE)), 2, (255, 255, 255), 1)
                    # Kreis zum schwarzen Punkt 
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), 2)
                    #Linie zu Punkt
                    #cv2.line(frame, (int(X_MIDDLE), int(Y_MIDDLE)), (int(x), int(y)), (0, 0, 255), 2)
                    
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
                #cv2.imshow("Frame", frame)

        #Pausierung des programms 
        #if cv2.waitKey(1) & 0xFF == ord('b'):
         #   print("Pause")
          #  while True:
           #     if cv2.waitKey(1) & 0xFF == ord('b'):
            #        print("Go")
             #       break       
                
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   GenerateData(sharedList)
          #  logging.info(f"Total time running: {str(int((time.time() - START_TIME) / 60))} minutes - {BIT_COUNTER} Bits")
           # logging.info(f"Generated {str(BIT_COUNTER / (time.time() - START_TIME))} Bits per second on average")
            #break

    cap.release()
    cv2.destroyAllWindows()



def GenerateData(sharedList):
    """
    Führt erschwünschte Endmethoden zur Digitalisierung aus 
    """
    global XCOORD_LIST, YCOORD_LIST, WINKEL_LIST
    
    widthToBitsPaul(XCOORD_LIST, sharedList)
    heightToBitsPaul(YCOORD_LIST, sharedList)
    LsbFloat(WINKEL_LIST, sharedList)

    XCOORD_LIST, YCOORD_LIST, WINKEL_LIST = [], [], []


def Sign(zahl):
    """
    Überprüft ob die übergebene Zahl ein negatives Vorzeichen hat
    """
    return -1 if (zahl < 0) else 1


def ClearTestSetup():
    """
    Löscht Inhalt der jeweiligen Files 
    """
    with open('output.csv', 'w') as f:
        f.write("")

    with open('bits.txt', 'w') as f:
        f.write("")     

    
def LsbFloat(floatList, sharedList):
    """
    Schreibt LSB einer Float (aus floatList) in file 
    """
    for i in floatList:
        binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', i))
        if len(binary_str) > 8:
            lsb = binary_str[-1]
            write(lsb, sharedList)

def CapturePendelum(stopEvent, errorEvent, sharedList):
    """
    Hauptmethode
    Startet Pendel 
    """
    try:
        Capture(stopEvent,errorEvent ,sharedList)
    except Exception:
        """
        Error Handling für unbekannte/unerwartete Fehler 
        """
        #errorEvent.setErrorDescription("Oops something went wrong, review logs")
        logging.info(Exception)
        #errorEvent.setEvent()
