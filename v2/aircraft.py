import matplotlib.pyplot as plt
from airport import IsSchengenAirport,LoadAirports



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
        if vuelo.ICAO == "":  #si no existe pues dejaremos un guión como nos piden
            icao = "-"
        else:
            icao = vuelo.ICAO #De lo contrario, lo añadiremos.

        if vuelo.origin == "" :
            origin = "-"
        else:
            origin = vuelo.origin

        if vuelo.arrival == "" :
            arrival = "-"
        else:
            arrival = vuelo.arrival

        if vuelo.airline == "" :
            airline = "-"
        else:
            airline = vuelo.airline

        # Escribimos la línea
        file.write(icao + " " + origin + " " + arrival + " " + airline + "\n")

        i = i + 1

    file.close()

def PlotAirlines(aircrafts):
    # Chequeamos que hay una lista
    if not aircrafts:
        print("Error: No hay vuelos para mostrar.")
        return

    airlines = []
    frequencies = []

    # Buscamos entre todos los vuelos
    i = 0
    while i < len(aircrafts):
        airline = aircrafts[i].airline

        # Buscamos la aerolinea en la lista
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
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.show()

def PlotFlightsType(aircrafts):
    schengen_count = 0
    non_schengen_count = 0

    # Recorremos la lista aircraft
    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]
        es_schengen= IsSchengenAirport(vuelo.origin[:2]) #IMPORTANTE, SOLO COGER LOS DOS PRIMEROS ELEMENTOS
        # Consultamos a la función auxiliar pasando el código de origen
        if  es_schengen:
            schengen_count = schengen_count + 1
        else:
            non_schengen_count = non_schengen_count + 1

        i = i + 1

    # Creamos el gráfico de barras apiladas
    # Dibujamos primero la parte de Schengen
    plt.bar("Tipo de Vuelo", schengen_count, color="skyblue", label="Schengen")

    # Dibujamos la parte de No-Schengen encima, usando 'bottom' para apilar
    plt.bar("Tipo de Vuelo", non_schengen_count, bottom=schengen_count, color="orange", label="Non-Schengen")

    plt.ylabel("Número de vuelos")
    plt.title("Schengen vs Non-Schengen)")
    plt.legend()
    plt.show()


def GetAirportCoordinates(code, lista_airports):
    i = 0
    while i < len(lista_airports):
        if lista_airports[i].ICAO == code:
            return lista_airports[i].latitude, lista_airports[i].longitude
        i = i + 1
def MapFlights(aircrafts):
    # 1. Validación de lista vacía
    if len(aircrafts) == 0:
        print("Error: No hay vuelos para mapear.")
        return

    # 2. Abrir archivo KML
    f = open("flights.kml", "w")

    # Cabecera KML
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')

    # 3. Recorrido con while
    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]

        # Obtenemos coordenadas (ajusta según tu función)
        lat_origen, lon_origen = GetAirportCoordinates(vuelo.origin,LoadAirports("Airports"))
        lat_lebl, lon_lebl = GetAirportCoordinates("LEBL", LoadAirports("Airports"))

        # Definimos el color según si es Schengen
        if IsSchengenAirport(vuelo.origin):
            color = "FF00FF00"  # Verde para Schengen
        else:
            color = "FF0000FF"  # Rojo para No-Schengen

        # Escribir el Placemark con estilo en línea (sin usar id)
        f.write('<Placemark>\n')
        f.write('  <Style>\n')
        f.write('    <LineStyle>\n')
        f.write(f'      <color>{color}</color>\n')
        f.write('      <width>3</width>\n')
        f.write('    </LineStyle>\n')
        f.write('  </Style>\n')
        f.write('  <LineString>\n')
        f.write('    <coordinates>\n')
        f.write(f'      {lon_origen},{lat_origen},0 {lon_lebl},{lat_lebl},0\n')
        f.write('    </coordinates>\n')
        f.write('  </LineString>\n')
        f.write('</Placemark>\n')

        i = i + 1

    # Cerrar archivo
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print("Archivo 'flights.kml' generado correctamente (sin IDs).")

#test section
aircraft = LoadArrivals("arrivals.txt") # Cargamos los datos del archivo que creamos
PlotArrivals(aircraft) # Llamamos a la función de gráfico
PlotAirlines(aircraft)
PlotFlightsType(aircraft)
MapFlights(aircraft)

