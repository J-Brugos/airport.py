
class Gate:
    def __init__(self, name):
        self.name = name  # Nombre de la puerta (ej.: "T1BAaG1")
        self.occupied = False  # Booleano: True si está ocupada
        self.aircraft_id = None  # ID de la aeronave si está ocupada


class BoardingArea:
    def __init__(self, name, area_type):
        self.name = name  # Nombre del área (ej.: "T1BAa")
        self.area_type = False  # "Schengen" boolean
        self.gates = []  # Lista de objetos Gate

        # Lógica para el booleano: si el texto es "Schengen", pasa a True
        if area_type == "Schengen":
            self.area_type = True


class Terminal:
    def __init__(self, name):
        self.name = name  # Nombre de la terminal (ej.: "T1")
        self.boarding_areas = []  # Lista de objetos BoardingArea
        self.airlines = []  # Lista de códigos ICAO de aerolíneas


class BarcelonaAP:
    def __init__(self, code):
        self.code = code  # Código ICAO del aeropuerto (ej.: "LEBL")
        self.terminals = []  # Lista de objetos Terminal


# --- Funciones ---

def SetGates(area, init_gate, end_gate, prefix):
    # Si el número final no es mayor al inicial, error (-1)
    if end_gate <= init_gate:
        return -1

    # Se elimina la lista previa si existía
    area.gates = []

    i = init_gate
    while i <= end_gate:
        # Concatenación del prefijo y el número de puerta
        nombre_p = prefix + str(i)
        nueva_puerta = Gate(nombre_p)

        # Se añade a la lista de puertas del objeto area
        area.gates.append(nueva_puerta)
        i += 1

    return 0


def LoadAirlines(terminal, t_name):
    # Construimos el nombre del archivo (ej: "T1_Airlines.txt")
    file_name = t_name + "_Airlines.txt"

    try:
        # Intentamos abrir el archivo
        file = open(file_name, 'r')

        # Leemos las líneas
        lines = file.readlines()

        nuevas_aerolineas = []

        # Recorremos las líneas leídas con un bucle while
        i = 0
        while i < len(lines):
            linea_limpia = lines[i].strip()

            # Si la línea contiene texto, extraemos el código
            if linea_limpia != "":
                # dividimos la línea en una lista de palabras usando los espacios como separadores
                palabras = linea_limpia.split()

                # Guardamos la última palabra de la lista (el código ICAO)
                codigo_icao = palabras[-1]

                # Añadimos el código a nuestra lista temporal
                nuevas_aerolineas.append(codigo_icao)

            i += 1

        # Actualizamos la terminal
        terminal.airlines = nuevas_aerolineas
        #Cerramos el archivo
        file.close()

    except FileNotFoundError:
        # Si el archivo no existe, devolvemos error
        return -1


def LoadAirportStructure(filename):
    try:
        file = open(filename, 'r')
        lines = file.readlines()
        file.close()

        # 1. De la primera línea sacamos el código del aeropuerto (ej: "LEBL")
        primera_linea = lines[0].strip().split()
        codigo_ap = primera_linea[0]
        aeropuerto = BarcelonaAP(codigo_ap)

        # Variables auxiliares para recordar en qué terminal estamos trabajando
        terminal_actual = None

        # 2. Recorremos el resto de líneas con un while
        i = 1
        while i < len(lines):
            linea_limpia = lines[i].strip()

            if linea_limpia != "":
                palabras = linea_limpia.split()
                tipo_linea = palabras[0]  # Puede ser "Terminal" o "Area"

                # --- SI ES UNA TERMINAL ---
                if tipo_linea == "Terminal":
                    t_name = palabras[1]  # "T1" o "T2"
                    terminal_actual = Terminal(t_name)

                    # REQUISITO: Cargamos las aerolíneas de esta terminal
                    LoadAirlines(terminal_actual, t_name)

                    # Guardamos la terminal en el aeropuerto
                    aeropuerto.terminals.append(terminal_actual)

                # --- SI ES UN ÁREA DE EMBARQUE ---
                elif tipo_linea == "Area":
                    letra_area = palabras[1]  # "A", "B", "M", etc.
                    tipo_area = palabras[2]  # "Schengen" o "non-Schengen"

                    # Las puertas están fijas en las posiciones 5 y 7 de la línea
                    # Ejemplo: ["Area", "A", "Schengen", "Gates", "1", "-", "11"]
                    p_inicio = int(palabras[4])  # 1
                    p_fin = int(palabras[6])  # 11

                    # Creamos el objeto BoardingArea (le pasamos la letra y el tipo)
                    # El constructor interno ya pondrá True si es "Schengen"
                    nueva_area = BoardingArea(letra_area, tipo_area)

                    # REQUISITO: Prefijo único por área para SetGates (ej: "T1-A-")
                    prefijo = terminal_actual.name + "-" + letra_area + "-"
                    SetGates(nueva_area, p_inicio, p_fin, prefijo)

                    # Añadimos la zona a la terminal en la que estamos
                    terminal_actual.boarding_areas.append(nueva_area)

            i += 1

        return aeropuerto

    except FileNotFoundError:
        return -1

#test section
#LOAD AIRLINES
t = Terminal("T1")
t.airlines = ["VIEJA1", "VIEJA2"]

# Probamos carga normal
LoadAirlines(t, "T1")
print("Resultado T1:", t.airlines)

# Probamos error con un archivo que no exista
err = LoadAirlines(t, "T3")
print("Código error (debe ser -1):", err)
print("Terminal tras error (no cambia):", t.airlines)

#AIRPORT STRUCTURE
mi_aeropuerto = LoadAirportStructure("Terminals.txt")

if mi_aeropuerto == -1:
    print("Error: El archivo Terminals.txt no existe.")
else:
    print("--- TEST AEROPUERTO ---")
    print("Código Aeropuerto:", mi_aeropuerto.code)  # Debe poner LEBL
    print("Total Terminales:", len(mi_aeropuerto.terminals))  # Debe poner 2

    # Comprobamos la T1
    t1 = mi_aeropuerto.terminals[0]
    print("\nTerminal:", t1.name)  # T1
    print("Zonas en T1:", len(t1.boarding_areas))  # Debería poner 5 (A, B, C, D, E)
    print("Primera puerta de la Zona A:", t1.boarding_areas[0].gates[0].name)  # Ej: T1-A-1
    print("Aerolíneas cargadas en T1 (primeras 3):", t1.airlines[:3])  # Códigos ICAO