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
    frecuencias = [0] * 24
    i=0
    while i < len(aircrafts):
            partes = aircrafts[i].arrival.split(':')
            hora = int(partes[0])

            if 0 <= hora < 24: #si la hora es real, sumamos la frecuencia de la hora correspondiente
                frecuencias[hora] += 1
            i = i + 1


    horas = range(24)
    plt.bar(horas, frecuencias, color='turquoise')
    plt.xlabel('Hora del día')
    plt.ylabel('Número de vuelos')
    plt.title('Frecuencia de llegadas')
    plt.show()


def SaveFlights(aircrafts, filename):
    file = open(filename, 'w')
    file.write("AIRCRAFT ORIGIN ARRIVAL AIRLINE\n")

    #Recorremos toda la lista
    i = 0
    while i < len(aircrafts):
        # Accedemos al elemento usando el índice [i] que le llamaremos vuelo.
        vuelo = aircrafts[i]

        # Procesamiento de cada campo
        if vuelo.ICAO == "" or vuelo.ICAO is None: #si no existe pues dejaremos un guión como nos piden
            icao = "-"
        else:
            icao = vuelo.ICAO #De lo contrario, lo añadiremos.

        if vuelo.origin == "" or vuelo.origin is None:
            origin = "-"
        else:
            origin = vuelo.origin

        if vuelo.arrival == "" or vuelo.arrival is None:
            arrival = "-"
        else:
            arrival = vuelo.arrival

        if vuelo.airline == "" or vuelo.airline is None:
            airline = "-"
        else:
            airline = vuelo.airline

        # Escribimos la línea
        file.write(icao + " " + origin + " " + arrival + " " + airline + "\n")

        i = i + 1

    file.close()

def PlotAirlines(aircrafts):
    # Check if there are flights to show
    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    # Lists to store airline names and their flight counts
    airlines = []
    frequencies = []

    # Go through all flights
    i = 0
    while i < len(aircrafts):
        airline = aircrafts[i].airline

        # Search for the airline in the list
        found = False
        position = 0
        j = 0

        while j < len(airlines):
            if airlines[j] == airline:
                found = True
                position = j
            j += 1

        # Update count or add a new airline
        if found:
            frequencies[position] += 1
        else:
            airlines.append(airline)
            frequencies.append(1)

        i += 1

    # Draw the bar chart
    plt.bar(airlines, frequencies, color='orange')
    plt.xlabel('Airline')
    plt.ylabel('Number of flights')
    plt.title('Number of flights by airline')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

#test section
aircraft = LoadArrivals("arrivals.txt") # Cargamos los datos del archivo que creamos
PlotArrivals(aircraft) # Llamamos a la función de gráfico
arrivals = LoadArrivals("arrivals.txt") # Cargamos los datos del archivo que creamos
PlotAirlines(arrivals) # Llamamos a la función de gráfico
