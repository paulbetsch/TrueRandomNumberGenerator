import cv2
import math
import struct
import time
from Engine import motor
# RPi.GPIO as GPIO
from time import sleep    
import keyboard
import numpy as np

#um Programm zu stoppen "q" in geöffnetem Fenster drücken
#Video Capture anpassen - 0 = Standard Kamera , 1 = Externe Kamera ...


cap = cv2.VideoCapture(0)

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#ret, frame = cap.read()
#height, width, channels = frame.shape
#RGB reichweite für Punkte
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (255, 255, 55)

#Mittelpunkt für Polar Koordinaten System

X_MIDDLE = 323  
Y_MIDDLE = 235

#Minimum Fläche für Punkt

MIN_AREA = 20

#Daten
TIMESTAMPS = []
XCOORD_LIST = []
YCOORD_LIST = []
WINKEL_LIST = []
DISTANZ_LIST = []



def write(bit, file):
    """
    Schreibt bit in file
    """
    with open(file, 'a') as f:
        f.write(bit)


def rangeToBits(coordList, middle, file, pixelRange):
    """
    coordList - Liste mit X oder Y Koordinaten
    middle - Mittelpunkt X oder Y (Pendelmitte)
    file - In welche File die Daten zu schreiben sind
    """
    parts = 240 / pixelRange
    pixelRangesRight = [middle]
    pixelRangesLeft = [middle]
    for i in range (150):
        pixelRangesRight.append(pixelRangesRight[i] + pixelRange)
        pixelRangesLeft.append(pixelRangesLeft[i] - pixelRange)

    for x in coordList:
        i = 0
        found = False
        if x < middle:
            while found == False and i < len(pixelRangesLeft) - 1:
                if x <= pixelRangesLeft[i] and x > pixelRangesLeft[i+1]:
                    #print(str(pixelRangesLeft[i]) +  " > " + str(x)  + " > " + str(pixelRangesLeft[i+1]))
                    found = True
                    write("0", file)
                i += 2
            if found == False:
                write("1", file)
        else:
            while found == False and i < len(pixelRangesRight) - 1:
                if x > pixelRangesRight[i] and x <= pixelRangesRight[i+1]:
                    #print(str(pixelRangesRight[i]) +  " < " + str(x)  + " < " + str(pixelRangesRight[i+1]))
                    found = True
                    write("1", file)
                i += 2
            if found == False:
                write("0", file)

def Coords(xcoordList, ycoordList, distanzList, winkelList, timestamps, file):
    """
    Schreibt Parameter in Datei (file)
    Erste Zeile Kopfzeile: timestamp, x Koordinate, y Koordinate, abstand, winkel
    Jede Zeile entspricht 1 Punkt - timestamp, x Koordinate, y Koordinate, abstand, winkel
    """

    print("write Coords to " + file + " count " + str(len(timestamps)) + ", "  +str(len(xcoordList)) + ", " + str(len(ycoordList)) + ", " + str(len(distanzList)) + ", " + str(len(winkelList)))
     # Überschreibt alte CSV Datei und schreibt Kopfzeile
    with open(file, 'w') as f:
        f.write("timestamp, x, y, abstand, winkel" + "\n")

    # Schreibt Daten in CSV
    n = 0
    for x in timestamps:
        with open(file, 'a') as f:
            #print(str(x) + ", " + str(xcoord_list[n]) + ", " + str(ycoord_list[n]) + ", " + str(distanz_list[n]) + ", " + str(winkel_list[n]) + "\n")
            f.write(str(x) + ", " + str(xcoordList[n]) + ", " + str(ycoordList[n]) + ", " + str(distanzList[n]) + ", " + str(winkelList[n]) + "\n")
        n += 1


def Capture(numbits):
    """
    Tracked Konturen aus einem Live Stream, schreibt Koordinaten x, y und abstand, winkel (polares Koordinaten System)
    Solange bis "q" im geöffneten Fenster gedrückt wird oder die Gewünschte anzahl an Bits (numbits) erreicht wurde 
    """
    timestamp = time.time()
    motor.StartEngine(3, 0, True)
    #time.sleep(0.5)
    print(" ")
    print("Start Camera")
    while True:            
        if time.time() - timestamp > 10:
            motor.StartEngine(2, 0, True)
            timestamp = time.time()
            time.sleep(0.5)
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
                        print("Bits: " + str(len(XCOORD_LIST) * 2))
                        XCOORD_LIST.append(float(x))
                        YCOORD_LIST.append(float(y))
                        DISTANZ_LIST.append(distanz)
                        WINKEL_LIST.append(winkel)
                        TIMESTAMPS.append(time.time())

                    # Abfrage geschwindigkeit anpassen
                    #time.sleep(0.01)
                cv2.imshow("Frame", frame)

        #Pausierung des programms 
        if cv2.waitKey(1) & 0xFF == ord('b'):
            print("Break")
            while True:
                if cv2.waitKey(1) & 0xFF == ord('b'):
                    print("Go")
                    break       
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            GenerateData()
            break
        
        # Sobald gewünschte Anzahl an Bits erreicht ist, Daten 
        elif len(XCOORD_LIST) * 2 > numbits:
            GenerateData()
            break

    cap.release()
    cv2.destroyAllWindows()



def GenerateData():
    """
    Führt erschwünschte Endmethoden zur Digitalisierung aus 
    """

    Coords(XCOORD_LIST, YCOORD_LIST, DISTANZ_LIST, WINKEL_LIST, TIMESTAMPS, "TRNG_Pendel\\KameraRaspberryPi\\output.csv")
    rangeToBits(XCOORD_LIST, X_MIDDLE, "TRNG_Pendel\\KameraRaspberryPi\\bits.txt", 2)
    rangeToBits(YCOORD_LIST, Y_MIDDLE, "TRNG_Pendel\\KameraRaspberryPi\\bits.txt", 2)


def Sign(zahl):
    """
    Ermittelt vorzeichen einer Zahl
    """

    if zahl < 0:
        return -1
    else:
        return 1


def ClearTestSetup():
    """
    Löscht Inhalt der jeweiligen Files 
    """

    with open('TRNG_Pendel\\KameraRaspberryPi\\output.csv', 'w') as f:
        f.write("")

    with open('TRNG_Pendel\\KameraRaspberryPi\\bits.txt', 'w') as f:
        f.write("")

    with open('TRNG_Pendel\\KameraRaspberryPi\\Rangebits02.txt', 'w') as f:
        f.write("")
    
    with open('TRNG_Pendel\\KameraRaspberryPi\\Range05.txt', 'w') as f:
        f.write("")
    
    with open('TRNG_Pendel\\KameraRaspberryPi\\Range1bits.txt', 'w') as f:
        f.write("")
    
    with open('TRNG_Pendel\\KameraRaspberryPi\\Range2bits.txt', 'w') as f:
        f.write("")


def splitIntoQty(inputFile, qty, bits, returnValue):
    """
    Teilt generierte Bits aus inputFile in die gewünschte Qty und länge der BitWords
    Gibt  Liste (returnValue) zurück mit je 1 BitWord als Eintrag in Liste
    Gesamt Liste hat Länge Qty
    """

    with open(inputFile, 'r') as f:
        bitStr = f.read().strip()
        if len(bitStr) < qty * bits:
            raise Exception("insufficient amount of bits in File: " + str(inputFile))

        num_bits = len(bitStr)
        returnValue = [bitStr[i:i+bits] for i in range(0, num_bits, bits)]

        # Letzten Wert mit 0 füllen falls anzahl nicht reicht
        lastValueLen = len(returnValue[-1])
        if lastValueLen < bits:
            returnValue[-1] += '0' * (bits - lastValueLen)

        while len(returnValue) > qty:
            returnValue.pop()
        
        return returnValue
        


def CheckMiddlePoint(x0, y0):
    """
    überprüft ob der Mittelpunkt des Pendels falsch gesetzt ist  
    """
    


def CapturePendelum(bits, qty, returnValue):
    """
    Hauptmethode
    Startet Pendel 
    Teilt dannach Bits in geteilte qty und schreibt in returnValue
    """
    CheckMiddlePoint(X_MIDDLE, Y_MIDDLE)
    ClearTestSetup()
    Capture(bits * qty)
    returnValue = splitIntoQty("TRNG_Pendel\\KameraRaspberryPi\\bits.txt", qty, bits, returnValue)

