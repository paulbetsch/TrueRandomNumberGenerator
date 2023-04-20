
import time
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
import binascii
import subprocess
import signal
import os
import time
import picamera
from PIL import Image, ImageEnhance



def cleanSetup():
    print("clean setup")
    DeleteFileContents("output.txt")
    DeleteFolderContents("PiPictures")

def TakePictures():
    #capture_process = subprocess.Popen(['python', 'PiCapture.py'])
    print("Swing Pendelum")
    #proc = subprocess.Popen(['python', 'PiCapture.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    #stdout, stderr = proc.communicate()
    with picamera.PiCamera() as camera:
        camera.resolution = (1920, 1080)
        camera.framerate = 30
        #camera.shutter_speed = 10000
        time.sleep(3)
        for i in range(100):
            print("Picture: " + str(i) )
            camera.capture("PiPictures/Image" + str(i) + ".jpg")
    camera.close()
    for i in range(100):
        image = Image.open('PiPictures/Image' + str(i) + '.jpg')

        gray_image = image.convert('L')

        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(1.5)

        enhancer = ImageEnhance.Brightness(enhanced_image)
        brightened_image = enhancer.enhance(50.5)

        #Kontrast
        enhancer = ImageEnhance.Contrast(gray_image)
        enhanced_image = enhancer.enhance(4.5)

        brightened_image.save('EnhancedPictures/enhanced_image' + str(i) + '.jpg')

# Close the camera

def DeleteFolderContents(filename):
    folder_path = os.getcwd() + '/' + filename 
    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')
    print(folder_path + " cleared")
    
        

def DeleteFileContents(filename):
    filename = os.getcwd() + '/' + filename
    if os.path.exists(filename):
        os.remove(filename)
        with open(filename, 'w') as file:
            file.write('')
    print(filename + " cleared")
  

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
    rgbBlack = [0, 0, 0, 55, 55, 55]
    rgbAll = [rgbBlack]
    return rgbAll

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


# Schreib übergebenen String (input) in den übergebenen Pfad, falls Pfad nicht vorhanden wird dieser erstellt
def WriteToFile(input, filename):
    filename = os.getcwd() + '/' + filename
    with open(filename, 'a') as file:
        print(f"File '{filename}' write to file.")
    outputFile = open(filename, "a")
    outputFile.write(str(input))
    outputFile.close()
 

# Bekommt ergebnissliste (egal ob normale Koordinaten (float) oder Winkel(dezimal))
# Wandelt ergebnisse in Binär um und schreibt LSB in übergebenen filepath
# returnt lsbs in Array
def LsbBits(results, file_path):
    bits = []
    for result in results:
        for coords in result:
            if isinstance(coords, tuple):
                for coord in coords:
                    if isinstance(coord, (float, decimal.Decimal)):
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
            elif isinstance(coords, (float, decimal.Decimal)):
                binary_str = format(struct.unpack('!Q', struct.pack('!d', coords))[0], '064b')
                lsb = int(binary_str[-1])
                print(f"Original number: {coords}")
                print(f"Binary string: {binary_str}")
                print(f"LSB: {lsb}")
                WriteToFile(lsb, file_path)
                bits.append(lsb)
            elif isinstance(coords, (int)):
                binary_str = format(coords, '064b')
                lsb = int(binary_str[-1])
                print(f"Original number: {coords}")
                print(f"Binary string: {binary_str}")
                print(f"LSB: {lsb}")
                WriteToFile(lsb, file_path)
                bits.append(lsb)
    return bits


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
    dir = os.getcwd() + file
    while(idx < endIdx):
        image = LoadImage(dir + pictureName + str(idx) + ".jpg")
        if image != 0:
            result = ScanDotsPolar(image, GetWidth(image), GetHeight(image), rgb, 1065, 444)
            all_results.append(result)
        idx += 1
    return all_results


def DeleteDoubles(results):
    prevcord = ["", ""]  
    new_results = []
    for result in results:
        for coord in result:
            if coord[0] == prevcord[0]: #or len(str(coord[0])) < 7 :
                print(str(coord) + " == " + str(prevcord) + " remove")
                result.remove(coord)  
            else:
                new_results.append(coord)
                print(str(coord) + " != " + str(prevcord) + " keep")
                prevcord = coord  
    return new_results
                   

def run():
    #cleanSetup()
    #TakePictures()
    results = Analyse("/PiPictures/","Image", 0, 100)
    results = DeleteDoubles(results)
    LsbBits(results, "output.txt")

run()

