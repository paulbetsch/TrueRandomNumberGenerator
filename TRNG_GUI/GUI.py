import tkinter as tk
import sys

sys.path.insert(0, '../TRNG_Pendel') # inserting path for imports

#import Lightbarrier
import KameraRaspberryPi.ObjectTracker as ot
import CodeSnippets.controls as co
#from ObjectTracker import *


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

        self.startLightOneB = tk.Button(self, text="Start One Lightbarrier", command=self.StartLightOne)
        self.startLightOneB.pack(side="bottom")

       # self.startLightTwoB = tk.Button(self, text="Start Both Lightbarriers", command=self.StartLightTwo)
       # self.startLightTwoB.pack(side="bottom")

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
       global CAMERA_RUNNING
       CAMERA_RUNNING = True
       if CAMERA_RUNNING == True:
           # ot.CapturePendelum()
           self.ChangeText("Status: Camera running")

    

    def StopCamera(self):
    # Objecttracking stops
        self.ChangeText("Status: Camera stopped")
        global CAMERA_RUNNING
        if CAMERA_RUNNING == False:
           self.ChangeText("Status: Camera is not running")
        elif CAMERA_RUNNING == True:
            CAMERA_RUNNING = False
            self.ChangeText("Status: Camera stopped")

    

    def StartLightOne(self):
    # One Lightbarrier starts
       self.ChangeText("Status: One Lightbarrier started")  
       global LIGHT_RUNNING
       LIGHT_RUNNING = True
       if LIGHT_RUNNING == True:
           # Lightbarrier.runOneLightbarrierParallel()  
           self.ChangeText("Status: Lightbarrier running")  

  #  def StartLightTwo(self):
    # Both Lightbarriers starts
   #    self.ChangeText("Status: Two Lightbarriers started")  
    #   Lightbarrier.runTwoLightbarriersParallel()

    def StopLight(self):
    # Lightbarrier stops
        self.ChangeText("Status: Lightbarrier stopped")  
        global LIGHT_RUNNING
        if LIGHT_RUNNING == False:
           self.ChangeText("Status: Lightbarrier is not running")
        elif LIGHT_RUNNING == True:
            LIGHT_RUNNING = False
            self.ChangeText("Status: Lightbarrier stopped")    

    def StartEngine(self):
    # Engine Tool starts
        self.ChangeText("Status: Engine started")  
        global ENGINE_RUNNING
        ENGINE_RUNNING = True
        if ENGINE_RUNNING == True:
           co.run()
           self.ChangeText("Status: Engine running")
           

    def StopEngine(self):
    # Engine Tool stops
        self.ChangeText("Status: Engine stopped")
        global ENGINE_RUNNING
        if ENGINE_RUNNING == False:
           self.ChangeText("Status: Engine is not running")
        elif ENGINE_RUNNING == True:
            ENGINE_RUNNING = False
            self.ChangeText("Status: Engine stopped") 

    def StartAll(self):
    # All tools start
        self.StartCamera
        self.StartEngine
        self.StartLightOne
        self.ChangeText("Status: All tools started")

    def StopAll(self):
    # All tools stop
        self.StopCamera
        self.StopEngine
        self.StopLight
        self.ChangeText("Status: All tools stopped")


root = tk.Tk() # setting root
root.title("Tool Management") # naming the frame
root.geometry("500x300") # setting size
app = Application(master=root) # initializing application
app.mainloop() # starting application 