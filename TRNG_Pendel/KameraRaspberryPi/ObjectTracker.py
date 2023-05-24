import cv2
import math
import struct
import time
#import RPi.GPIO as GPIO
from time import sleep    
#import keyboard
import numpy as np
from multiprocessing import Process
#from Engine import motor

#Video Quelle -> 0 = Standard Kamera , 1 = Externe Kamera
cap = cv2.VideoCapture(0)

#RGB Reichweite für die Analyse der Bewegungen des schwarzen Pendels
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (255, 255, 55)

#Minimale Fläche bei der schwarze Pixel als schwarzer Punkte des Pendels erkannt werden
MIN_AREA = 20

X_MIDDLE = 324  
Y_MIDDLE = 234

#Daten
TIMESTAMPS = []
XCOORD_LIST = []
YCOORD_LIST = []
WINKEL_LIST = []
DISTANZ_LIST = []
BIT_STRING = ""

#Dicitionaries mit Pixelranges
ONEANDZEROGRID_BREITE = {}
for breite in range(1920+1):
    ONEANDZEROGRID_BREITE[breite] = breite % 2

ONEANDZEROGRID_HOEHE = {}
for hoehe in range(1080+1):
    ONEANDZEROGRID_HOEHE[hoehe] = hoehe % 2

# Schreibt ein Strings an Bits in die übergebene File sowie in die globale Variable BIT_STRING
# Wenn 64 Bit generiert wurden, werden diese per Interprozess Kommunikation an das Skript
# Pendelmanager übergeben
def write(randomBit, sharedList):
    global BIT_STRING
    """with open(file, 'a') as f:
        f.write(randomBit)"""
    
    if len(BIT_STRING) < 64:
        BIT_STRING = BIT_STRING + randomBit
    else: 
        sharedList.append(BIT_STRING)
        BIT_STRING = randomBit

# Wandelt die X-Koordinate über das BreitenEinserUndNullerRaster in eine Zufallszahl um und speichert diese
def widthToBitsPaul(coordList, sharedList):
    for coord in coordList:
        write(ONEANDZEROGRID_BREITE.get(int(coord)), sharedList)

# Wandelt die Y-Koordinate über das BreitenEinserUndNullerRaster in eine Zufallszahl um und speichert diese
def heightToBitsPaul(coordList, sharedList):
    for coord in coordList:
        write(ONEANDZEROGRID_HOEHE.get(int(coord)), sharedList)
        
def CheckIfMoving(x):
    """
    Checks if the Pendelum has enough movement
    """
    if len(x) < 1:
        return False

    for i in range (len(x) - 2):
        if int(x[i]) == int(x[i + 1]) == int(x[i + 2]):
            return False
    return True


def Capture(stopEvent, errorEvent, sharedList):
    """
    Tracked Konturen aus einem Live Stream, schreibt Koordinaten x, y und abstand, winkel (polares Koordinaten System)
    Solange bis "q" im geöffneten Fenster gedrückt wird oder die Gewünschte anzahl an Bits (numbits) erreicht wurde 
    """
    cap = cv2.VideoCapture(-1, cv2.CAP_V4L)
    timestamp = time.time()
    motor.StartEngine(3, 0)
    print("\n Start Camera")
    while not stopEvent.is_set():
        if time.time() - timestamp > 8:
            GenerateData(sharedList)
            t = Process(target=motor.StartEngine, args=(2, 0))
            t.start()
            timestamp = time.time()
            if CheckIfMoving(XCOORD_LIST):
                print("Pendelum is moving")
            else:
                print("Pendelum not moving")
                cap.release()
                cv2.destroyAllWindows()
                errorEvent.set()
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
                if area >= MIN_AREA:
                    center = (float(x), float(y))
                    radius = int(radius)
                    #Kreis zum Mittelpunkt
                    cv2.circle(frame, (int(X_MIDDLE), int(Y_MIDDLE)), 2, (255, 255, 255), 1)
                    # Kreis zum schwarzen Punkt 
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), 2)
                    #Linie zu Punkt
                    #cv2.line(frame, (int(X_MIDDLE), int(Y_MIDDLE)), (int(x), int(y)), (0, 0, 255), 2)
                    
                    dx = float(x) - X_MIDDLE
                    dy = float(y) - Y_MIDDLE 
                    distanz = math.sqrt(dx ** 2 + dy ** 2)
            
                    winkel = math.acos(dx/distanz) * Sign(dy) # Winkel berechnung in Bogenmaß
                    
                    if distanz < 220:
                        XCOORD_LIST.append(float(x))
                        YCOORD_LIST.append(float(y))
                        DISTANZ_LIST.append(distanz)
                        WINKEL_LIST.append(winkel)
                        TIMESTAMPS.append(time.time())

                cv2.imshow("Frame", frame)

        #Pausierung des programms 
        if cv2.waitKey(1) & 0xFF == ord('b'):
            print("Break")
            while True:
                if cv2.waitKey(1) & 0xFF == ord('b'):
                    print("Go")
                    break       
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            GenerateData(sharedList)
            break

    cap.release()
    cv2.destroyAllWindows()



def GenerateData(sharedList):
    """
    Führt erschwünschte Endmethoden zur Digitalisierung aus 
    """
    global XCOORD_LIST, YCOORD_LIST, WINKEL_LIST, DISTANZ_LIST
    
    widthToBitsPaul(XCOORD_LIST, sharedList)
    heightToBitsPaul(YCOORD_LIST, sharedList)
    LsbFloat(WINKEL_LIST, "bits.txt", sharedList)

    XCOORD_LIST, YCOORD_LIST, WINKEL_LIST, DISTANZ_LIST = [], [], [], []


# Überprüft ob die übergebene Zahl ein negatives Vorzeichen hat
def Sign(zahl):
    return -1 if (zahl < 0) else 1


def ClearTestSetup():
    """
    Löscht Inhalt der jeweiligen Files 
    """
    with open('output.csv', 'w') as f:
        f.write("")

    with open('bits.txt', 'w') as f:
        f.write("")     

def CheckMiddlePoint(x0, y0):
    """
    überprüft ob der Mittelpunkt des Pendels falsch gesetzt ist  
    """
    
def LsbFloat(floatList, file, sharedList):
    """
    Schreibt LSB einer Float (aus floatList) in file 
    """
    with open(file, 'w') as f:
        f.write("")
    for i in floatList:
        binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', i))
        if len(binary_str) > 8:
            lsb = binary_str[-1]
            write(lsb, file, sharedList)

def CapturePendelum(stopEvent, errorEvent ,sharedList):
    """
    Hauptmethode
    Startet Pendel 
    """
    CheckMiddlePoint(X_MIDDLE, Y_MIDDLE)
    ClearTestSetup()
    Capture(stopEvent,errorEvent ,sharedList)