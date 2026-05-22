import os
import matplotlib.pyplot as plt

# Importamos la funcion que permite saber si el origen de un vuelo es Schengen.
try:
    from project.airport import IsSchengenAirport
except ModuleNotFoundError:
    from airport import IsSchengenAirport


# Representa una puerta concreta del aeropuerto.
class Gate:
    def __init__(self, name):
        self.name = name
        self.occupied = False
        self.aircraft_id = None


# Representa una zona de embarque, que puede ser Schengen o no Schengen.
class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name
        self.area_type = False
        self.gates = []

        if area_type == "Schengen":
            self.area_type = True


# Representa una terminal con sus zonas de embarque y aerolineas asociadas.
class Terminal:
    def __init__(self, name):
        self.name = name
        self.boarding_areas = []
        self.airlines = []


# Representa el aeropuerto de Barcelona con todas sus terminales.
class BarcelonaAP:
    def __init__(self, code):
        self.code = code
        self.terminals = []


# Crea las puertas de una zona a partir del primer y ultimo numero de puerta.
def SetGates(area, init_gate, end_gate, prefix):
    if end_gate <= init_gate:
        return -1

    area.gates = []

    i = init_gate

    # Generamos los nombres de puertas usando el prefijo de terminal y zona.
    while i <= end_gate:
        gate_name = prefix + str(i)
        new_gate = Gate(gate_name)
        area.gates.append(new_gate)
        i += 1

    return 0


# Carga las aerolineas de una terminal desde archivo o usa valores por defecto.
def LoadAirlines(terminal, t_name, base_path=""):
    file_name = os.path.join(base_path, t_name + "_Airlines.txt")

    try:
        file = open(file_name, "r")
        lines = file.readlines()
        file.close()

        new_airlines = []

        i = 0

        # Cada linea puede contener texto, pero usamos el ultimo dato como codigo.
        while i < len(lines):
            clean_line = lines[i].strip()

            if clean_line != "":
                words = clean_line.split()
                airline_code = words[-1].upper()
                new_airlines.append(airline_code)

            i += 1

        terminal.airlines = new_airlines
        return 0

    except FileNotFoundError:
        # Si no existe archivo externo, usamos listas basicas para T1 y T2.
        if t_name == "T1":
            terminal.airlines = [
                "VLG", "IBE", "AEA", "DLH", "SWR", "KLM", "BAW", "AFR",
                "TAP", "AZA", "EZY", "SWT", "IBK", "LAV", "EFD", "UPS",
                "THY"
            ]
            return 0

        if t_name == "T2":
            terminal.airlines = [
                "RYR", "EJU", "WZZ", "TRA", "TUI", "TOM", "NSZ"
            ]
            return 0

        return -1


# Carga la estructura completa de LEBL: aeropuerto, terminales, areas y puertas.
def LoadAirportStructure(filename):
    try:
        file = open(filename, "r")
        lines = file.readlines()
        file.close()

        base_path = os.path.dirname(filename)

        first_line = lines[0].strip().split()
        airport_code = first_line[0]
        airport = BarcelonaAP(airport_code)

        current_terminal = None

        i = 1

        # Recorremos el archivo y creamos objetos segun el tipo de linea.
        while i < len(lines):
            clean_line = lines[i].strip()

            if clean_line != "":
                words = clean_line.split()
                line_type = words[0]

                if line_type == "Terminal":
                    # Al crear una terminal, tambien cargamos sus aerolineas.
                    terminal_name = words[1]
                    current_terminal = Terminal(terminal_name)
                    LoadAirlines(current_terminal, terminal_name, base_path)
                    airport.terminals.append(current_terminal)

                elif line_type == "Area":
                    # Cada area crea un rango de puertas dentro de la terminal actual.
                    area_letter = words[1]
                    area_type = words[2]
                    first_gate = int(words[4])
                    last_gate = int(words[6])

                    new_area = BoardingArea(area_letter, area_type)
                    prefix = current_terminal.name + "-" + area_letter + "-"
                    SetGates(new_area, first_gate, last_gate, prefix)
                    current_terminal.boarding_areas.append(new_area)

            i += 1

        return airport

    except FileNotFoundError:
        return -1


# Comprueba si una aerolinea pertenece a una terminal concreta.
def IsAirlineInTerminal(terminal, name):
    if name == "":
        return False, -1

    airline_name = name.upper()

    i = 0

    # Buscamos el codigo de aerolinea dentro de la lista de la terminal.
    while i < len(terminal.airlines):
        if terminal.airlines[i].upper() == airline_name:
            return True

        i += 1

    return False


# Busca en que terminal opera una aerolinea.
def SearchTerminal(bcn, name):
    i = 0

    while i < len(bcn.terminals):
        terminal = bcn.terminals[i]

        if IsAirlineInTerminal(terminal, name) == True:
            return terminal.name

        i += 1

    return ""


# Asigna la primera puerta libre compatible con la terminal y el tipo de vuelo.
def AssignGate(bcn, aircraft):
    terminal_name = SearchTerminal(bcn, aircraft.airline)

    if terminal_name == "":
        return -1

    is_flight_schengen = IsSchengenAirport(aircraft.origin[:2])

    target_terminal = None

    i = 0

    # Localizamos el objeto Terminal que corresponde a la aerolinea del vuelo.
    while i < len(bcn.terminals):
        if bcn.terminals[i].name == terminal_name:
            target_terminal = bcn.terminals[i]
            break

        i += 1

    if target_terminal is None:
        return -1

    selected_gate = None

    j = 0

    # Recorremos las areas de embarque buscando una puerta libre del tipo correcto.
    while j < len(target_terminal.boarding_areas):
        area = target_terminal.boarding_areas[j]

        if area.area_type == is_flight_schengen:
            k = 0

            while k < len(area.gates):
                gate = area.gates[k]

                if not gate.occupied and selected_gate is None:
                    selected_gate = gate

                k += 1

        j += 1

    if selected_gate is None:
        return -1

    # Marcamos la puerta como ocupada y guardamos el identificador del avion.
    selected_gate.occupied = True
    selected_gate.aircraft_id = aircraft.ICAO

    return 0


# Libera todas las puertas para poder hacer una nueva asignacion desde cero.
def ResetGates(bcn):
    if bcn is None:
        return

    t = 0

    # Recorremos terminales, areas y puertas para limpiar su estado.
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                area.gates[g].occupied = False
                area.gates[g].aircraft_id = None
                g += 1

            a += 1

        t += 1


# Convierte el estado de puertas en una lista de diccionarios facil de graficar.
def GateOccupancy(bcn):
    occupancy_list = []

    t_idx = 0

    # Guardamos una fila de informacion por cada puerta del aeropuerto.
    while t_idx < len(bcn.terminals):
        terminal = bcn.terminals[t_idx]

        a_idx = 0
        while a_idx < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a_idx]

            g_idx = 0
            while g_idx < len(area.gates):
                gate = area.gates[g_idx]

                if gate.occupied:
                    status = "occupied"
                else:
                    status = "free"

                occupancy_list.append({
                    "terminal": terminal.name,
                    "boarding_area": area.name,
                    "gate_name": gate.name,
                    "status": status,
                    "aircraft_id": gate.aircraft_id
                })

                g_idx += 1

            a_idx += 1

        t_idx += 1

    return occupancy_list


# Dibuja la ocupacion de puertas por terminal y area de embarque.
def PlotAirportOccupancy(occupancy_data):
    if len(occupancy_data) == 0:
        print("No gate layout data available to display.")
        return

    terminals = []

    i = 0

    # Primero obtenemos la lista de terminales presentes en los datos.
    while i < len(occupancy_data):
        terminal_name = occupancy_data[i]["terminal"]

        if terminal_name not in terminals:
            terminals.append(terminal_name)

        i += 1

    t_idx = 0
    while t_idx < len(terminals):
        current_terminal = terminals[t_idx]

        areas = []

        i = 0

        # Para cada terminal, buscamos sus areas de embarque.
        while i < len(occupancy_data):
            if occupancy_data[i]["terminal"] == current_terminal:
                area_name = occupancy_data[i]["boarding_area"]

                if area_name not in areas:
                    areas.append(area_name)

            i += 1

        fig, axes = plt.subplots(1, len(areas), figsize=(3.5 * len(areas), 8))

        if len(areas) == 1:
            axes = [axes]

        a_idx = 0
        while a_idx < len(areas):
            current_area = areas[a_idx]
            ax = axes[a_idx]

            area_gates = []

            i = 0

            # Filtramos solo las puertas que pertenecen al area actual.
            while i < len(occupancy_data):
                if (
                    occupancy_data[i]["terminal"] == current_terminal
                    and occupancy_data[i]["boarding_area"] == current_area
                ):
                    area_gates.append(occupancy_data[i])

                i += 1

            occupied_count = 0

            i = 0

            # Contamos cuantas puertas estan ocupadas para mostrarlo en el titulo.
            while i < len(area_gates):
                if area_gates[i]["status"] == "occupied":
                    occupied_count += 1

                i += 1

            ax.set_title(
                current_area + "\n" + str(occupied_count) + "/" + str(len(area_gates)) + " occupied",
                fontsize=11,
                weight="bold"
            )

            cols = 4
            g_idx = 0

            # Dibujamos cada puerta como un rectangulo verde o rojo.
            while g_idx < len(area_gates):
                gate_info = area_gates[g_idx]

                col = g_idx % cols
                row = g_idx // cols

                if gate_info["status"] == "occupied":
                    color = "#d9534f"
                    text_color = "white"
                else:
                    color = "#5cb85c"
                    text_color = "black"

                rect = plt.Rectangle(
                    (col, -row),
                    0.85,
                    0.85,
                    facecolor=color,
                    edgecolor="black"
                )
                ax.add_patch(rect)

                gate_number = gate_info["gate_name"].split("-")[-1]
                label = "G" + gate_number

                if gate_info["aircraft_id"] is not None:
                    label += "\n" + str(gate_info["aircraft_id"])

                ax.text(
                    col + 0.425,
                    -row + 0.425,
                    label,
                    ha="center",
                    va="center",
                    fontsize=7,
                    color=text_color,
                    weight="bold"
                )

                g_idx += 1

            rows = (len(area_gates) - 1) // cols + 1

            ax.set_xlim(-0.2, cols)
            ax.set_ylim(-rows, 1)
            ax.axis("off")

            a_idx += 1

        fig.suptitle("LEBL Gate Occupancy - " + current_terminal, fontsize=16, weight="bold")
        plt.tight_layout()
        plt.show()

        t_idx += 1


# Prueba rapida del modulo cuando se ejecuta LEBL.py directamente.
if __name__ == "__main__":
    bcn = LoadAirportStructure("Terminals.txt")

    if bcn == -1:
        print("Error: Terminals.txt not found.")
    else:
        print("Airport:", bcn.code)
        print("Total terminals:", len(bcn.terminals))

        occupancy = GateOccupancy(bcn)
        PlotAirportOccupancy(occupancy)

