import csv
import os

l = [[123, 12], [555,487], [56454, 4862]]

def writeData(liste):
    with open ("Data.txt", 'a', newline='') as filedata:
        writer = csv.writer(filedata, delimiter=';')
        writer.writerow(['Test56454', 'Test4862'])
        
        """ for i in range(len(liste)):
            stringrow = ""
            for o in range(len(liste[0])):
                stringrow += str(liste[i][o])
            print(stringrow)
            writer.writerow(str(stringrow)) """


def readData(filepath):
    with open (filepath, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',')
        for v in csv_reader:
            string = str(v)
            if("0" in v):
                print("Found!!")

#writeData(l)
print(os.getcwd())
print(os.listdir())
readData("KGELBNEW.csv")


