from PIL import Image
import hashlib

def sha512Hash(data):
    hashValue = hashlib.sha512(str(data).encode('utf-8')).hexdigest()
    
    ##Converts the hex digest to a raw binary String and guarantees that
    ##preciding zeros are not missing
    res = bin(int('1'+hashValue, 16))[3:]
    return res
    
def loadImage(path):
    im = Image.open(path)
    print(str(path)+" picture has been loaded.")
    return im
    
def scanResolution(image):
    print("Dected resolution: Width="+str(image.size[0])+" Height="+str(image.size[1]))
    return image.size

def getWidth(image):
    return image.size[0]

def getHeight(image):
    return image.size[1]
    
def scanBlackDots(im, width, height):
    counter = summeX = summeY = 0
    dotsAvg = []
    rgb_im = im.convert("RGB")

    print("Beginning to search for Black Dots")

    for x in range(width):
        for y in range(height):
            r, g, b = rgb_im.getpixel((x, y))
            ##print("Pixelkoords: : %3s %3s Rot: %3s Grün: %3s Blau: %3s" % (x,y,r,g,b))
            
            ##If-Statement should check whether the current pixel has the desired color
            ##For black it is RGB(0,0,0) and for a color of blue you would you a range of
            ##colors like RGB(0-90,0-220,80-255)
            if(r <= 80 and g <= 200 and b <= 255):
                counter, summeX, summeY = counter+1, summeX+x, summeY+y
                avg = summeX / counter
                ##Black Pixel which are 50 Pixels away from the currente middle of the current
                ##black dot will count as a new black Dot.
                ##Alternative (maybe even better): Check for a minimal amount of black pixels
                ##e.g. 100 Pixel (Concentration)
                if x < avg - 50 or x > avg + 50:
                    dotsAvg.append((summeX/counter))
                    dotsAvg.append((summeY/counter))
                    summeX = summeY = counter = 0
    if(counter != 0):
        dotsAvg.append((summeX/counter))
        dotsAvg.append((summeY/counter))
    print(str(int(len(dotsAvg)/2))+" black dots were found")
    return dotsAvg
    
def printResults(dotsAvg):
    counter, punkt = 0, 1
    for z in dotsAvg:
        if(counter % 2 == 0):
            print("Dot "+str(punkt)+" X-Kord: "+str(int(z)))
        else:
            print("Dot "+str(punkt)+" Y-Kord: "+str(int(z)))
            punkt += 1
        counter += 1
    string = ""
    for z in dotsAvg:
        string += sha512Hash(z)
    print(string)

def anlayzeMovement(pic1, pic2):
    pic1 = loadImage(pic1)
    pic2 = loadImage(pic2)
  
    widthPic1 = getWidth(pic1)
    heightPic1 = getHeight(pic1)
    widthPic2 = getWidth(pic2)
    heightPic2 = getHeight(pic2)

    ##In Case of a camera error, in the normal state of the camer
    ##it will always stay the same resolution!
    if(widthPic1 != widthPic2 and heightPic1 != heightPic2):
        printErrorMessage("Stopped Process", "Camera Failure", "The resolution of the processed picture are different!", ("Picture 1: "+str(widthPic1)+"x"+str(heightPic1)), ("Picture 2: "+str(widthPic2)+"x"+str(heightPic2)))
        return False
    
    dotsPic1 = scanBlackDots(pic1, widthPic1, heightPic1)
    dotsPic2 = scanBlackDots(pic2, widthPic2, heightPic2)

    ##If the programm does not find the same Amount of black Dots
    ##there has to be movement in the pictures.
    if(len(dotsPic1) != len(dotsPic2)):
        return True

    ##Analyze the Coordinates of the black dots if the dots cords
    ##differentiate over more than 15 Pixels the programm we accept
    ##it as Movement.
    for i in range(len(dotsPic1)):
        if(not(dotsPic1[i] <= (dotsPic2[i] + 15) and dotsPic1[i] >= (dotsPic2[i] - 15))):
            print("Die Bilder unterscheiden sich gut genug. Breite: "+str(dotsPic1[i])+" Höhe: "+str(dotsPic2[i]))
            return True

    return False
    
def printErrorMessage(*string):
    header = "#"
    header = header * (len(max(string, key=len)) + 4)
    print(header)
    for s in string:
        print("# "+str(s))
    print(header)
    
im = loadImage("27.jpg")
scanResolution(im)
result = scanBlackDots(im, getWidth(im), getHeight(im))
printResults(result)

##print(anlayzeMovement("test9.png","test10.png"))







        






