from PIL import Image
import os.path
import cv2 as cv
import math
import numpy as np
import csv
import math
from zipfile import ZipFile
import shutil

#Gibt RGB Reichweiten für die Punkte zum Scannen zurück
#rgb" "= [r<,g<,b<,r>,g>,b>]
def GetRgbValues():
    rgbBlack = [0, 0, 0, 5, 5, 5]
    #rgbGreen = [40, 110, 95, 65, 125, 100]
    # rgbYellow = [190, 167, 65, 220, 185, 100]
    #rgbBlue = [45, 110, 135, 70, 130 ,160]
    # Add all colours you want to add, to the return variable
    rgbAll = [rgbBlack]#, rgbYellow]#, rgbGreen]
    return rgbAll


def ScanDots(im, path, width, height, rgb):
    counter = summeX = summeY = 0
    dotsAvg = []
    rgb_im = im.convert("RGB")

    # print("Beginning to search for Black Dots")
    for x in range(width):
        for y in range(height):
            r, g, b = rgb_im.getpixel((x, y))
            # Nach Punkten in allen gegebenen Farben suchen
            for i in range(len(rgb)):
                # Hier wird der Aktuelle Pixel auf den Farbbereich geprüft
                if (r >= rgb[i][0] and g >= rgb[i][1] and b >= rgb[i][2]) and (r <= rgb[i][3] and g <= rgb[i][4] and b <= rgb[i][5]):
                    # print("Pixel an X: " + str(x) + " und Y: " + str(y))
                    counter, summeX, summeY = counter + 1, summeX + x, summeY + y
                    avg = summeX / counter

                    # TODO die dichte der Punkte innerhalb eines Bereiches überprüfen
                    # Jeder weiterer Punkt muss mehr als 30 Pixel von dem aktuellen entfernt sein
                    if x < avg - 30 or x > avg + 30:
                        dotsAvg.append([(summeX / counter), (summeY / counter)])
                        summeX = summeY = counter = 0

    if not counter == 0:
        dotsAvg.append([(summeX / counter), (summeY / counter)])
    
    # with open('resultsXY.csv', 'a', newline='') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     if(len(dotsAvg) == 2):
    #         csvwriter.writerow([path, dotsAvg[0][0], dotsAvg[0][1], dotsAvg[1][0], dotsAvg[1][1]])
    #print('Dots AVG: ' + str(dotsAvg))
    return dotsAvg


# Sucht nach den übergebenen RGB werten in dem übergebenen Bild und gibt ein Array mit den Winkeln und der
# Distanz zum übergebenen Mittelpunkt x0,y0 zurück
# [(d1, w1), (d2, w2), (d3, w3)]
def ScanDotsPolar(image, path, width, height, rgb, x0, y0):
    dotsAvg = ScanDots(image, path, width, height, rgb)
    coords = []

    # Für jeden gefundenen Punkt die Berechnung durchführen
    for x, y in dotsAvg:
        # Umrechnung der XY-Koordinaten ins Polarkoordinatensystem
        dx = x - x0
        dy = y - y0
        abstand = math.sqrt(dx**2 + dy**2)
        winkel = math.acos(dx/abstand) * sign(dy)
        # Abstand und Winkel der Punkte zur rückgabe Variable hinzufügen
        coords.append([abstand, winkel])

    with open('resultsPolar.csv', 'a', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)
        if(len(coords) == 2):
            csvwriter.writerow([path, coords[0][0], coords[0][1], coords[1][0], coords[1][1]])
    return coords


def GetWidth(image):
    return image.size[0]
 
def GetHeight(image):
    return image.size[1]

# Gibt -1 zurück wenn die übergebene Zahl kleiner 0 ist und 1 wenn sie größer als 0 ist
def sign(x):
    if x == 0:
        return 0
    elif x < 0:
        return -1
    else:
        return 1


# Läd Bild des angegebenen Pfades und gibt es zurück
def LoadImage(path):
    try:
        im = Image.open(path)
    except FileNotFoundError  as e:
        print(" ")
        print(str(path) + " not found.")
    else:
        print(" ")
        print(str(path) + " loaded.")
        return im
    return 0

# Läuft durch alle Bilder (benannt "idx".jpg) im angebenen Pfad
# Ruft Scan Methode auf speichter rückgabe Werte in all_results (jeweils 1 result pro Bild) 
def Analyse(file, idx, endIdx, isPolar):
    rgb = GetRgbValues()
    all_results = []
    dir = os.getcwd() + file
    for i in range (20, 70):
        idx = 2
        while(idx < endIdx):
            image = LoadImage(dir + str(i) + '\\' + str(idx) + ".jpg")
            if image != 0:
                if isPolar:
                    # Determine Middlepoint of the coordinates
                    resultPolar = ScanDotsPolar(image, str(i) + '\\' + str(idx) + ".jpg", GetWidth(image), GetHeight(image), rgb, 1204, 465)
                    if (int(len(resultPolar) / 2)) == 2:
                        print("Valid coords - appended")   
                        all_results.append(resultPolar)
                else:
                    resultXY = ScanDots(image, str(i) + '\\' + str(idx) + ".jpg", GetWidth(image), GetHeight(image), rgb)
                    if (int(len(resultXY) / 2)) == 2:
                        print("Valid coords - appended")   
                        all_results.append(resultXY)
            idx += 1
    return all_results

# Extract files into a temporary directory
def extractData(TMP_DIR_NAME):
    # Ensure the temporary directory doesnt exists
    if(os.path.isdir(TMP_DIR_NAME)):
        shutil.rmtree(TMP_DIR_NAME)
    # Extract all files of the ZIP FILE into a temporary dircectory
    with ZipFile('Pictures.zip', 'r') as zip:
        zip.extractall(TMP_DIR_NAME)


if __name__ == "__main__": 
    # extractData('Pictures')
    # if(os.path.isdir('Pictures')):
    #     print("Bilder entzippt.")
    # else:
    #     print('Bilder nicht entzippt.')
    #     exit()
    # columnNames = ['Timestamp/Bildnummer', 'X-Wert Punk1', 'Y-Wert Punkt1', 'X-WertPunkt2', 'Y-Wert Punkt2', 'Stecke Punkt1', 'Winkel Punkt1', 'Strecke Punkt2', 'Winkel Punkt2']
    # with open('resultsPolar.csv', 'w') as csvfile:
    #     csvwriter = csv.writer(csvfile)
    #     headers = ['Timestamp/Bildnummer', 'Srecker Punkt1', 'Winkel Punkt1', 'Strecke Punkt2', 'Winkel Punkt2']
    #     csvwriter.writerow(headers)
    with open('resultsXY.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)
        headers = ['Timestamp/Bildnummer', 'X-Wert Punk1', 'Y-Wert Punkt1', 'X-WertPunkt2', 'Y-Wert Punkt2']
        csvwriter.writerow(headers)
    print('CSV-FILES HEADER WRITTEN!')
    # Ordnerpfad, Bildbenennung (ohne Name leerer String), StartIdx Bilder, EndIdx Bilder
    # resultsXY = Analyse("\\Pictures" + "\\", 2, 299, False)
    resultsPolar = Analyse("\\Pictures" + "\\", 2, 299, True)
    #img = LoadImage('Pictures\\6\\15.jpg')
    #result = ScanDotsPolar(img, GetWidth(img), GetHeight(img), GetRgbValues(), 1204, 456)
    print('Ergebnis: ' + str(resultsPolar))
    #shutil.rmtree('Pictures')
    pass