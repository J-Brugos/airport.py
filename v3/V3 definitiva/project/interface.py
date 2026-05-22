# Importamos Tkinter para construir la ventana y sus controles.
from tkinter import *
from tkinter import filedialog, messagebox

# Importamos las funciones de los otros modulos del proyecto.
from airport import (
    AddAirport,
    Airport,
    LoadAirports,
    MapAirports,
    PlotAirports,
    RemoveAirport,
    SaveSchengenAirports,
    SetSchengen,
    converttodegrees
)
from aircraft import LoadArrivals, SaveFlights, PlotArrivals, PlotAirlines, MapFlights, PlotArrivalsSchengen

from LEBL import LoadAirportStructure, GateOccupancy, PlotAirportOccupancy, AssignGate, ResetGates


# Listas y objetos globales que guardan los datos cargados desde la interfaz.
airports = []
aircrafts = []
bcn_airport = None


# Convierte coordenadas escritas como numero decimal o como formato N/S/E/W.
def parse_coordinate(value):
    value = value.strip().upper()

    try:
        return float(value)
    except ValueError:
        return converttodegrees(value)


# Recalcula el valor Schengen de todos los aeropuertos recibidos.
def update_schengen_values(loaded_airports):
    i = 0

    while i < len(loaded_airports):
        SetSchengen(loaded_airports[i])
        i += 1


# Lee archivos con cabeceras o coordenadas decimales cuando LoadAirports no sirve.
def read_flexible_airport_file(filename):
    loaded_airports = []

    with open(filename, "r") as f:
        lines = f.readlines()
        line_index = 0

        # Recorremos las lineas con while para procesar el archivo paso a paso.
        while line_index < len(lines):
            line_number = line_index + 1
            line = lines[line_index]
            data = line.strip().split()

            if not data:
                line_index += 1
                continue

            if len(data) < 3 or data[0].upper() in ("ICAO", "CODE", "AIRCRAFT"):
                line_index += 1
                continue

            try:
                airport = Airport(data[0].upper(), parse_coordinate(data[1]), parse_coordinate(data[2]), False)
            except ValueError as exc:
                raise ValueError(f"Invalid airport coordinates on line {line_number}: {line.strip()}") from exc

            loaded_airports.append(airport)
            line_index += 1

    return loaded_airports


# Abre un selector de archivo y carga la lista de aeropuertos en memoria.
def load_airports_file():
    global airports

    filename = filedialog.askopenfilename(
        title="Select airports file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if not filename:
        return

    try:
        try:
            # Usamos primero la funcion del modulo airport.py.
            airports = LoadAirports(filename)
        except (ValueError, IndexError):
            # Si el archivo tiene cabecera o coordenadas decimales, usamos el lector flexible.
            airports = read_flexible_airport_file(filename)
    except ValueError as exc:
        messagebox.showerror("Error", str(exc))
        return

    update_schengen_values(airports)

    textBox.delete(1.0, END)
    with open(filename, "r") as f:
        textBox.insert(END, f.read())

    refresh_list()
    update_info()
    messagebox.showinfo("OK", "Airports loaded")


# Guarda en un archivo solo los aeropuertos marcados como Schengen.
def save_schengen():
    if not airports:
        messagebox.showerror("Error", "No airports loaded")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".txt")

    if not filename:
        return

    result = SaveSchengenAirports(airports, filename)

    if result == -1:
        messagebox.showerror("Error", "No Schengen airports")
    else:
        messagebox.showinfo("OK", "Schengen airports saved")


# Anade manualmente un aeropuerto usando el texto escrito en la caja de entrada.
def add_airport():
    global airports

    data = entry.get().strip().split()

    if len(data) != 3:
        messagebox.showerror("Error", "Format: CODE LAT LON")
        return

    try:
        code = data[0].upper()
        lat = float(data[1])
        lon = float(data[2])

        airport = Airport(code, lat, lon, False)
        SetSchengen(airport)

        found = False
        i = 0

        # Comprobamos manualmente si el codigo ya existe antes de anadirlo.
        while i < len(airports):
            if airports[i].ICAO == code:
                found = True
            i += 1

        if found:
            messagebox.showinfo("Info", "Airport already exists")
            return

        AddAirport(airports, airport)
        refresh_list()
        update_info()
        messagebox.showinfo("OK", "Airport added")

    except ValueError:
        messagebox.showerror("Error", "Latitude and longitude must be numbers")


# Elimina de la lista el aeropuerto cuyo codigo ICAO se escribe en la entrada.
def remove_airport():
    global airports

    code = entry.get().strip().upper()

    if not code:
        messagebox.showinfo("Remove Airport", "Enter the ICAO code to remove")
        return

    found = False
    i = 0

    # Buscamos el aeropuerto por codigo ICAO antes de intentar eliminarlo.
    while i < len(airports):
        if airports[i].ICAO == code:
            found = True
        i += 1

    if not found:
        messagebox.showerror("Error", "Airport not found")
        return

    RemoveAirport(airports, code)
    refresh_list()
    update_info()
    messagebox.showinfo("OK", f"Airport {code} removed")


# Recalcula el valor Schengen de todos los aeropuertos cargados.
def set_schengen_all():
    if not airports:
        messagebox.showerror("Error", "No airports loaded")
        return

    # Actualizamos cada aeropuerto usando el prefijo ICAO que define su pais/zona.
    update_schengen_values(airports)

    refresh_list()
    update_info()
    messagebox.showinfo("OK", "Schengen values updated")


# Muestra un grafico resumen de aeropuertos Schengen y no Schengen.
def plot_airports():
    if not airports:
        messagebox.showerror("Error", "No airports loaded")
        return

    PlotAirports(airports)


# Genera un archivo KML con la posicion de los aeropuertos cargados.
def map_airports():
    if not airports:
        messagebox.showerror("Error", "No airports loaded")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".kml")

    if not filename:
        return

    MapAirports(airports, filename)
    messagebox.showinfo("OK", "Airport KML saved")


# Carga el archivo de llegadas y lo muestra en la caja de texto.
def load_arrivals_file():
    global aircrafts

    filename = filedialog.askopenfilename(
        title="Select arrivals file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if not filename:
        return

    aircrafts = LoadArrivals(filename)

    textBox.delete(1.0, END)
    with open(filename, "r") as f:
        textBox.insert(END, f.read())

    update_info()
    messagebox.showinfo("OK", "Arrivals loaded")


# Guarda los vuelos cargados en un archivo elegido por el usuario.
def save_flights():
    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".txt")

    if not filename:
        return

    SaveFlights(aircrafts, filename)
    messagebox.showinfo("OK", "Flights saved")


# Dibuja la distribucion de llegadas por hora.
def plot_arrivals():
    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    PlotArrivals(aircrafts)


# Dibuja cuantos vuelos hay por aerolinea.
def plot_airlines():
    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    PlotAirlines(aircrafts)


# Genera un KML con las rutas de los vuelos hacia Barcelona.
def map_flights():
    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    filename = filedialog.asksaveasfilename(defaultextension=".kml")

    if not filename:
        return

    MapFlights(aircrafts, filename)
    messagebox.showinfo("OK", "Flights KML saved")


# Dibuja las llegadas separando vuelos Schengen y no Schengen.
def plot_arrivals_schengen():
    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    extra = {
        "aircrafts": aircrafts,
        "airports": airports
    }

    PlotArrivalsSchengen(extra)


# Carga la estructura de terminales, areas y puertas del aeropuerto LEBL.
def load_lebl_structure():
    global bcn_airport

    filename = filedialog.askopenfilename(
        title="Select terminal structure file",
        filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
    )

    if not filename:
        return

    bcn_airport = LoadAirportStructure(filename)

    if bcn_airport == -1:
        messagebox.showerror("Error", "Could not load LEBL structure")
        bcn_airport = None
        return

    update_info()
    messagebox.showinfo("OK", "LEBL structure loaded")


# Asigna una puerta a cada vuelo segun terminal, aerolinea y tipo Schengen.
def assign_gates():
    if bcn_airport is None:
        messagebox.showerror("Error", "No LEBL structure loaded")
        return

    if not aircrafts:
        messagebox.showerror("Error", "No arrivals loaded")
        return

    ResetGates(bcn_airport)

    assigned = 0
    failed = 0

    i = 0

    # Recorremos todos los vuelos cargados e intentamos asignar una puerta a cada uno.
    while i < len(aircrafts):
        result = AssignGate(bcn_airport, aircrafts[i])

        if result == 0:
            assigned += 1
        else:
            failed += 1

        i += 1

    update_info()
    messagebox.showinfo("Gate Assignment", f"Assigned: {assigned}\nFailed: {failed}")


# Muestra graficamente que puertas estan libres u ocupadas.
def plot_gate_occupancy():
    if bcn_airport is None:
        messagebox.showerror("Error", "No LEBL structure loaded")
        return

    occupancy = GateOccupancy(bcn_airport)
    PlotAirportOccupancy(occupancy)


# Actualiza la lista visible de aeropuertos en la parte derecha de la ventana.
def refresh_list():
    listBox.delete(1.0, END)

    i = 0

    # Reconstruimos la lista visible desde cero para que coincida con los datos actuales.
    while i < len(airports):
        airport = airports[i]
        schengen_text = "Schengen" if airport.SCHENGEN else "Not Schengen"
        listBox.insert(
            END,
            f"{airport.ICAO} ({airport.latitude:.4f}, {airport.longitude:.4f}) - {schengen_text}\n"
        )
        i += 1


# Actualiza el contador superior con los datos cargados actualmente.
def update_info():
    total_airports = len(airports)
    total_schengen = 0
    i = 0

    # Contamos los aeropuertos Schengen sin usar for, siguiendo el estilo del proyecto.
    while i < len(airports):
        if airports[i].SCHENGEN:
            total_schengen += 1
        i += 1
    total_arrivals = len(aircrafts)


    infoLabel.config(
        text=f"Airports: {total_airports} | Schengen: {total_schengen} | Arrivals: {total_arrivals}"
    )


# Creamos la ventana principal y la dividimos en panel izquierdo y derecho.
window = Tk()
window.title("Airport, Aircraft and LEBL Manager")
window.geometry("1000x650")

left_frame = Frame(window, width=280)
left_frame.pack(side="left", fill="y")

right_frame = Frame(window)
right_frame.pack(side="right", fill="both", expand=True)

# Botones relacionados con aeropuertos.
Label(left_frame, text="AIRPORT FUNCTIONS", font=("Arial", 14)).pack(pady=10)

entry = Entry(left_frame)
entry.pack(fill="x", padx=10, pady=5)

Button(left_frame, text="Add Airport", command=add_airport).pack(fill="x", padx=10)
Button(left_frame, text="Remove Airport", command=remove_airport).pack(fill="x", padx=10)
Button(left_frame, text="Set Schengen", command=set_schengen_all).pack(fill="x", padx=10)
Button(left_frame, text="Plot Airports", command=plot_airports).pack(fill="x", padx=10)
Button(left_frame, text="Load Airports", command=load_airports_file).pack(fill="x", padx=10, pady=(15, 0))
Button(left_frame, text="Save Schengen", command=save_schengen).pack(fill="x", padx=10)
Button(left_frame, text="Map Airports", command=map_airports).pack(fill="x", padx=10)

# Botones relacionados con vuelos y aeronaves.
Label(left_frame, text="AIRCRAFT FUNCTIONS", font=("Arial", 14)).pack(pady=(25, 10))

Button(left_frame, text="Load Arrivals", command=load_arrivals_file).pack(fill="x", padx=10)
Button(left_frame, text="Save Flights", command=save_flights).pack(fill="x", padx=10)
Button(left_frame, text="Plot Arrivals", command=plot_arrivals).pack(fill="x", padx=10)
Button(left_frame, text="Plot Airlines", command=plot_airlines).pack(fill="x", padx=10)
Button(left_frame, text="Map Flights", command=map_flights).pack(fill="x", padx=10)
Button(left_frame, text="Plot Arrivals Schengen", command=plot_arrivals_schengen).pack(fill="x", padx=10)

# Botones relacionados con terminales, puertas y ocupacion de LEBL.
Label(left_frame, text="LEBL FUNCTIONS", font=("Arial", 14)).pack(pady=(25, 10))

Button(left_frame, text="Load LEBL Structure", command=load_lebl_structure).pack(fill="x", padx=10)
Button(left_frame, text="Assign Gates", command=assign_gates).pack(fill="x", padx=10)
Button(left_frame, text="Plot Gate Occupancy", command=plot_gate_occupancy).pack(fill="x", padx=10)

# Etiqueta superior con el resumen de datos cargados.
infoLabel = Label(
    right_frame,
    text="Airports: 0 | Schengen: 0 | Arrivals: 0",
    font=("Arial", 12)
)
infoLabel.pack(pady=5)

# Caja de texto donde se muestra el contenido del archivo cargado.
textBox = Text(right_frame, height=10)
textBox.pack(fill="x", padx=10, pady=5)

Label(right_frame, text="Airports list:").pack()

# Caja donde se lista cada aeropuerto con sus coordenadas y estado Schengen.
listBox = Text(right_frame)
listBox.pack(fill="both", expand=True, padx=10, pady=5)

# Inicia el bucle principal de la interfaz grafica.
window.mainloop()


