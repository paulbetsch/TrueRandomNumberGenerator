from multiprocessing import Event

class ErrorEvent(Event):
    def __init__ (self):
        super().__init__()
        self.__description = ""
    
    def setErrorDescription(self, errorDescription):
        self.__description = errorDescription

    def getErrorDescription(self):
        return self.__description
