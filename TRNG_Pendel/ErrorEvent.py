from multiprocessing import Event, Value

class ErrorEvent():
    def __init__ (self, array):
        super().__init__()
        self.__event = Event()
        self.__description = array
    
    def setEvent(self):
        self.__event.set()
    
    def getEvent(self):
        return self.__event
    
    def isEventSet(self):
        return self.__event.is_set()
    
    def setErrorDescription(self, errorDescription):
        i = 0
        for c in errorDescription:
            self.__description[i] = ord(c)
            i += 1
        self.__description[i] = 0

    def getErrorDescription(self):
        result = ""
        for i in range(0, 255):
            if(ord(self.__description[i]) == 0):
                break
            result += chr(ord(self.__description[i]))
        
        return result
