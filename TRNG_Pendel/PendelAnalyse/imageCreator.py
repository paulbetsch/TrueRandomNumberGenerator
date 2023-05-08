from PIL import Image


def generatePictureOutOfDictionary(dic):
    img = Image.new('RGB', (1920, 1080), (0,0,0))

    v = list(dic.values())
    maxValue = max(v)

    whiteCircle = []
    
    valuesList = dic.values()

    print(len(valuesList))
    minValue = min(valuesList)
    maxValue = max(valuesList)
    for tupel in dic:
        #frequency = dic[tupel] / maxValue 
        frequency = ((dic[tupel] - minValue) / (maxValue - minValue)) * 0.8 + 0.2
        img.putpixel((tupel[0],tupel[1]), (int(frequency*255),int(frequency*255),int(frequency*255)))
        
            
        
    img.save('image.png')
    print("saved")
