from PIL import Image
import hashlib
import os.path
import cv2 as cv

current_dir = os.getcwd()
pictures_folder_path = os.path.join(current_dir, "Pictures")


# Löscht inhalte der rawnumbers.txt, für neuen Output

def create_output():
    filename = os.getcwd() + '\\rawnumbers.txt'

    if os.path.exists(filename):
        os.remove(filename)
        print(f"File '{filename}' has been deleted.")

    with open(filename, 'w') as file:
        print(f"File '{filename}' has been created.")

# Macht bilder und schreibt sie in den Pictures Ordner, wird nur bei Live auswertung benötigt

def take_pictures():
    cap = cv.VideoCapture(1, cv.CAP_DSHOW)

    # check if camera opened successfully
    if not cap.isOpened():
        print("Error opening video capture.")

    # read a single frame from the camera

    # name = 'a'
    count = 0
    # if frame is read correctly, show it
    while True:
        ret, frame = cap.read()
        # cv2.imshow("Webcam", frame)
        # cv2.waitKey(0)
        cv.imwrite(os.getcwd() + '\\Pictures\\' + str(count) + '.png', frame)  # save image
        # name = name + 'a'
        count = count + 1
        if count > 100:
            break


    # release the camera and close the window
    cap.release()
    cv.destroyAllWindows()


# Löscht alte Bilder aus dem Pictures Ordner, für Live analyse benötigt

def delete_contents():
    for filename in os.listdir(pictures_folder_path):
        file_path = os.path.join(pictures_folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
        print("Picture deleted")


# Erstellt Pictures ordner falls nicht vorhanden

def folder():
    if os.path.exists(pictures_folder_path) and os.path.isdir(pictures_folder_path):
        print("Folder found: " + pictures_folder_path)
    else:
        os.mkdir('Pictures')
        os.listdir('Pictures')


def sha512Hash(data):
    hashValue = hashlib.sha512(str(data).encode('utf-8')).hexdigest()
    res = bin(int('1' + hashValue, 16))[3:]
    return res


def loadImage(path):
    im = Image.open(path)
    print(str(path) + " picture has been loaded.")
    return im


def scanResolution(image):
    print("Dected resolution: Width=" + str(image.size[0]) + " Height=" + str(image.size[1]))
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
            if (r >= 0 and g >= 0 and b >= 120) and (r <= 55 and g <= 200 and b <= 255):
                #print("Blau Pixel an X: " + str(x) + " und Y: " + str(y))
                counter, summeX, summeY = counter + 1, summeX + x, summeY + y
                avg = summeX / counter

                if x < avg - 30 or x > avg + 30:
                    dotsAvg.append((summeX / counter))
                    dotsAvg.append((summeY / counter))
                    summeX = summeY = counter = 0

    if not counter == 0:
        dotsAvg.append((summeX / counter))
        dotsAvg.append((summeY / counter))
        print(str(int(len(dotsAvg) / 2)) + " Schwarze Punkte wurden gefunden")

    return dotsAvg


def anlayzeMovement(pic1, pic2):
    pic1 = loadImage(pic1)
    pic2 = loadImage(pic2)

    widthPic1 = getWidth(pic1)
    heightPic1 = getHeight(pic1)
    widthPic2 = getWidth(pic2)
    heightPic2 = getHeight(pic2)

    ##In Case of a camera error, in the normal state of the camer
    ##it will always stay the same resolution!
    if (widthPic1 != widthPic2 and heightPic1 != heightPic2):
        printErrorMessage("Stopped Process", "Camera Failure", "The resolution of the processed picture are different!",
                          ("Picture 1: " + str(widthPic1) + "x" + str(heightPic1)),
                          ("Picture 2: " + str(widthPic2) + "x" + str(heightPic2)))
        return False

    dotsPic1 = scanBlackDots(pic1, widthPic1, heightPic1)
    dotsPic2 = scanBlackDots(pic2, widthPic2, heightPic2)

    ##If the programm does not find the same Amount of black Dots
    ##there has to be movement in the pictures.
    if (len(dotsPic1) != len(dotsPic2)):
        return True

    ##Analyze the Coordinates of the black dots if the dots cords
    ##differentiate over more than 15 Pixels the programm we accept
    ##it as Movement.
    for i in range(len(dotsPic1)):
        if not ((dotsPic2[i] + 15) >= dotsPic1[i] >= (dotsPic2[i] - 15)):
            print("Die Bilder unterscheiden sich gut genug. Breite: " + str(dotsPic1[i]) + " Höhe: " + str(dotsPic2[i]))
            return True

    return False


def printErrorMessage(*string):
    header = "#"
    header = header * (len(max(string, key=len)) + 4)
    print(header)
    for s in string:
        print("# " + str(s))
    print(header)





# Bilder richtig auf name anpassen
def analyse():
    x = 100
    help = []
    directory = os.getcwd() + '\\Pictures\\'
    for filename in os.listdir(directory):
        if x > 650:
            break
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            image = loadImage(directory + "Test" + str(x) + ".png")
            x = x + 1
            result = scanBlackDots(image, getWidth(image), getHeight(image))
            bool = True
            for i in help:
                if i == result:
                    bool = False
                    break
            if bool == True:
                help.append(result)
    for i in help:
        print_results(i)


    clearOutput(help)


def clearOutput(help):
    for i in range(len(help)):
        print(help[i])






def print_results(dotsAvg):
    counter, punkt = 0, 1
    for z in dotsAvg:
        if (counter % 2 == 0):
            print("Punkt " + str(punkt) + " X-Kord: " + str(int(z)))
        else:
            print("Punkt " + str(punkt) + " Y-Kord: " + str(int(z)))
            punkt += 1
        counter += 1
    string = ""
    for z in dotsAvg:
        string += sha512Hash(z)
    print(string)

    filename = os.getcwd() + '\\rawNumbers.txt'

    outputFile = open(os.getcwd() + '\\rawNumbers.txt', "a")
    outputFile.write(string)
    outputFile.close()


def run():
    folder()
    create_output()
    # delete_contents()
    analyse()


run()
