from PIL import Image


def generatePictureOutOfDictionary(dic):
    img = Image.new('RGB', (1920, 1080), (255,0,0))

    v = list(dic.values())
    maxValue = max(v)

    whiteCircle = []

    for tupel in dic:
        frequency = dic[tupel] / maxValue
        img.putpixel((tupel[0],tupel[1]), (int(frequency*255),int(frequency*255),int(frequency*255)))
        if(frequency >= 1):
            whiteCircle.append(tupel)
            img.putpixel((tupel[0],tupel[1]), (120,44,233))
            
        
    with open("circleValues.txt", 'w') as f:
        for i in whiteCircle:
            f.write(str(i))
    img.save('c:/Users/Paul/Desktop/PendelErwartungswerte/image.png')
    print("saved")
