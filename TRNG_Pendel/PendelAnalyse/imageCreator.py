from PIL import Image


def generatePictureOutOfDictionary(dic):
    img = Image.new('RGB', (1920, 1080), (255,0,0))

    v = list(dic.values())
    maxValue = max(v)

    for tupel in dic:
        frequency = dic[tupel] / maxValue
        img.putpixel((tupel[0],tupel[1]), (int(frequency*255),int(frequency*255),int(frequency*255)))
    
    img.save('c:/Users/Paul/Desktop/PendelErwartungswerte/image.png')
    print("saved")
