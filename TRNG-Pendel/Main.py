from PIL import Image
import hashlib
import os.path
import cv2 as cv
import math
import struct
import hashlib
import numpy as np
import csv
import math
import decimal


# Berechnet Shannon Entropie des angegebenen Files (nur Nullen und einsen)
def shannonEntropy(file_path):
    with open(file_path, "r") as f:
        data = f.read().replace(" ", "").replace("\n", "")

    n = len(data)
    zeros = data.count("0")
    ones = data.count("1")
    p_zero = decimal.Decimal(zeros) / decimal.Decimal(n)
    p_one = decimal.Decimal(ones) / decimal.Decimal(n)

    entropy = - (p_zero * decimal.Decimal(math.log2(p_zero)) + p_one * decimal.Decimal(math.log2(p_one)))
    print(f"Shannon-Entropy: {entropy:.20f}")
    return entropy

# Zeigt die Verteilung von Nullen und Einsen im angebenen File 
def verteilung(file_path):
    # Öffnen der Datei im Lesemodus
    with open(file_path, "r") as f:
        # Lesen des Dateiinhalts und Entfernen von Leerzeichen und Zeilenumbrüchen
        data = f.read().replace(" ", "").replace("\n", "")
    zeros = data.count("0")
    ones = data.count("1")
    print("1: - " + str(ones))
    print("0: - " + str(zeros))

# Löscht angegebene File und erstellt sie neu
def DeleteFileContents(filename):
    filename = os.getcwd() + '\\' + filename
    if os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')
            print(filename + " cleared")
    else:
        print(filename + " not found")

# Läd Bild des angegebenen Pfades und gibt es zurück
def LoadImage(path):
    try:
        im = Image.open(path)
    except FileNotFoundError  as e:
        print(" ")
        print(str(path) + " not found .")
    else:
        print(" ")
        print(str(path) + " loaded.")
        return im
    return 0
 
def GetWidth(image):
    return image.size[0]
 
def GetHeight(image):
    return image.size[1]
 
#Gibt RGB Reichweiten für die Punkte zum Scannen zurück
#rgb" "= [r<,g<,b<,r>,g>,b>]
def GetRgbValues():
    rgbGreen = [40, 110, 95, 65, 125, 100]
    rgbYellow = [190, 167, 65, 220, 185, 100]
    #rgbBlue = [45, 110, 135, 70, 130 ,160]
    rgbAll = [rgbYellow, rgbGreen]
    return rgbAll
 
# Sucht nach den übergebenen RGB werten in dem übergebenen Bild und gibt ein Array mit den Koordinaten
# der jeweilig gefunden Punkte für die RGB werte zurück
# [(x1,y1),(x2,y2),(x3,y3)]
def ScanDots(image, width, height, rgb):
    coords = []
    # für jede RGB reichtweite ein durchlauf
    for i in range(len(rgb)):
        counter = summeX = summeY = 0
        dotsAvg = []
        np_im = np.array(image)
        # RGB reichweiten deklarieren
        mask = np.logical_and.reduce((np_im[:,:,0] >= rgb[i][0], np_im[:,:,1] >= rgb[i][1], np_im[:,:,2] >= rgb[i][2],
                                      np_im[:,:,0] <= rgb[i][3], np_im[:,:,1] <= rgb[i][4], np_im[:,:,2] <= rgb[i][5]))
        pixels = np.transpose(np.where(mask))
        for x, y in pixels:
            counter, summeX, summeY = counter + 1, summeX + x, summeY + y
            avg = summeX / counter

            # Wenn der Abstand zweier Pixel innerhalb 70 Pixel liegt gehört es noch zu dem aktuellen Punkt
            if x < avg - 70 or x > avg + 70:
                dotsAvg.append((summeX / counter))
                dotsAvg.append((summeY / counter))
                summeX = summeY = counter = 0
 
        if not counter == 0:
            dotsAvg.append((summeX / counter))
            dotsAvg.append((summeY / counter))
            print(str(int(len(dotsAvg) / 2)) + " Punkt wurde für "  + str(rgb[i][0]) + " =< R >= " + str(rgb[i][1]) + " " + 
                str(rgb[i][2]) + " =< G >= " + str(rgb[i][3]) + " " +str(rgb[i][4]) + " =< B >= " + str(rgb[i][5]) + " gefunden")
            if (int(len(dotsAvg) / 2)) == 1:
                print("Valid coords - appended")
                coords.append(dotsAvg)    
    return coords

# Sucht nach den übergebenen RGB werten in dem übergebenen Bild und gibt ein Array mit den Winkeln und der
# Distanz zum übergebenen Mittelpunkt x0,y0 zurück
# [(d1, w1), (d2, w2), (d3, w3)]
def ScanDotsPolar(image, width, height, rgb, x0, y0):
    coords = []
    # für jede übergebene RGB reichtweite im Array ein durchlauf
    for i in range(len(rgb)):
        counter = summeX = summeY = 0
        dotsAvg = []
        np_im = np.array(image)
        # RGB reichweiten deklarieren
        mask = np.logical_and.reduce((np_im[:,:,0] >= rgb[i][0], np_im[:,:,1] >= rgb[i][1], np_im[:,:,2] >= rgb[i][2],
                                      np_im[:,:,0] <= rgb[i][3], np_im[:,:,1] <= rgb[i][4], np_im[:,:,2] <= rgb[i][5]))
        pixels = np.transpose(np.where(mask))
        for x, y in pixels:
            counter, summeX, summeY = counter + 1, summeX + x, summeY + y
            avg = summeX / counter
            # Wenn der Abstand zweier Pixel innerhalb 70 Pixel liegt gehört es noch zu dem aktuellen Punkt
            if x < avg - 70 or x > avg + 70:
                # Umrechnung der Koordinaten ins Polarkoordinatensystem
                dx = x0 - x
                dy = y0 - y
                abstand = math.sqrt(dx**2 + dy**2)
                winkel = math.acos(dx/abstand)
                dotsAvg.append((abstand, winkel))
                summeX = summeY = counter = 0

        if not counter == 0:
            # Umrechnung der Koordinaten ins Polarkoordinatensystem
            dx = x0 - x
            dy = y0 - y
            abstand = math.sqrt(dx**2 + dy**2)
            winkel = math.acos(dx/abstand)
            # Ergebnisse in DotsAvg schreiben
            dotsAvg.append((abstand, winkel))
            print(str(int(len(dotsAvg))) + " Punkt wurde für "  + str(rgb[i][0]) + " =< R >= " + str(rgb[i][1]) + " " + 
                str(rgb[i][2]) + " =< G >= " + str(rgb[i][3]) + " " +str(rgb[i][4]) + " =< B >= " + str(rgb[i][5]) + " gefunden")
            print("Valid coords - appended")
            # Ergebniss des durchlaufes in Gesamtergebnissliste hängen
            coords.append(dotsAvg)
            # Schreibt Koordinaten in CSV File
            with open('output.csv', 'a', newline='') as file:
                writer = csv.writer(file)
                for dot in dotsAvg:
                    writer.writerow(dot)
            # --> dann nächste Farbe   
    return coords

 
# Schreibt Koordinaten von 1 Bild in jeweilige csv Dateien für den jeweiligen Punkt
def WriteToCsvSingleCoord(coords):
     for i, lst in enumerate(coords):
                filename = f"Koordinaten_{i+1}.csv"
                with open(filename, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    for j in range(0, len(lst), 2):
                        csvwriter.writerow([lst[j], lst[j+1]])
                    print(f"written to {filename} successfully.")

# Schreib übergebenen String (input) in den übergebenen Pfad, falls Pfad nicht vorhanden wird dieser erstellt
def WriteToFile(input, filename):
    filename = os.getcwd() + '\\' + filename
    with open(filename, 'a') as file:
        print(f"File '{filename}' write to file.")
    outputFile = open(filename, "a")
    outputFile.write(str(input))
    outputFile.close()
 

# Bekommt ergebnissliste (egal ob normale Koordinaten (float) oder Winkel(dezimal))
# Wandelt ergebnisse in Binär um und schreibt LSB in übergebenen filepath
# returnt lsbs in Array
def LsbBits(results, file_path):
    DeleteFileContents(file_path)
    bits = []
    # Results hält ergebnisse aller Bilder
    # Result ist das Ergebniss eines Bild
    # Coords ist jeweils ein Koordinaten Tupel 
    # Coord is ein einziger Wert (Koordinate/Winkel oder Distanz)
    for result in results:
        for coords in result:
            for coord in coords:
                if isinstance(coord, tuple):
                    for value in coord:
                        if isinstance(value, (float, decimal.Decimal)):
                            binary_str = format(struct.unpack('!Q', struct.pack('!d', value))[0], '064b')
                            lsb = int(binary_str[-1])
                            print(f"Original number: {value}")
                            print(f"Binary string: {binary_str}")
                            print(f"LSB: {lsb}")
                            WriteToFile(lsb, file_path)
                            bits.append(lsb)
                        elif isinstance(value, (int)):
                            binary_str = format(value, '064b')
                            lsb = int(binary_str[-1])
                            print(f"Original number: {value}")
                            print(f"Binary string: {binary_str}")
                            print(f"LSB: {lsb}")
                            WriteToFile(lsb, file_path)
                            bits.append(lsb)
                elif isinstance(coord, (float, decimal.Decimal)):
                    binary_str = format(struct.unpack('!Q', struct.pack('!d', coord))[0], '064b')
                    lsb = int(binary_str[-1])
                    print(f"Original number: {coord}")
                    print(f"Binary string: {binary_str}")
                    print(f"LSB: {lsb}")
                    WriteToFile(lsb, file_path)
                    bits.append(lsb)
                elif isinstance(coord, (int)):
                    binary_str = format(coord, '064b')
                    lsb = int(binary_str[-1])
                    print(f"Original number: {coord}")
                    print(f"Binary string: {binary_str}")
                    print(f"LSB: {lsb}")
                    WriteToFile(lsb, file_path)
                    bits.append(lsb)
    return bits

# Hasht übergebene Result Liste immer mit dem nachgehenden Wert als Seed 
# Ergebnisse werden in  binarynumbers.txt geschrieben
def HashBits(results):
    DeleteFileContents("binarynumbers.txt")
    for result in results:
        for coords in result:
            gangweite = 0
            for coord in coords:
                prevcoord = coord
                # Gangweite ist der Abstand der jeweiligen Werte
                if gangweite == 1:
                    num = bytes(str(prevcoord), 'utf-8')
                    seed = struct.pack('f', coord)
 
                    hash_object = hashlib.blake2b(digest_size=8, salt=seed)
                    hash_object.update(str(num).encode())
                    hash_value = hash_object.digest()
 
                    hash_int = int.from_bytes(hash_value, byteorder='big')
                    hash_bits = bin(hash_int)[2:]
                    WriteToFile(hash_bits, "binarynumbers.txt")
                else: 
                    gangweite += 1

# Schreibt übergebene Gesamtergebnissliste mit [ [(x1,y1), (x2,y2), (x3, y3)] , [(z1,u1), (z2,u2), (z3,u3)] , ...]
# Liste hält jeweils ergebnisse für ein Bild, welches jeweils die Koordinaten der jeweiligen Farben umfasst 
# Kann werte unabhängig von Datentyp schreiben 
def WriteToCsv(results):
     for coords in results:
        for i, lst in enumerate(coords):
                    filename =  "Farbe" + str(i)  +".csv"
                    with open(filename, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        for j in range(0, len(lst), 2):
                            csvwriter.writerow([lst[j], lst[j+1]])
                        print(f"written to {filename} successfully.")

# Gibt ergebnissliste aus
def printResults(results):
    for result in results:
        print(" ")
        for coords in result:
            print(coords)

# Läuft durch alle Bilder (benannt "Picturename" + "idx") im angebenen Pfad
# Ruft Scan Methode auf speichter rückgabe Werte in all_results (jeweils 1 result pro Bild) 
def Analyse(file, pictureName, idx, endIdx):
    rgb = GetRgbValues()
    all_results = []
    dir = os.getcwd() + '\\TRNG-Pendel\\' + file + '\\'
    while(idx < endIdx):
        image = LoadImage(dir + pictureName + str(idx) + ".jpg")
        if image != 0:
            result = ScanDotsPolar(image, GetWidth(image), GetHeight(image), rgb, 870, 475)
            all_results.append(result)
        idx += 1
    return all_results
 

def Run():
    # Ordnerpfad, Bildbenennung (ohne Name leerer String), StartIdx Bilder, EndIdx Bilder
    results = Analyse("Folder" + "\\", "Picture", 1,   150)
    printResults(results)
    
    LsbBits(results)
    #WriteToCsv(results)
    shannonEntropy("binarynumbers.txt")
    verteilung("binarynumbers.txt")
    

Run()

