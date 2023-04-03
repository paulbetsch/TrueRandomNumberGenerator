import cv2 as cv
import os
from PIL import Image
import hashlib

filename='C:\\Python311\\Tests\\Output\\rawNumbers.txt'

if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")

allList = []

### open the default camera (usually the built-in webcam)
##cap = cv.VideoCapture(1, cv.CAP_DSHOW)
### check if camera opened successfully
##if not cap.isOpened():
##    print("Error opening video capture.")
##
### read a single frame from the camera
##
##
### name = 'a'
##count = 0
### if frame is read correctly, show it
##while(True):
##      ret, frame = cap.read()
##      # cv2.imshow("Webcam", frame)
##      # cv2.waitKey(0)
##      cv.imwrite('C:\\Python311\\Tests\\Pictures\\' + str(count) + '.jpg', frame) #save image
##      # name = name + 'a'
##      count = count+1
##      if(count > 100):
##         break
##   
### else:
##   # print("Error reading frame from video capture.")
##
### release the camera and close the window
##cap.release()
##cv.destroyAllWindows()
##


#Read the Folder
###
#########################################################################
from PIL import Image
import hashlib

def sha512Hash(data):
    hashValue = hashlib.sha512(str(data).encode('utf-8')).hexdigest()
    res = bin(int('1'+hashValue, 16))[3:]
    return res
    
def loadImage(path):
    im = Image.open(path)
    # print("Das Bild wurde geladen" + path)
    return im
    
def scanResolution(image):
    # print("Folgende Auflösung wurde erkannt: Breite="+str(image.size[0])+" Höhe="+str(image.size[1]))
    return image.size

def getWidth(image):
    return image.size[0]

def getHeight(image):
    return image.size[1]
    
def scanBlackDots(im, width, height):
    counter = summeX = summeY = 0
    dotsAvg = []
    rgb_im = im.convert("RGB")

    # print("Beginning to search for Black Dots")

    for x in range(width):
  
        for y in range(height):
            r, g, b = rgb_im.getpixel((x, y))
            
            if((r >=0 and g >= 0 and b >= 120)and(r <= 55 and g <= 200 and b <= 255) ):
                # print("Schwarzer Pixel an X: "+str(x)+" und Y: "+str(y))
                counter, summeX, summeY = counter+1, summeX+x, summeY+y
                avg = summeX / counter
               
                if x < avg - 100 or x > avg + 100:
                       dotsAvg.append((summeX/counter))
                       dotsAvg.append((summeY/counter))
                       summeX = summeY = counter = 0

    if not counter == 0:         
        dotsAvg.append((summeX/counter))
        dotsAvg.append((summeY/counter))        
        # print(str(int(len(dotsAvg)/2))+" Schwarze Punkte wurden gefunden")
    
    return dotsAvg
    
def printResults(dotsAvg):
    counter, punkt = 0, 1
    counter1 = 0
          
    for z in dotsAvg:
        if(counter % 2 == 0):
            # print("Punkt "+str(punkt)+" X-Kord: "+str(int(z)))
            allList.append(int(z))                      
        else:                
            # print("Punkt "+str(punkt)+" Y-Kord: "+str(int(z)))
            allList.append(int(z))
            punkt += 1
        counter += 1
    string = ""
   


    

def comparePictures(pic1, pic2):
    pic1 = loadImage(pic1)
    pic2 = loadImage(pic2)
    widthPic1 = getWidth(pic1)
    heightPic1 = getHeight(pic1)
    widthPic2 = getWidth(pic2)
    heightPic2 = getHeight(pic2)
    
    if(widthPic1 == widthPic2 and heightPic1 == heightPic2):
        print("Picture have the same resolution!")
    dotsPic1 = scanBlackDots(pic1, widthPic1, heightPic1)
    dotsPic2 = scanBlackDots(pic2, widthPic2, heightPic2)
    if(len(dotsPic1) != len(dotsPic2)):
        return False
        for i in range(len(dotsPic1)):
            if(dotsPic1[i] <= 15 + dotsPic2([i]) and dotsPic1[i] >= 15 - dotsPic2([i])):
                print("Es die Bilder unterscheiden")
            return False
    return True



## import required module         
## assign directory
directory = 'C:\\Python311\\Tests\\Pictures\\'

## iterate over files in
## that directory
x=0

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)
    
## checking if it is a file

    if os.path.isfile(f):

    
        im = loadImage('C:\\Python311\\Tests\\Pictures\\'+str(x)+".jpg")
        x=x+1
        scanResolution(im)
        result = scanBlackDots(im, getWidth(im), getHeight(im))
        printResults(result)

def deleteDoubles(allList):


# Initialisiere eine leere Liste, um die Ergebnisse zu speichern
    pairs = []

# Iteriere über die Zahlenliste in Schritten von 2, da jedes Paar aus zwei Zahlen besteht
    for i in range(0, len(allList), 2):
        pair = [allList[i], allList[i+1]]
    # Überprüfe, ob das aktuelle Paar bereits in der Liste `pairs` vorhanden ist
        if pair not in pairs:
            pairs.append(pair)

# Gib die Liste der einzigartigen Zweierpaare aus
    print(pairs)

    return pairs


coordinates = deleteDoubles(allList)

def writeOutput(coordinates):
    output = []
    for c in coordinates:
        output.append(sha512Hash(c))     
        string = str(output)
        string=string.replace(" ",'')
        string=string.replace(",",'')
        string=string.replace("'",'')
        string=string.replace("]",'')
        string=string.replace("[",'')






        print(string)
    with open("C:\Git\TrueRandomNumberGenerator\Output\\rawNumbers.txt", "w") as f:
        f.write(string)
        os.close    
      
    return

writeOutput(coordinates)