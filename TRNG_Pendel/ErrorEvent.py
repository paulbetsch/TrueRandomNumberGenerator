from multiprocessing import Event

class ErrorEvent():
    def __init__ (self):
        super().__init__()
        self.__event = Event()
        self.__description = ""
    
    def setEvent(self):
        self.__event.set()
    
    def getEvent(self):
        return self.__event
    
    def isEventSet(self):
        return self.__event.is_set()
    
    def setErrorDescription(self, errorDescription: str):
        self.__description = errorDescription

    def getErrorDescription(self):
        return self.__description
