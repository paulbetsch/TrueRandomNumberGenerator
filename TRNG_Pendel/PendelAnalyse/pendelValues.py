import matplotlib.pyplot as plt
from matplotlib.patches import Circle
import math
from imageCreator import *

def berechnePunkteAufKreis(radius, mittelpunkt, anzahlPunkte):
    x0, y0 = mittelpunkt
    punkte = []
    for i in range(anzahlPunkte):
        theta = 2 * math.pi * i / anzahlPunkte
        y = y0 + (radius * math.sin(theta))
        x = x0 + (radius * math.cos(theta))
        punkte.append(((int(x)), (int(y))))
    return punkte


def berechnePendel(pendelnummer):
    mittelpunkte = [(960,540)]
    wertebereich = {}

    for anzahl in range(pendelnummer):
        print("Berechne Punkte für Pendel "+str(anzahl+1))
        neuePunkte = []
        anzahlMittelpunkte = len(mittelpunkte)
        progessCounter = 0
        for punkt in mittelpunkte:
            if(progessCounter % 1000 == 0):
                print(str(round((progessCounter / anzahlMittelpunkte * 100),2)) + "%")
            progessCounter += 1
            neuePunkte += berechnePunkteAufKreis(50, punkt, 1000)
            if(anzahl == pendelnummer-1):
                for tupel in neuePunkte:
                    if wertebereich.get(tupel) == None:
                        wertebereich[tupel] = 1
                    else:
                        wertebereich[tupel] = wertebereich[tupel] +1
                neuePunkte = []
        print("Berechnung Punkte für Pendel "+str(anzahl+1) + " fertig")
        mittelpunkte = neuePunkte
    return wertebereich



#print(berechnePendel(3))
print(generatePictureOutOfDictionary(berechnePendel(3)))

# def calculateFrequencies(mittelpunkte):
#     print("Calculating frequencies")
#     wertebereich = {}
#     for tupel in mittelpunkte:
#         if wertebereich.get(tupel) == None:
#             wertebereich[tupel] = 1
#         else:
#             wertebereich[tupel] = wertebereich[tupel] +1
#     return wertebereich

# def berechnePendel(pendelnummer):
#     # fig, ax = plt.subplots()
#     # ax.set_xlim(-200, 200)
#     # ax.set_ylim(-200, 200)

#     mittelpunkte = [(960,540)]

#     for anzahl in range(pendelnummer):
#         print("Berechne Punkte für Pendel "+str(pendelnummer+1))
#         neuePunkte = []
#         for punkt in mittelpunkte:
#             #print("Berechne neue Kreispunkte für Punkt"+str(punkt))
#             # if(anzahl == pendelnummer-1):
#             #     maleKreis(50, punkt, "0.7" , ax)
#             neuePunkte += berechnePunkteAufKreis(50, punkt, 100)
#         mittelpunkte = neuePunkte
#     return mittelpunkte

def maleKreis(radius, mittelpunkt, farbe, ax):
    circle = Circle(mittelpunkt, radius, fill=False, edgecolor=farbe)
    ax.add_patch(circle)

def malePendel():
    mittelpunkte = berechnePendel(1)
    wertebereich = {}
    for tupel in mittelpunkte:
        if wertebereich.get(tupel) == None:
            wertebereich[tupel] = 1
        else:
            wertebereich[tupel] = wertebereich[tupel] +1

    v = list(wertebereich.values())
    print(max(v))
    maxValue = max(v)

    maxi = len(wertebereich)
    counter = 0
    for tupel in wertebereich:
        if(counter % 10000 == 0):
            print(round(counter / maxi, 2))
        counter += 1
        plt.scatter(tupel[0], tupel[1], color='black', s=0.1 )

    plt.savefig("c:/Users/Paul/Desktop/test1.png", format="png")
    print("Done")   

    #plt.show()

# #malePendel()

# #malePendel(3)






