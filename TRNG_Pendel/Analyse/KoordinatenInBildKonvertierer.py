from PIL import Image


def generatePictureOutOfDictionary(dic):
    img = Image.new('RGB', (1200, 1200), (0,0,0))

    v = list(dic.values())
    maxValue = max(v)

    whiteCircle = []
    
    valuesList = dic.values()

    minValue = min(valuesList)
    maxValue = max(valuesList)
    for tupel in dic:
        frequency = ((dic[tupel] - minValue) / (maxValue - minValue)) * 0.8 + 0.2
        img.putpixel((tupel[0],tupel[1]), (int(frequency*255),int(frequency*255),int(frequency*255)))
        
            
        
    img.save('TRNG_Pendel/Analyse/Erwartungsraum.png')
    print("Bild gespeichert")
