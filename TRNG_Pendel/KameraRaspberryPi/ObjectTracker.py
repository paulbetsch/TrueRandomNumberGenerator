import cv2
import math
import struct
import time
import RPi.GPIO as GPIO
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
BINARY_STRING = ""
LOWER_TIMESTAMPS = []
UPPER_TIMESTAMPS = []

TIMESTAMPS = []
XCOORD_LIST = []
YCOORD_LIST = []
WINKEL_LIST = []
DISTANZ_LIST = []

LOWER_YCOORD_LIST = []
UPPER_YCOORD_LIST = []
LOWER_XCOORD_LIST = []
UPPER_XCOORD_LIST = []

UPPER_DISTANZ_LIST = []
LOWER_DISTANZ_LIST = []

LOWER_WINKEL_LIST = []
UPPER_WINKEL_LIST = []

LOWER_WINKEL_HEX = []
UPPER_WINKEL_HEX = []
#Schreibt alle Daten in CSV Datei mit: timestamp, x, y, abstand, winkel

def write(bit, file):
    with open(file, 'a') as f:
        f.write(bit)

def rangeToBits(XList, x0, file):
    with open(file, 'w') as f:
        f.write("")
    pixelRange = 2
    pixelRangesRight = [x0]
    pixelRangesLeft = [x0]
    for i in range (150):
        pixelRangesRight.append(pixelRangesRight[i] + pixelRange)
        pixelRangesLeft.append(pixelRangesLeft[i] - pixelRange)

    for x in XList:
        i = 0
        found = False
        if x < x0:
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

#Durchläuft liste mit Floats, schreibt lsbs in bin.txt

def LsbFloat(liste1, file):
# Löscht Inhalt bin.txt
    with open(file, 'w') as f:
        f.write("")

# Schreibt lsbs
    for i in liste1:
        binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', i))
        if len(binary_str) > 8:
            lsb = binary_str[-1]
            with open(file, 'a') as f:
                f.write(lsb)

def Capture(numbits):
    timestamp = time.time()
    StartEngine(3, 0, True);
    time.sleep(0.5)
    print("GO")
    while True:            
        if time.time() - timestamp > 10:
            StartEngine(2, 0, True);
            timestamp = time.time()
            time.sleep(0.5)
        #time.sleep(0.02)
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

                    #winkel = (winkel + 360) % 360  # Gradmaß zu 360 Grad System (anstatt 0-180 und 0 - (-180))
                    #angleStr = "Winkel: " + str(winkel)
                    #cv2.putText(frame, angleStr, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    #Ausgabe 
                    
                    if winkel > 0 and distanz < 220:  
                        #print(" -- LOWER -- count: " + str(len(LOWER_WINKEL_LIST) + 1) + "\n" + "   x   : " + str(float(x)) + "\n" + "   Y   : " + str(float(y)) +"\n" + "Winkel : " + str(winkel) + "\n"+ "Abstand: " + str(distanz) + "\n" + "----------------------------")
                        LOWER_XCOORD_LIST.append(float(x))
                        LOWER_YCOORD_LIST.append(float(y))
                        LOWER_DISTANZ_LIST.append(distanz)
                        LOWER_WINKEL_LIST.append(winkel)
                        LOWER_TIMESTAMPS.append(time.time())
                    elif winkel < 0 and distanz <220:
                        #print(" -- UPPER -- count: " + str(len(UPPER_WINKEL_LIST) + 1)  + "\n" + "   x   : " + str(float(x)) + "\n" + "   Y   : " + str(float(y)) +"\n" + "Winkel : " + str(winkel) + "\n"+ "Abstand: " + str(distanz) + "\n" + "----------------------------")
                        UPPER_XCOORD_LIST.append(float(x))
                        UPPER_YCOORD_LIST.append(float(y))
                        UPPER_DISTANZ_LIST.append(distanz)
                        UPPER_WINKEL_LIST.append(winkel)
                        UPPER_TIMESTAMPS.append(time.time())
                   
                    if distanz < 220:
                        print("Bits: " + str(len(XCOORD_LIST) * 2))
                        XCOORD_LIST.append(float(x))
                        YCOORD_LIST.append(float(y))
                        DISTANZ_LIST.append(distanz)
                        WINKEL_LIST.append(winkel)
                        TIMESTAMPS.append(time.time())

                    # Abfrage geschwindigkeit anpassen
                    time.sleep(0.01)
                cv2.imshow("Frame", frame)

        #Pausierung des programms 
        if cv2.waitKey(1) & 0xFF == ord('b'):
            print("Break")
            while True:
                if cv2.waitKey(1) & 0xFF == ord('b'):
                    print("Go")
                    break       
                
        if cv2.waitKey(1) & 0xFF == ord('q'):
            Coords(UPPER_XCOORD_LIST, UPPER_YCOORD_LIST, UPPER_DISTANZ_LIST, UPPER_WINKEL_LIST, UPPER_TIMESTAMPS, 'outputUpper.csv')
            Coords(LOWER_XCOORD_LIST,LOWER_YCOORD_LIST,LOWER_DISTANZ_LIST, LOWER_WINKEL_LIST, LOWER_TIMESTAMPS, 'outputLower.csv')
            Coords(XCOORD_LIST, YCOORD_LIST, DISTANZ_LIST, WINKEL_LIST, TIMESTAMPS, "output.csv")
            WinkelToHex16(UPPER_WINKEL_LIST, "UpperHexBits.txt")
            WinkelToHex16(LOWER_WINKEL_LIST, "LowerHexBits.txt")
            WinkelToHex32(UPPER_WINKEL_LIST, "UpperHexBits32.txt")
            WinkelToHex32(LOWER_WINKEL_LIST, "LowerHexBits32.txt")
            LsbFloat(WINKEL_LIST, "WinkelLsb.txt")
            LsbFloat(DISTANZ_LIST, "DistanzLsb.txt")
            rangeToBits(XCOORD_LIST, X_MIDDLE, "rangeBitsX.txt")
            rangeToBits(YCOORD_LIST, Y_MIDDLE, "rangeBitsY.txt")
            break
        
        #elif len(LOWER_WINKEL_LIST) > (numbits / 4) or len(UPPER_WINKEL_LIST) > (numbits / 4) or len(XCOORD_LIST) > numbits:
        elif len(XCOORD_LIST) > numbits:
            Coords(UPPER_XCOORD_LIST, UPPER_YCOORD_LIST, UPPER_DISTANZ_LIST, UPPER_WINKEL_LIST, UPPER_TIMESTAMPS, 'outputUpper.csv')
            Coords(LOWER_XCOORD_LIST,LOWER_YCOORD_LIST,LOWER_DISTANZ_LIST, LOWER_WINKEL_LIST, LOWER_TIMESTAMPS, 'outputLower.csv')
            Coords(XCOORD_LIST, YCOORD_LIST, DISTANZ_LIST, WINKEL_LIST, TIMESTAMPS, "output.csv")
            WinkelToHex(UPPER_WINKEL_LIST, "UpperHexBits.txt")
            WinkelToHex(LOWER_WINKEL_LIST, "LowerHexBits.txt")
            LsbFloat(WINKEL_LIST, "WinkelLsb.txt")
            LsbFloat(DISTANZ_LIST, "DistanzLsb.txt")
            WinkelToHex32(UPPER_WINKEL_LIST, "UpperHexBits32.txt")
            WinkelToHex32(LOWER_WINKEL_LIST, "LowerHexBits32.txt")
            rangeToBits(XCOORD_LIST, X_MIDDLE, "rangeBitsX.txt")
            rangeToBits(YCOORD_LIST, Y_MIDDLE, "rangeBitsY.txt")
            break

    cap.release()
    cv2.destroyAllWindows()

# Schreibt Hex Zahl für jeweikige Winkel Position
def WinkelToHex16(winkelList, file):
    with open(file, 'w') as f:
        f.write("")
    hexRanges = []
    hexCount = {}
    winkelHex = []
    hexRanges.append(0)
    # Initialisieren der Bereiche (unterer Halbkreis(pi) in 16 Bereiche teilen)
    for i in range(16):
        hexRanges.append(np.pi/ 16 * (i + 1))
        if hexCount.get(i) == None and i < 16:
            hexCount[i] = 0

    # Winkel den Bereichen zuordnen, in neue Liste schreiben, und zählen für Statisik
    for winkel in winkelList:
        if winkel < 0:
            winkel = winkel * -1
        for i in range(16):
            if winkel > hexRanges[i] and winkel < hexRanges[i + 1]:
                # Zählen der Haufigkeit
                hexCount[i] += 1
                # Hex bereich anhängen
                winkelHex.append(i)
                break
    
    bin_list = []

    # Hex ziffern in binär in bin.txt schreiben
    for hex_digit in winkelHex:
        bin_digit = bin(hex_digit)[2:].zfill(4)
        bin_list.append(bin_digit)
        with open(file, 'a') as f:
            f.write(bin_digit)
    
    # Ausgabe Statistik der Häufigkeiten
    print (hexCount)
    #import matplotlib.pyplot as plt

    #data = hexCount

    #plt.bar(data.keys(), data.values())
    #plt.xlabel('Hex')
    #plt.ylabel('Count')
    #plt.show()

# Schreibt Hex Zahl für jeweikige Winkel Position
def WinkelToHex32(winkelList, file):
    with open(file, 'w') as f:
        f.write("")
    hexRanges = []
    hexCount = {}
    winkelHex = []
    hexRanges.append(0)
    # Initialisieren der Bereiche (unterer Halbkreis(pi) in 16 Bereiche teilen)
    for i in range(32):
        hexRanges.append(np.pi/ 32 * (i + 1))
        if hexCount.get(i) == None and i < 32:
            hexCount[i] = 0


    # Winkel den Bereichen zuordnen, in neue Liste schreiben, und zählen für Statisik
    for winkel in winkelList:
        if winkel < 0:
            winkel = winkel * -1
        for i in range(32):
            if winkel > hexRanges[i] and winkel < hexRanges[i + 1]:
                # Zählen der Haufigkeit
                hexCount[i] += 1
                # Hex bereich anhängen
                if i < 16:
                    winkelHex.append(i)
                else:
                    winkelHex.append(i - 16)
                break
    
    bin_list = []

    # Hex ziffern in binär in bin.txt schreiben
    for hex_digit in winkelHex:
        bin_digit = bin(hex_digit)[2:].zfill(4)
        bin_list.append(bin_digit)
        with open(file, 'a') as f:
            f.write(bin_digit)
    
    print (hexCount)


# Ermittelt vorzeichen einer Zahl
def Sign(zahl):
    return -1 if (zahl < 0) else 1

def StartEngine(durationRunning, timeToWait, isRunning):
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
        isRunning = True
        # Ermöglicht den Stromfluss im Relay für den Motor
        GPIO.output(6,1)
        # Ermöglicht den Stromfluss im Relay fü den Hubmagnet
        GPIO.output(13,0)
    
    # Unterbrechung des Stromflusses im Relay für den Motor
    GPIO.output(6,0)   
    # Unterbrechung des Stromflusses im Relay für den Hubmagnet   
    GPIO.output(13,1)
    isRunning = False   
    # GPIO.cleanup()

def ClearTestSetup():

    with open('output.csv', 'w') as f:
        f.write("")

    with open('outputUpper.csv', 'w') as f:
        f.write("")

    with open('outputLower.csv', 'w') as f:
        f.write("")

    with open('LowerHexBits.txt', 'w') as f:
        f.write("")
    
    with open('UpperHexBits.txt', 'w') as f:
        f.write("")

    with open('lsbBitsCoordsXy.txt') as f:
        f.write("")

    with open('lsbBitsCoordsWinkelDistanz.txt') as f:
        f.write("")

    with open('LowerHexBitsInCircle.txt', 'w') as f:
        f.write("")
    
    with open('UpperHexBitsInCircle.txt', 'w') as f:
        f.write("")


# For Final System
def CapturePendelum(numBits, returnValue):
    Capture(numBits)
    returnvalue = BINARY_STRING
    return returnValue

def CapturePendelumTest(numBits):
    print("Start captureing")
    Capture(numBits)


CapturePendelumTest(100000)

