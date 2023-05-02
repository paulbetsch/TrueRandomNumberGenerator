# import requests
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
        self.create_widgets() 

    def ChangeText(self, textnew): #updates status depending on which button was pushed
        self.statusB.config(text = textnew) 

    def CreateWidgets(self):
    # creating and packing buttons
        self.startCameraB = tk.Button(self, text="Start Camera", command=self.startCamera)
        self.startCameraB.pack(side="bottom")

        self.stopCameraB = tk.Button(self, text="Stop Camera", command=self.stopCamera)
        self.stopCameraB.pack(side="bottom")

        self.startLightB = tk.Button(self, text="Start Lightbarrier", command=self.startLight)
        self.startLightB.pack(side="bottom")

        self.stopLightB = tk.Button(self, text="Stop Lightbarrier", command=self.stopLight)
        self.stopLightB.pack(side="bottom")

        self.startEngineB = tk.Button(self, text="Start Engine", command=self.startEngine)
        self.startEngineB.pack(side="bottom")

        self.stopEngineB = tk.Button(self, text="Stop Engine", command=self.stopEngine)
        self.stopEngineB.pack(side="bottom")

        self.startAllB = tk.Button(self, text="Start All", command=self.startAll)
        self.startAllB.pack(side="bottom")

        self.stopAllB = tk.Button(self, text="Stop All", command=self.stopAll)
        self.stopAllB.pack(side="bottom")

        self.result_label = tk.Label(self, text="Bedienung leicht gemacht")
        self.result_label.pack(side="top")

        self.statusB = tk.Label(self, text="Status: null")
        self.statusB.pack(side="bottom")

    
    def StartCamera(self):
       # Objecttracking starts
       self.changeText("Status: Camera started")
       

    def StopCamera(self):
        # Objecttracking stops
        self.changeText("Status: Camera stopped")
        

    def StartLight(self):
        # Lightbarrier starts
       #  Lightbarrier.__init__
       self.changeText("Status: Lightbarrier started")
       

    def StopLight(self):
        # Lightbarrier stops
        self.changeText("Status: Lightbarrier stopped")
        

    def StartEngine(self):
        # Engine Tool starts
        self.changeText("Status: Engine started")

    def StopEngine(self):
        # Engine Tool stops
        self.changeText("Status: Engine stopped")

    def StartAll(self):
        # All tools start
        self.changeText("Status: All tools started")

    def StopAll(self):
        # All tools stop
        self.changeText("Status: All tools stopped")


root = tk.Tk() # setting root
root.title("Tool Management") # naming the frame
root.geometry("500x300") # setting size
app = Application(master=root) # initializing application
app.mainloop() # starting application 