# import requests
import tkinter as tk


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def changeText(self, textnew): 
        self.statusB.config(text = textnew) 

    def create_widgets(self):
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

    
    def startCamera(self):
       # Objecttracking starts
       # KameraRaspberryPi.__init__
       self.changeText("Status: Camera started")
       

    def stopCamera(self):
        # Objecttracking stops
        self.changeText("Status: Camera stopped")
        

    def startLight(self):
        # Lightbarrier starts
       #  Lightbarrier.__init__
       self.changeText("Status: Lightbarrier started")
       

    def stopLight(self):
        # Lightbarrier stops
        self.changeText("Status: Lightbarrier stopped")
        

    def startEngine(self):
        # Engine Tool starts
        self.changeText("Status: Engine started")

    def stopEngine(self):
        # Engine Tool stops
        self.changeText("Status: Engine stopped")

    def startAll(self):
        # All tools start
        self.changeText("Status: All tools started")

    def stopAll(self):
        # All tools stop
        self.changeText("Status: All tools stopped")


  #  def generate(self):
   #     num_bits = self.num_bits_entry.get()
    #    quantity = self.quantity_entry.get()
#
       # Make a GET request to the API endpoint
  #      response = requests.get(f"http://localhost:5000/randomNum/getRandom?numBits={num_bits}&quantity={quantity}")
#
 #       if response.status_code == 200:
  #          # Update the result label with the generated hexadecimal numbers
   #         self.result_label.config(text=response.text)
    #    else:
     #       # Display an error message if the API request fails
      #      self.result_label.config(text="Error: " + response.text)


root = tk.Tk()
root.title("Tool Management")
root.geometry("500x300")
app = Application(master=root)
app.mainloop()