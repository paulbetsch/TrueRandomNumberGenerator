import cv2
import math
import struct
import time

# um Programm zu stoppen "q" in geöffnetem Fenster drücken 
# Video Capture anpassen - 0 = Standard Kamera , 1 = Externe Kamera ...
cap = cv2.VideoCapture(0)
#RGB reichweite für Punkte
lower_black = (0, 0, 0)
upper_black = (255, 255, 80)
# Mittelpunkt für Polar Koordinaten System
x_middle = 290
y_middle = 215
# Minimum Fläche für Punkt
min_contour_area = 100

# Daten
xcoord_list = []
ycoord_list = []
distanz_list = []
winkel_list = []
timestamps = []

# Schreibt alle Daten in CSV Datei mit: timestamp, x, y, abstand, winkel
def coords():
    # Überschreibt alte CSV Datei und schreibt Kopfzeile
    with open('output.csv', 'w') as f:
        f.write("timestamp, x, y, abstand, winkel" + "\n")

    # Schreibt Daten in CSV
    n = 0
    for x in timestamps:
        with open('output.csv', 'a') as f:
            #print(str(x) + ", " + str(xcoord_list[n]) + ", " + str(ycoord_list[n]) + ", " + str(distanz_list[n]) + ", " + str(winkel_list[n]) + "\n")
            f.write(str(x) + ", " + str(xcoord_list[n]) + ", " + str(ycoord_list[n]) + ", " + str(distanz_list[n]) + ", " + str(winkel_list[n]) + "\n")
        n += 1


# Durchläuft liste mit Floats, schreibt lsbs in bin.txt
def lsbFloat(liste):
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

def capture():

    while True:
        ret, frame = cap.read()
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_black, upper_black)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        for contour in contours:
            area = cv2.contourArea(contour)
            if area >= min_contour_area:
                # Compute the center and radius of the contour
                (x, y), radius = cv2.minEnclosingCircle(contour)
                timestamps.append(time.time())
                center = (float(x), float(y))
                radius = int(radius)
                
                # Kreis um Punkt
                cv2.circle(frame, (int(x), int(y)), radius, (0, 255, 0), 2)
                
                # Linie zu Punkt
                cv2.line(frame, (int(x_middle), int(y_middle)), (int(x), int(y)), (0, 0, 255), 2)
                
                dx = x_middle - float(x)
                dy = y_middle - float(y)
                distanz = math.sqrt(dx ** 2 + dy ** 2)
        
                winkel = math.degrees(math.atan2(dy, dx))  # Winkel berechnung in Gradmaß
                winkel = (winkel + 360) % 360  # Gradmaß zu 360 Grad System (anstatt 0-180 und 0 - (-180))
                angle_str = "Winkel: " + str(round(x, 2)) + " Grad"
                cv2.putText(frame, angle_str, (int(x), int(y)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
                #Ausgabe 
                print("Black object position: x " + str(float(x)) + " y " + str(float(y)))
                print("Black Object winkel: " + str(winkel) + " abstand " + str(distanz)) 
                xcoord_list.append(float(x))
                ycoord_list.append(float(y))
                distanz_list.append(distanz)
                winkel_list.append(winkel)
                # Abfrage geschwindigkeit anpassen
                time.sleep(0.008)
                
        cv2.imshow("Frame", frame)
        # when q gedrückt beenden
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

capture()
lsbFloat(winkel_list)
coords()
