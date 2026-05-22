import matplotlib.pyplot as plt
try:
    from project.airport import LoadAirports, SetSchengen
except ModuleNotFoundError:
    from airport import LoadAirports, SetSchengen


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
            # Saltamos la cabecera que no contiene nada importante
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
    i = 0

    while i < len(aircrafts):
        partes = aircrafts[i].arrival.split(':')
        hora = int(partes[0])

        # Si la hora es real, sumamos la frecuencia de la hora correspondiente
        if 0 <= hora < 24:
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

    # Recorremos toda la lista
    i = 0
    while i < len(aircrafts):
        # Accedemos al elemento usando el índice [i] que le llamaremos vuelo
        vuelo = aircrafts[i]

        # Procesamiento de cada campo
        if vuelo.ICAO == "" or vuelo.ICAO is None:
            icao = "-"
        else:
            icao = vuelo.ICAO

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
    # Comprobamos si hay vuelos para mostrar
    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    # Listas para guardar aerolíneas y frecuencias
    airlines = []
    frequencies = []

    # Recorremos todos los vuelos
    i = 0
    while i < len(aircrafts):
        airline = aircrafts[i].airline

        # Buscamos la aerolínea en la lista
        found = False
        position = 0
        j = 0

        while j < len(airlines):
            if airlines[j] == airline:
                found = True
                position = j
            j += 1

        # Actualizamos la frecuencia o añadimos la aerolínea
        if found:
            frequencies[position] += 1
        else:
            airlines.append(airline)
            frequencies.append(1)

        i += 1

    # Dibujamos el gráfico de barras
    plt.bar(airlines, frequencies, color='orange')
    plt.xlabel('Airline')
    plt.ylabel('Number of flights')
    plt.title('Number of flights by airline')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

def PlotArrivalsSchengen(extra):

    if isinstance(extra, dict):
        aircrafts = extra.get("aircrafts", [])
        airports = extra.get("airports", [])
    else:
        aircrafts = extra
        airports = []

    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    if not airports:
        try:
            airports = LoadAirports("Airports.txt")
        except FileNotFoundError:
            print("Error: No hay aeropuertos para comparar Schengen.")
            return

    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    schengen_hours = [0] * 24
    not_schengen_hours = [0] * 24

    i = 0
    while i < len(aircrafts):
        flight = aircrafts[i]

        partes = flight.arrival.split(":")
        hour = int(partes[0])

        origin_airport = None

        j = 0
        while j < len(airports):
            if airports[j].ICAO == flight.origin:
                origin_airport = airports[j]
            j += 1

        if origin_airport is not None and 0 <= hour < 24:
            if origin_airport.SCHENGEN:
                schengen_hours[hour] += 1
            else:
                not_schengen_hours[hour] += 1

        i += 1

    hours = range(24)

    plt.bar(hours, schengen_hours, color="turquoise", label="Schengen")
    plt.bar(hours, not_schengen_hours, bottom=schengen_hours, color="orange", label="Not Schengen")

    plt.xlabel("Hora del día")
    plt.ylabel("Número de llegadas")
    plt.title("Llegadas por hora: Schengen / Not Schengen")
    plt.legend()
    plt.tight_layout()
    plt.show()


def MapFlights(aircrafts, filename="map_flights.kml"):
    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    airports = LoadAirports("Airports")

    # Marcamos si cada aeropuerto es Schengen o no
    i = 0
    while i < len(airports):
        SetSchengen(airports[i])
        i += 1

    # Buscamos el aeropuerto de Barcelona
    i = 0
    while airports[i].ICAO != "LEBL":
        i += 1
    barcelona = airports[i]

    f = open(filename, 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Flights to Barcelona</name>\n')

    # Recorremos todos los vuelos
    i = 0
    while i < len(aircrafts):
        origin_code = aircrafts[i].origin

        # Buscamos el aeropuerto de origen
        origin_airport = None
        j = 0
        while j < len(airports):
            if airports[j].ICAO == origin_code:
                origin_airport = airports[j]
            j += 1

        # Dibujamos la línea si el aeropuerto existe
        if origin_airport is not None:
            if origin_airport.SCHENGEN:
                color = "ff0000ff"
            else:
                color = "ffff0000"

            f.write('  <Placemark>\n')
            f.write('    <name>' + origin_code + ' to LEBL</name>\n')
            f.write('    <Style>\n')
            f.write('      <LineStyle>\n')
            f.write('        <color>' + color + '</color>\n')
            f.write('        <width>2</width>\n')
            f.write('      </LineStyle>\n')
            f.write('    </Style>\n')
            f.write('    <LineString>\n')
            f.write('      <coordinates>\n')
            f.write('        ' + str(origin_airport.longitude) + ',' + str(origin_airport.latitude) + ',0 '
                    + str(barcelona.longitude) + ',' + str(barcelona.latitude) + ',0\n')
            f.write('      </coordinates>\n')
            f.write('    </LineString>\n')
            f.write('  </Placemark>\n')

        i += 1

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()

    print(f"Archivo {filename} generado. Ábrelo con Google Earth.")


if __name__ == "__main__":
    arrivals = LoadArrivals("arrivals.txt")
    PlotArrivals(arrivals)
    PlotAirlines(arrivals)
    MapFlights(arrivals, "Mapa_Vuelos.kml")
