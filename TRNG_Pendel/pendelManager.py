from Lightbarrier.lightbarrier.py import *

# Wird von der REST-API geleitet

# Wird später aufgerufen um die Funktionalität der Lichtschranke, der Kamera und der Motorisierung des Pendels zu gewährleisten.
def checkFunctionality():
    if(testFunctionality()):
        print("Functionality Tests passed")
        return True
    else:
        print("Functionality Tests FAILED!")
        return False


# Hier soll der Motor gesteuert werden, und die Werte der Kamera und der Lichtschranke ausgewertet werden
def generateRandomBits():
    if(checkFunctionality()):
        # Wenn die Funtkion gewährleistet ist beginne die Generation
        print()
    else:
        print()

#Test
def checkBSITests():
    print()

