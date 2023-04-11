from PIL import Image
import hashlib
import os.path
import cv2 as cv
import math
import struct
import hashlib
import numpy as np
import csv
 
# Läd das Bild des übergebenen Pfades und gibt es zurück
def DeleteFileContents(filename):
    filename = os.getcwd() + '\\' + filename
    if os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write('')
            print(filename + " cleared")
    else:
        print(filename + " not found")
 
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
 
#Returns Array with RGB values for Pendelum points
 
def GetRgbValues():
    #rgbBlue = [0, 55, 90, 66, 200, 110]
    #rgbRed = [80, 0, 0, 110, 10, 15]
    #rgbAll = [rgbBlue, rgbRed]
 
    rgbGreen = [40, 110, 95, 65, 125, 100]
    rgbYellow = [190, 167, 65, 220, 185, 100]
    rgbBlue = [45, 110, 135, 70, 130 ,160]
    rgbAll = [rgbBlue, rgbYellow, rgbGreen]
 
    return rgbAll
 
# Sucht nach den übergebenen RGB werten in dem übergebenen Bild und gibt ein Array mit den Koordinaten
# der jeweilig gefunden Punkte für die RGB werte zurück
 
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
 
        # Gefundener Punkt (dotsAvg) x,y anhängen --> dann nächste Farbe      
    return coords
 
# Vergleicht zwei Bilder auf ausreichende Pendel bewegung
 
def Analyse(file, pictureName, idx, endIdx):
    rgb = GetRgbValues()
    all_results = []
    dir = os.getcwd() + '\\TRNG-Pendel\\' + file + '\\'
    while(idx < endIdx):
        image = LoadImage(dir + pictureName + str(idx) + ".jpg")
        if image != 0:
            result = ScanDots(image, GetWidth(image), GetHeight(image), rgb)
            all_results.append(result)
            WriteToCsv(result)
        idx += 1
    return all_results
 
# Schreibt Koordinaten für 1 Bild in jeweilige csv Dateien für die jeweilige Farbe
 
def WriteToCsv(coords):
     for i, lst in enumerate(coords):
                filename = f"Koordinaten_{i+1}.csv"
                with open(filename, 'a', newline='') as csvfile:
                    csvwriter = csv.writer(csvfile)
                    for j in range(0, len(lst), 2):
                        csvwriter.writerow([lst[j], lst[j+1]])
                    print(f"written to {filename} successfully.")
 
def WriteToFile(input, filename):
 
    filename = os.getcwd() + '\\' + filename
 
    with open(filename, 'a') as file:
        print(f"File '{filename}' write to file.")
    outputFile = open(filename, "a")
    outputFile.write(str(input))
    outputFile.close()
 
# Methode um Koordinaten sauber auszugeben
def FloatToBinary(number):
    packed = struct.pack('f', number)
    number = ''.join(format(b, '08b')for b in packed)
    return number
 
def LsbBits(results):
    DeleteFileContents("binarynumbers")
    bits = []
    for result in results:
        for coords in result:
            for coord in coords:
                binary_str = format(struct.unpack('!Q', struct.pack('!d', coord))[0], '064b')
                lsb = int(binary_str[-1])
                print(f"Original float: {coord}")
                print(f"Binary string: {binary_str}")
                print(f"LSB: {lsb}")
                WriteToFile(lsb, "binarynumbers")
                bits.append(lsb)
    return bits
 
def xor_binary_files(file1, file2, output_file):
    with open(file1, 'rb') as f1, open(file2, 'rb') as f2, open(output_file, 'wb') as out:
        byte1 = f1.read(1)
        byte2 = f2.read(1)
        while byte1 and byte2:
            out.write(bytes([byte1[0] ^ byte2[0]]))
            byte1 = f1.read(1)
            byte2 = f2.read(1)
 
def HashBits(results):
    DeleteFileContents("binarynumbers")
    gangweite = 0
    for result in results:
        for coords in result:
            for coord in coords:
                prevcoord = coord
                if gangweite == 10:
                    num = bytes(str(coord), 'utf-8')
                    seed = struct.pack('f', prevcoord)
 
                    hash_object = hashlib.blake2b(digest_size=8, salt=seed)
                    hash_object.update(str(num).encode())
                    hash_value = hash_object.digest()
 
                    hash_int = int.from_bytes(hash_value, byteorder='big')
                    hash_bits = bin(hash_int)[2:]
                    WriteToFile(hash_bits, "binarynumbers")
                else: 
                    gangweite += 1
                
def WriteToCsv(results):
     for coords in results:
        for i, lst in enumerate(coords):
                    filename = f"Koordinaten_{i+1}.csv"
                    with open(filename, 'a', newline='') as csvfile:
                        csvwriter = csv.writer(csvfile)
                        for j in range(0, len(lst), 2):
                            csvwriter.writerow([lst[j], lst[j+1]])
                        print(f"written to {filename} successfully.")

def Sha512Hash(data):
    hashValue = hashlib.sha512(str(data).encode('utf-8')).hexdigest()
    res = bin(int('1' + hashValue, 16))[3:]
    WriteToFile(res, "binarynumbers")
    return res
 
def Run():
    results = Analyse("TriPendelGelb", "", 1, 150)
    HashBits(results)
Run()
