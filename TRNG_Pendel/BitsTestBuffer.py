import time
import os

MAX_LENGTH = 10000
buffer = "101010101010101010110101010110"

def loadBufferFromTxt():
    with open("TRNG_Pendel/Ressoruces/TestBitsBuffer.txt", 'r') as file:
        buffer = str(file.read())

def putBitsInTestBitsBuffer(bitsString):
    summeOfBits = len(buffer)+len(bitsString)
    if(summeOfBits > MAX_LENGTH):
        bitsToReduze = (summeOfBits-MAX_LENGTH)
        buffer = buffer[:MAX_LENGTH-bitsToReduze]
    buffer += bitsString

def saveBufferToTxt():
    with open("Ressources\\TestBitsBuffer.txt", 'w') as file:
        file.write(buffer)

print(os.path.dirname(__file__))
saveBufferToTxt()