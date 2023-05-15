import math
from KoordinatenInBildKonvertierer import *

# radius: Radius des Kreises auf dem die Punkte berechnet werden sollen
# mittelpunkt: Mittelpunkt des Kreises als Tupel (X-Koordinate, Y-Koordinate) auf dem die Punkte berechnet werden sollen 
# anzahlPunkte: Anzahl der Punkte die auf dem Kreis berechnet werden sollen
def berechnePunkteAufKreis(radius, mittelpunkt, anzahlPunkte):
    x0, y0 = mittelpunkt
    punkte = []
    for i in range(anzahlPunkte):
        # Triviale Formeln für berechnung in einem Kreis und in einem Dreieck
        theta = 2 * math.pi * i / anzahlPunkte
        y = y0 + (radius * math.sin(theta))
        x = x0 + (radius * math.cos(theta))
        punkte.append(((int(x)), (int(y))))
    return punkte


# pendelnummer: Gibt an von welchem Pendel der theoretisch erwartbaren Raum zu generieren ist
# 1 -> Einfaches Pendel
# 2 -> Doppelpendel
# 3 -> Tri-Pendel
def berechnePendelErwartungsraumMitHäufigkeiten(pendelnummer):
    # Der Mittelpunkt soll mit dem Mittelpunkt im Skript "KordinatenInBildKonvertierer" überein stimmen
    mittelpunkte = [(600,600)]
    wertebereich = {}

    # Berechnung muss ab dem ersten Pendel starten, da die vorherigen Pendelerwartungsräume benötigt werden
    # um den Erwartungsraum des nächsten Pendel zuberechnen
    for anzahl in range(pendelnummer):
        print("Berechne Punkte für Pendel "+str(anzahl+1))
        neuePunkte = []
        anzahlMittelpunkte = len(mittelpunkte)
        progessCounter = 0
        for punkt in mittelpunkte:
            if(progessCounter % 2500 == 0):
                print(str(round((progessCounter / anzahlMittelpunkte * 100),2)) + "%")

            progessCounter += 1
            neuePunkte += berechnePunkteAufKreis(150, punkt, 1000)
            if(anzahl == pendelnummer-1):
                for tupel in neuePunkte:
                    if wertebereich.get(tupel) == None:
                        wertebereich[tupel] = 1
                    else:
                        wertebereich[tupel] = wertebereich[tupel] +1
                neuePunkte = []

        print("Berechnung Punkte für Pendel "+str(anzahl+1) + " fertig")
        mittelpunkte = neuePunkte
    return wertebereich



generatePictureOutOfDictionary(berechnePendelErwartungsraumMitHäufigkeiten(3))







