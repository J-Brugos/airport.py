import matplotlib.pyplot as plt
class Arrival:
    def __init__(self, ICAO, origin, arrival, airline):
        self.ICAO = ICAO
        self.origin = origin
        self.arrival = arrival
        self.airline = airline

    def __str__(self):
        return f"{self.ICAO} ({self.origin}) - {self.arrival} - {self.airline}"

def LoadArrivals(filename):
    p = []  # Tu lista de objetos (como en LoadAirports)

    try:
        with open(filename, 'r') as f:
            #Saltamos la cabecera que no contiene nada importante
            f.readline()

            for linea in f:
                datos = linea.strip().split()
                icao = datos[0]
                origin = datos[1]
                arrival = datos[2]
                airline = datos[3]
                # Creamos el objeto y lo añadimos a la lista
                vuelo = Arrival(icao, origin, arrival, airline)
                p.append(vuelo)

    except FileNotFoundError:
        # Si el fichero no existe, retornamos lista vacía
        return []

    return p

def PlotArrivals(aircrafts):
    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    frecuencias = [0] * 24

    for vuelo in aircrafts:
        try:
            partes = vuelo.arrival.split(':')
            hora = int(partes[0])

            if 0 <= hora < 24:
                frecuencias[hora] += 1
        except:
            continue

    horas = range(24)
    plt.bar(horas, frecuencias, color='turquoise')
    plt.xlabel('Hora del día')
    plt.ylabel('Número de vuelos')
    plt.title('Frecuencia de llegadas')
    plt.show()