import tkinter as tk
import sys

sys.path.insert(0, '../TRNG_Pendel') # inserting path for imports

from KameraRaspberryPi import *
from Lightbarrier import *
from PendelAnalyse import *


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack() # packs all widgets into the main frame 
        self.CreateWidgets() 

    def ChangeText(self, textnew): 
    # updates status depending on which button was pushed
        self.statusB.config(text = textnew) 

    def CloseWindow(self): 
    # closes window - ends script
        root.destroy()

    def CreateWidgets(self):
    # creating and packing buttons
        self.startCameraB = tk.Button(self, text="Start Camera", command=self.StartCamera)
        self.startCameraB.pack(side="bottom")

        self.stopCameraB = tk.Button(self, text="Stop Camera", command=self.StopCamera)
        self.stopCameraB.pack(side="bottom")

        self.startLightB = tk.Button(self, text="Start Lightbarrier", command=self.StartLight)
        self.startLightB.pack(side="bottom")

        self.stopLightB = tk.Button(self, text="Stop Lightbarrier", command=self.StopLight)
        self.stopLightB.pack(side="bottom")

        self.startEngineB = tk.Button(self, text="Start Engine", command=self.StartEngine)
        self.startEngineB.pack(side="bottom")

        self.stopEngineB = tk.Button(self, text="Stop Engine", command=self.StopEngine)
        self.stopEngineB.pack(side="bottom")

        self.startAllB = tk.Button(self, text="Start All", command=self.StartAll)
        self.startAllB.pack(side="bottom")

        self.stopAllB = tk.Button(self, text="Stop All", command=self.StopAll)
        self.stopAllB.pack(side="bottom")

        self.closeB = tk.Button(self, text="Close Window", command=self.CloseWindow)
        self.closeB.pack(side="bottom")

        self.result_label = tk.Label(self, text="Bedienung leicht gemacht")
        self.result_label.pack(side="top")

        self.statusB = tk.Label(self, text="Status: null")
        self.statusB.pack(side="bottom")

    
    def StartCamera(self):
    # Objecttracking starts
       self.ChangeText("Status: Camera started")
       

    def StopCamera(self):
    # Objecttracking stops
        self.ChangeText("Status: Camera stopped")
        

    def StartLight(self):
    # Lightbarrier starts
       self.ChangeText("Status: Lightbarrier started")
       

    def StopLight(self):
    # Lightbarrier stops
        self.ChangeText("Status: Lightbarrier stopped")
        

    def StartEngine(self):
    # Engine Tool starts
        self.ChangeText("Status: Engine started")

    def StopEngine(self):
    # Engine Tool stops
        self.ChangeText("Status: Engine stopped")

    def StartAll(self):
    # All tools start
        self.ChangeText("Status: All tools started")

    def StopAll(self):
    # All tools stop
        self.ChangeText("Status: All tools stopped")


root = tk.Tk() # setting root
root.title("Tool Management") # naming the frame
root.geometry("500x300") # setting size
app = Application(master=root) # initializing application
app.mainloop() # starting application 