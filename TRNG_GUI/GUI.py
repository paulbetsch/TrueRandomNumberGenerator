import tkinter as tk
import sys
import os
import threading


trng_pendel_path = os.path.abspath("../TRNG_Pendel")
sys.path.append(trng_pendel_path)

from KameraRaspberryPi import ObjectTracker1 as ot
from Engine import motor1 as mt


class cameraThread(threading.Thread): 
    # Thread for Camera Method
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run(self):
        # running the Script ObjectTracker.py
        ot.RunScript()
        
class engineThread(threading.Thread):
    # Thread for engine Method
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    
    def run(self):
        # running the Script motor.py
        mt.RunScript()
       #  pm.RunScript()


class Application(tk.Frame):
    # class for the Application Frame
    global ENGINE_RUNNING 
    global CAMERA_RUNNING
    CAMERA_RUNNING = False
    ENGINE_RUNNING = False
    # setting global variables to false
    
    def __init__(self, master):
        # initializing self
        super().__init__(master)
        self.master = master
        self.pack() # packs all widgets into the main frame 
        self.CreateWidgets() 

    def ChangeText(self, textnew): 
    # updates status depending on which button was clicked
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

        self.startEngineB = tk.Button(self, text="Start Engine", command=self.StartEngine)
        self.startEngineB.pack(side="bottom")

        self.stopEngineB = tk.Button(self, text="Stop Engine", command=self.StopEngine)
        self.stopEngineB.pack(side="bottom")

        self.closeB = tk.Button(self, text="Close Window", command=self.CloseWindow)
        self.closeB.pack(side="bottom")

        self.result_label = tk.Label(self, text="Bedienung leicht gemacht")
        self.result_label.pack(side="top")

        self.statusB = tk.Label(self, text="Status: null")
        self.statusB.pack(side="top")

    
    def StartCamera(self):
    # Objecttracking and Engine starts
       self.ChangeText("Status: Camera started")
       global CAMERA_RUNNING
       if ENGINE_RUNNING == False:
            CAMERA_RUNNING = True
            if CAMERA_RUNNING == True:
                thread1 = cameraThread(1, "Camera")
                thread1.start()
                self.ChangeText("Status: Camera running - press 'b' to pause")
       elif ENGINE_RUNNING == True:
           self.ChangeText("Engine is running - can't start Camera")
    

    def StopCamera(self):
    # Objecttracking and Engine stops
        self.ChangeText("Status: Camera stopped")
        global CAMERA_RUNNING
        if CAMERA_RUNNING == False:
           self.ChangeText("Status: Camera is not running")
        elif CAMERA_RUNNING == True:
           ot.StopScript()
           print("KAMERA STOP")
           CAMERA_RUNNING = False
           self.ChangeText("Status: Camera stopped")
 

    def StartEngine(self):
    # Engine Tool starts
     global ENGINE_RUNNING
     if CAMERA_RUNNING == False:
        ENGINE_RUNNING = True
        if ENGINE_RUNNING == True:
            thread2 = engineThread(2, "Engine")
            thread2.start()
            self.ChangeText("Status: Engine is running")   
        self.ChangeText("Status: Engine started")
     elif CAMERA_RUNNING == True:
        self.ChangeText("Camera is running - can't start Engine")

    def StopEngine(self):
    # Engine Tool stops
        self.ChangeText("Status: Engine stopped")
        global ENGINE_RUNNING
        if ENGINE_RUNNING == False:
           self.ChangeText("Status: Engine is not running")
        elif ENGINE_RUNNING == True:
            mt.StopScript()
            ENGINE_RUNNING = False
            self.ChangeText("Status: Engine stopped") 

root = tk.Tk() # setting root
root.title("Tool Management") # naming the frame
root.geometry("600x400") # setting size
app = Application(master=root) # initializing application
app.mainloop() # starting application 
