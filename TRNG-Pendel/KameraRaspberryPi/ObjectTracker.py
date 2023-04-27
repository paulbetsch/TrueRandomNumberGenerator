import cv2
import math
import struct
import time
import datetime

# um Programm zu stoppen "q" in geöffnetem Fenster drücken 
# Video Capture anpassen - 0 = Standard Kamera , 1 = Externe Kamera ...
cap = cv2.VideoCapture(0)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
ret, frame = cap.read()
height, width, channels = frame.shape
#RGB reichweite für Punkte
LOWER_BLACK = (0, 0, 0)
UPPER_BLACK = (255, 255, 90)
# Mittelpunkt für Polar Koordinaten System
X_MIDDLE = width / 2 + 7
Y_MIDDLE = height / 2 - 34
# Minimum Fläche für Punkt
MIN_AREA = 110

# Daten
XCOORD_LIST = []
YCOORD_LIST = []
DISTANZ_LIST = []
WINKEL_LIST = []
TIMESTAMPS = []

# Schreibt alle Daten in CSV Datei mit: timestamp, x, y, abstand, winkel
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


# Durchläuft liste mit Floats, schreibt lsbs in bin.txt
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

# Methode erkennt Punkte aus Live Stream - q gedrückt halten um zu Beenden - b für Pause (im Fenster drücken)
def Capture():
    while True:
        counter = 0
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, LOWER_BLACK, UPPER_BLACK)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Sortiere Konturen nach Fläche in absteigender Reihenfolge, nur die größten 2 Nehmen
        contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]

        for contour in contours:
            # Compute the center and radius of the contour
            (x, y), radius = cv2.minEnclosingCircle(contour)
            area = cv2.contourArea(contour)
            if area >= MIN_AREA:
                TIMESTAMPS.append(datetime.datetime.fromtimestamp(time.time()).strftime('%H:%M:%S.%f'))
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
        
                winkel = math.acos(dx/distanz) * sign(dy) # Winkel berechnung in Bogenmaß

                #winkel = (winkel + 360) % 360  # Gradmaß zu 360 Grad System (anstatt 0-180 und 0 - (-180))
                angleStr = "Winkel: " + str(winkel)
                cv2.putText(frame, angleStr, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                #Ausgabe
                print("   x   : " + str(float(x)) + "\n" + "   Y   : " + str(float(y)) +"\n" + "Winkel : " + str(winkel) + "\n"+ "Abstand: " + str(distanz) + "\n" + "----------------------------")
                XCOORD_LIST.append(float(x))
                YCOORD_LIST.append(float(y))
                DISTANZ_LIST.append(distanz)
                WINKEL_LIST.append(winkel)
                # Abfrage geschwindigkeit anpassen
                time.sleep(0.01)
                counter += 1
            
        cv2.imshow("Frame", frame)
        # when q gedrückt beenden
        
        if cv2.waitKey(1) & 0xFF == ord('b'):
            print("Pause")
            Pause = True
            for i in range(4):
                time.sleep(1)
                print(i + 1)
            print("swing")
            for i in range(2):
                time.sleep(1)
                print(i + 1)
                    
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Gibt vorzeichen einer Zahl zurück
def sign(zahl):
    if zahl < 0:
        return -1
    else:
        return 1

def __main__():
    Capture()
    Coords()

__main__()

