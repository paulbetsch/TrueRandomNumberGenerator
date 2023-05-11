import cv2
import math
import struct
import time
import numpy as np

#um Programm zu stoppen "q" in geöffnetem Fenster drücken
#Video Capture anpassen - 0 = Standard Kamera , 1 = Externe Kamera ...

cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
#ret, frame = cap.read()
#height, width, channels = frame.shape
#RGB reichweite für Punkte
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (235, 235, 85)

#Mittelpunkt für Polar Koordinaten System

X_MIDDLE = 305
Y_MIDDLE = 233

#Minimum Fläche für Punkt

MIN_AREA = 150

#Daten

XCOORD_LIST = []
YCOORD_LIST = []
DISTANZ_LIST = []
WINKEL_LIST = []
TIMESTAMPS = []
WINKEL_HEX = []
#Schreibt alle Daten in CSV Datei mit: timestamp, x, y, abstand, winkel

def Coords():
    # Überschreibt alte CSV Datei und schreibt Kopfzeile
    with open('output.csv', 'w') as f:
        f.write("timestamp, x, y, abstand, winkel" + "\n")

    # Schreibt Daten in CSV
    n = 0
    for x in TIMESTAMPS:
        with open('output.csv', 'a') as f:
            #print(str(x) + ", " + str(xcoord_list[n]) + ", " + str(ycoord_list[n]) + ", " + str(distanz_list[n]) + ", " + str(winkel_list[n]) + "\n")
            f.write(str(x) + ", " + str(XCOORD_LIST[n]) + ", " + str(YCOORD_LIST[n]) + ", " + str(DISTANZ_LIST[n]) + ", " + str(WINKEL_LIST[n]) + "\n")
        n += 1

#Durchläuft liste mit Floats, schreibt lsbs in bin.txt

def LsbFloat(liste):
# Löscht Inhalt bin.txt
#with open('bin.txt', 'w') as f:
#    f.write("")

# Schreibt lsbs
    for i in liste:
        binary_str = ''.join(format(c, '08b') for c in struct.pack('!f', i))
        if len(binary_str) > 8:
            lsb = binary_str[-1]
            with open('bin.txt', 'a') as f:
                f.write(lsb)

def Capture():
    while True:

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
                    TIMESTAMPS.append(time.time())
                    center = (float(x), float(y))
                    radius = int(radius)
                    #Kreis zum Mittelpunkt
                    cv2.circle(frame, (int(X_MIDDLE), int(Y_MIDDLE)), 2, (255, 255, 255), 2)
                    # Kreis zum schwarzen Punkt 
                    cv2.circle(frame, (int(x), int(y)), 5, (0, 255, 0), 2)
                    #Linie zu Punkt
                    cv2.line(frame, (int(X_MIDDLE), int(Y_MIDDLE)), (int(x), int(y)), (0, 0, 255), 2)
                    
                    
                    dx = float(x) - X_MIDDLE
                    dy = float(y) - Y_MIDDLE 
                    distanz = math.sqrt(dx ** 2 + dy ** 2)
            
                    winkel = math.acos(dx/distanz) * Sign(dy) # Winkel berechnung in Bogenmaß

                    #winkel = (winkel + 360) % 360  # Gradmaß zu 360 Grad System (anstatt 0-180 und 0 - (-180))
                    angleStr = "Winkel: " + str(winkel)
                    cv2.putText(frame, angleStr, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                    
                    #Ausgabe 
                    print("   x   : " + str(float(x)) + "\n" + "   Y   : " + str(float(y)) +"\n" + "Winkel : " + str(winkel) + "\n"+ "Abstand: " + str(distanz) + "\n" + "----------------------------")
                    if winkel > 0 and distanz < 220:  
                        XCOORD_LIST.append(float(x))
                        YCOORD_LIST.append(float(y))
                        DISTANZ_LIST.append(distanz)
                        WINKEL_LIST.append(winkel)
                    # Abfrage geschwindigkeit anpassen
                    time.sleep(0.12)
                
        cv2.imshow("Frame", frame)
        # when q gedrückt beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Schreibt Hex Zahl für jeweikige Winkel Position
def WinkelToHex(WINKEL_LIST):
    hexRanges = []
    hexCount = {}
    hexRanges.append(0)
    # Initialisieren der Bereiche (unterer Halbkreis(pi) in 16 Bereiche teilen)
    for i in range(16):
        hexRanges.append(np.pi/ 16 * (i + 1))
        if hexCount.get(i) == None and i < 16:
            hexCount[i] = 0

    # Winkel den Bereichen zuordnen, in neue Liste schreiben, und zählen für Statisik
    for winkel in WINKEL_LIST:
        for i in range(16):
            if winkel > hexRanges[i] and winkel < hexRanges[i + 1]:
                # Zählen der Haufigkeit
                hexCount[i] += 1

                # Hex bereich anhängen
                WINKEL_HEX.append(i)
                break
    

    bin_list = []

    # Hex ziffern in binär in bin.txt schreiben
    for hex_digit in WINKEL_HEX:
        bin_digit = bin(hex_digit)[2:].zfill(4)
        bin_list.append(bin_digit)
        with open('bin.txt', 'a') as f:
            f.write(bin_digit)
            print(bin_digit)
    
    # Ausgabe Statistik der Häufigkeiten
    print(hexCount)
    import matplotlib.pyplot as plt

    data = hexCount

    plt.bar(data.keys(), data.values())
    plt.xlabel('Hex')
    plt.ylabel('Count')
    plt.show()




# Ermittelt vorzeichen einer Zahl
def Sign(zahl):
    return -1 if (zahl < 0) else 1

# Startet Skript, Hauptmethode
def CapturePendelum():
    Capture()
    # LsbFloat(WINKEL_LIST)
    # LsbFloat(XCOORD_LIST)
    # LsbFloat(YCOORD_LIST)
    # LsbFloat(DISTANZ_LIST)
    # Coords()
    WinkelToHex(WINKEL_LIST)

CapturePendelum()

