class BarcelonaAP:
    def __init__(self, code):
        self.code = code              # Código ICAO del aeropuerto (ej.: "LEBL")
        self.terminals = []           # Lista de objetos Terminal


class Terminal:
    def __init__(self, name):
        self.name = name              # Nombre de la terminal (ej.: "T1")
        self.boarding_areas = []      # Lista de objetos BoardingArea
        self.airlines = []            # Lista de códigos ICAO de aerolíneas


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name              # Nombre del área (ej.: "T1BAa")
        self.area_type = area_type    # "Schengen" o "no-Schengen"
        self.gates = []               # Lista de objetos Gate


class Gate:
    def __init__(self, name):
        self.name = name              # Nombre de la puerta (ej.: "T1BAaG1")
        self.occupied = False         # Booleano: True si está ocupada
        self.aircraft_id = None       # ID de la aeronave si está ocupada

