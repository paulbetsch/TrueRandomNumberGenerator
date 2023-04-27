import requests
import tkinter as tk

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.num_bits_label = tk.Label(self, text="Number of bits:")
        self.num_bits_label.pack(side="left")

        self.num_bits_entry = tk.Entry(self)
        self.num_bits_entry.pack(side="left")

        self.quantity_label = tk.Label(self, text="Quantity:")
        self.quantity_label.pack(side="left")

        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.pack(side="left")

        self.submit_button = tk.Button(self, text="Generate", command=self.generate)
        self.submit_button.pack(side="left")

        self.result_label = tk.Label(self, text="")
        self.result_label.pack(side="left")

    def generate(self):
        num_bits = self.num_bits_entry.get()
        quantity = self.quantity_entry.get()

        # Make a GET request to the API endpoint
        response = requests.get(f"http://localhost:5000/randomNum/getRandom?numBits={num_bits}&quantity={quantity}")

        if response.status_code == 200:
            # Update the result label with the generated hexadecimal numbers
            self.result_label.config(text=response.text)
        else:
            # Display an error message if the API request fails
            self.result_label.config(text="Error: " + response.text)

root = tk.Tk()
root.title("TRNG")
app = Application(master=root)
app.mainloop()