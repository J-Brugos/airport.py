from tkinter import *
from airport2 import *

airports = []

window = Tk()
window.geometry("800x600")
window.rowconfigure(0, weight=1)
window.rowconfigure(1, weight=1)
window.rowconfigure(2, weight=1)
window.rowconfigure(3, weight=1)
window.rowconfigure(4, weight=1)
window.rowconfigure(5, weight=1)
window.columnconfigure(0, weight=1)
window.columnconfigure(1, weight=1)
window.columnconfigure(2, weight=1)
window.columnconfigure(3, weight=1)

# TÍTULO
tituloLabel = Label(window, text = "Mi programa", font=("Courier", 20, "italic"))
tituloLabel.grid(row=0, column=0, columnspan=4, sticky=N+S+E+W)

# ENTRIES
fraseEntry = Entry(window)
fraseEntry.grid(row=1, column=0)

latEntry = Entry(window)
latEntry.grid(row=1, column=1)

lonEntry = Entry(window)
lonEntry.grid(row=1, column=2)

# BOTONES
Button(window, text="Load", command = LoadAirports).grid(row=2, column=0)
#Button(window, text="Add", command = AddAirport).grid(row=2, column=1)
#Button(window, text="Remove", command = RemoveAirport).grid(row=2, column=2)
#Button(window, text="Save", command = SaveClick).grid(row=2, column=3)

#Button(window, text="Plot", command= PlotAirports).grid(row=3, column=1)
#Button(window, text="Map", command= MapAirports).grid(row=3, column=2)

window.mainloop()