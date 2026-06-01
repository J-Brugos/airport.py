import matplotlib.pyplot as plt
from airport import IsSchengenAirport,LoadAirports
import math


class Aircraft:
    def __init__(self, ICAO, origin, arrival, airline, destination, departure):
        self.ICAO = ICAO
        self.origin = origin
        self.arrival = arrival
        self.airline = airline
        self.destination = destination
        self.departure = departure

    def __str__(self):
        return f"{self.ICAO} ({self.airline}) | Arr: {self.origin} {self.arrival} | Dep: {self.destination} {self.departure}"

def LoadArrivals(filename):
    p = []

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
                vuelo = Aircraft(icao, origin, arrival, airline, "", "")
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
    # Cargamos la base de datos de aeropuertos una sola vez fuera del bucle
    airports_db = LoadAirports("Airports.txt")

    # Creamos o abrimos el archivo KML para escribir el mapa
    f = open("flights.kml", "w")

    # Escribimos la cabecera estándar del archivo KML
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Flights Map</name>\n')

    i = 0
    while i < len(aircrafts):
        vuelo = aircrafts[i]

        # Filtro imprescindible: Solo mapeamos si tiene origen (vuelos de llegada)
        # Si es un vuelo de salida pura de la V4, su origen es "" y lo saltamos de forma segura
        if vuelo.origin != "":

            coords_origen = GetAirportCoordinates(vuelo.origin, airports_db)
            coords_lebl = GetAirportCoordinates("LEBL", airports_db)

            # Si ambos aeropuertos existen en la base de datos, dibujamos la línea en el KML
            if coords_origen is not None and coords_lebl is not None:
                f.write('  <Placemark>\n')
                f.write(f'    <name>{vuelo.ICAO} ({vuelo.airline})</name>\n')
                f.write('    <LineString>\n')
                f.write('      <altitudeMode>clampToGround</altitudeMode>\n')
                f.write('      <coordinates>\n')
                # En KML primero va la Longitud y luego la Latitud
                f.write(f'        {coords_origen.longitude},{coords_origen.latitude},0\n')
                f.write(f'        {coords_lebl.longitude},{coords_lebl.latitude},0\n')
                f.write('      </coordinates>\n')
                f.write('    </LineString>\n')
                f.write('  </Placemark>\n')

        # El incremento se ejecuta SIEMPRE para avanzar en el while
        i = i + 1

    # Cerramos las etiquetas del KML y el archivo
    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()


def Haversine(lat1, lon1, lat2, lon2):
    # Radio de la Tierra en km según el documento
    r = 6371.0

    # Factor de conversión manual (pi / 180)
    c_rad = math.pi / 180.0

    # Conversión de grados a radianes[cite: 1]
    phi1 = lat1 * c_rad
    phi2 = lat2 * c_rad
    lam1 = lon1 * c_rad
    lam2 = lon2 * c_rad

    # Diferencias dφ y dλ[cite: 1]
    d_phi = abs(phi1 - phi2)
    d_lam = abs(lam1 - lam2)

    # Cálculo de 'a' y 'c' según las fórmulas de la imagen[cite: 1]
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # d = r * c[cite: 1]
    return r * c
def LongDistanceArrivals(aircrafts):
    # Cargamos aeropuertos y coordenadas de Barcelona (LEBL)
    lista_airports = LoadAirports("Airports.txt") # Recuerda asegurar que se llama "Airports.txt"
    vuelos_largos = []

    # Guardamos temporalmente el resultado de LEBL por seguridad
    coords_dest = GetAirportCoordinates("LEBL", lista_airports)
    if coords_dest is None:
        print("Error: LEBL no está en la base de datos.")
        return []
    lat_dest, lon_dest = coords_dest

    # Bucle while para recorrer la lista
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]

        # Buscamos las coordenadas y las guardamos temporalmente
        coords_orig = GetAirportCoordinates(ac.origin, lista_airports)

        # CONTROL DE NONE: Si el aeropuerto de origen no existe, saltamos al siguiente
        if coords_orig is None:
            i += 1
            continue

        # Si no es None, desempaquetamos de forma segura
        lat_orig, lon_orig = coords_orig

        # Calculamos distancia con Haversine
        distancia = Haversine(lat_orig, lon_orig, lat_dest, lon_dest)

        # Filtro de inspección especial (> 2000 Km)
        if distancia > 2000:
            vuelos_largos.append(ac)

        i += 1

    return vuelos_largos


def LoadDepartures(filename):
    departures_list = []
    try:
        f = open(filename, 'r')
        # Saltamos la cabecera
        f.readline()

        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) == 4:
                icao = datos[0]  # AIRCRAFT
                destination = datos[1]  # DESTINATION
                departure = datos[2]  # DEPARTURE
                airline = datos[3]  # AIRLINE

                vuelo = Aircraft(icao, "", "", airline, destination, departure)
                departures_list.append(vuelo)

            linea = f.readline()
        f.close()
    except FileNotFoundError:
        return []
    return departures_list


def MergeMovements(arrivals, departures):
    # Si alguna lista está vacía, se devuelve un código de error
    if len(arrivals) == 0 or len(departures) == 0:
        return -1

    merged_list = []

    # Para evitar modificar las listas, hacemos una copia de los arrivals
    i = 0
    while i < len(arrivals):
        # Creamos un objeto nuevo con la misma información base de llegada
        ac_arr = arrivals[i]

        new_ac = Aircraft(
            ac_arr.ICAO,
            ac_arr.origin,
            ac_arr.arrival,
            ac_arr.airline,
            "",  # Destino vacío
            ""  # Hora de salida vacía
        )
        merged_list.append(new_ac)
        i += 1

    # Recorremos la lista de salidas para emparejar o añadir como pernocta
    j = 0
    while j < len(departures):
        ac_dep = departures[j]

        # Buscamos si este avión ya existe en nuestra lista unificada
        encontrado = False
        k = 0
        while k < len(merged_list):
            ac_merged = merged_list[k]

            # Si coinciden en matrícula (ICAO)
            if ac_merged.ICAO == ac_dep.ICAO:

                # Comprobamos horarios (arrival < departure_time)
                # Si un avión tiene múltiples movimientos al día, emparejamos con el que aún no tenga salida asignada
                if ac_merged.arrival < ac_dep.departure_time and ac_merged.destination == "":
                    ac_merged.destination = ac_dep.destination
                    ac_merged.departure_time = ac_dep.departure_time
                    encontrado = True
                    break  # Salimos del bucle interno, ya encontramos su par compatible
            k += 1

        # Si no se ha encontrado ninguna llegada compatible es un "night aircraft"
        if not encontrado:
            night_ac = Aircraft(
                ac_dep.ICAO,
                "",  # Sin origen de llegada hoy
                "",  # Sin hora de llegada hoy
                ac_dep.airline,
                ac_dep.destination,
                ac_dep.departure_time
            )
            merged_list.append(night_ac)

        j += 1

    return merged_list


def NightAircraft(aircrafts):
    if len(aircrafts) == 0:
        return -1

    night_list = []
    i = 0

    while i < len(aircrafts):
        ac = aircrafts[i]

        # Un avión ha pasado la noche en el aeropuerto
        # si su origen y llegada están vacíos
        # pero posee un destino y hora de salida configurados
        if (ac.origin == "" or ac.arrival == "") and ac.destination != "":
            night_list.append(ac)

        i += 1

    return night_list


#test section
aircraft = LoadArrivals("arrivals.txt") # Cargamos los datos del archivo que creamos
PlotArrivals(aircraft) # Llamamos a la función de gráfico
PlotAirlines(aircraft)
PlotFlightsType(aircraft)
MapFlights(aircraft)
print("Probando funcion long distance.")
resultado = LongDistanceArrivals(aircraft)

i = 0
while i < len(resultado):
    print("Avión de larga distancia detectado. Origen:", resultado[i].origin)
    i += 1
print("--- PRUEBA LOAD DEPARTURES ---")
lista_salidas = LoadDepartures("departures.txt")
if len(lista_salidas) > 0:
    print("Ejemplo salida:", lista_salidas[0])
