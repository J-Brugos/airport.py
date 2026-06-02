import matplotlib.pyplot as plt
from airport import IsSchengenAirport,LoadAirports
import math


class Aircraft:
    def __init__(self, ICAO="", origin="", arrival="", airline="", destination="", departure=""):
        # La V4 guarda datos de llegada y tambien de salida en el mismo avion.
        self.ICAO = ICAO
        self.origin = origin
        self.arrival = arrival
        self.airline = airline
        self.destination = destination
        self.departure = departure

    def __str__(self):
        return f"{self.ICAO} ({self.airline}) | Arr: {self.origin} {self.arrival} | Dep: {self.destination} {self.departure}"


def TimeToMinutes(time):
    # Convierte una hora hh:mm a minutos para poder comparar vuelos facilmente.
    if time == "" or time is None:
        return -1

    parts = str(time).strip().split(":")

    # Si el formato no tiene dos partes, la hora no es valida.
    if len(parts) != 2:
        return -1

    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return -1

    # Controlamos los limites de un dia completo.
    if hour < 0 or hour > 23 or minute < 0 or minute > 59:
        return -1

    return hour * 60 + minute


def LoadArrivals(filename):
    # Lee el archivo de llegadas y devuelve una lista de objetos Aircraft.
    p = []

    try:
        with open(filename, 'r') as f:
            #Saltamos la cabecera que no contiene nada importante
            f.readline()

            linea = f.readline()
            while linea != "":
                datos = linea.strip().split()

                if len(datos) == 4 and TimeToMinutes(datos[2]) != -1:
                    icao = datos[0]
                    origin = datos[1]
                    arrival = datos[2]
                    airline = datos[3]
                    # Creamos el objeto y lo añadimos a la lista
                    vuelo = Aircraft(icao, origin, arrival, airline, "", "")
                    p.append(vuelo)

                linea = f.readline()

    except FileNotFoundError:
        # Si el fichero no existe, retornamos lista vacía
        return []

    return p

def PlotArrivals(aircrafts):
    # Dibuja cuantas llegadas hay en cada hora del dia.
    if len(aircrafts) == 0:
        print("Error: no hay vuelos para mostrar.")
        return -1

    frecuencias = [0] * 24
    i=0
    while i < len(aircrafts):
            minutos = TimeToMinutes(aircrafts[i].arrival)

            if minutos != -1:
                hora = minutos // 60
                frecuencias[hora] += 1

            i = i + 1


    horas = range(24)
    plt.bar(horas, frecuencias, color='turquoise')
    plt.xlabel('Hora del día')
    plt.ylabel('Número de vuelos')
    plt.title('Frecuencia de llegadas')
    plt.show()


def SaveFlights(aircrafts, filename):
    # Guarda la lista de vuelos en el formato de texto pedido por el proyecto.
    if len(aircrafts) == 0:
        return -1

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
    return 0

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

        # Actualizamos la frecuencia o añadimos una nueva aerolinea
        if found:
            frequencies[position] += 1
        else:
            airlines.append(airline)
            frequencies.append(1)

        i += 1

    # Dibujamos el grafico de barras
    plt.bar(airlines, frequencies, color='orange')
    plt.xlabel('Airline')
    plt.ylabel('Number of flights')
    plt.title('Number of flights by airline')
    label_size = 7

    if len(airlines) > 80:
        label_size = 4
    elif len(airlines) > 50:
        label_size = 5
    elif len(airlines) > 30:
        label_size = 6

    plt.xticks(rotation=45, ha="right", fontsize=label_size)
    plt.tight_layout()
    plt.show()

def PlotFlightsType(aircrafts):
    # Compara llegadas Schengen y no Schengen en una grafica apilada.
    if len(aircrafts) == 0:
        print("Error: no hay vuelos para mostrar.")
        return -1

    schengen_count = 0
    non_schengen_count = 0

    # Recorremos la lista de aviones
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

    # Dibujamos la parte de No-Schengen encima, usando el parametro 'bottom' para apilar
    plt.bar("Tipo de Vuelo", non_schengen_count, bottom=schengen_count, color="orange", label="Non-Schengen")

    plt.ylabel("Número de vuelos")
    plt.title("Schengen vs Non-Schengen)")
    plt.legend()
    plt.show()


def PlotArrivalsSchengen(extra):
    # Acepta directamente una lista o un diccionario con la lista de aviones.
    if isinstance(extra, dict):
        aircrafts = extra.get("aircrafts", [])
    else:
        aircrafts = extra

    if not aircrafts:
        print("Error: no arrivals to display.")
        return

    schengen_hours = [0] * 24
    non_schengen_hours = [0] * 24

    i = 0
    while i < len(aircrafts):
        aircraft = aircrafts[i]
        minutes = TimeToMinutes(aircraft.arrival)

        # Separamos cada llegada por hora y por tipo Schengen.
        if aircraft.origin != "" and minutes != -1:
            hour = minutes // 60

            if IsSchengenAirport(aircraft.origin[:2]):
                schengen_hours[hour] += 1
            else:
                non_schengen_hours[hour] += 1

        i += 1

    hours = range(24)
    plt.bar(hours, schengen_hours, color="turquoise", label="Schengen")
    plt.bar(hours, non_schengen_hours, bottom=schengen_hours, color="orange", label="Non-Schengen")
    plt.xlabel("Hour of day")
    plt.ylabel("Number of arrivals")
    plt.title("Arrivals by hour: Schengen / Non-Schengen")
    plt.legend()
    plt.tight_layout()
    plt.show()


def plotschengentimes(extra):
    # Alias pedido para la funcion extra, manteniendo el nombre usado por el proyecto.
    return PlotArrivalsSchengen(extra)


def GetAirportCoordinates(code, lista_airports):
    # Busca un aeropuerto por codigo ICAO y devuelve sus coordenadas.
    i = 0
    while i < len(lista_airports):
        if lista_airports[i].ICAO == code:
            return lista_airports[i].latitude, lista_airports[i].longitude
        i = i + 1


def MapFlights(aircrafts, filename="flights.kml"):
    # Cargamos la base de datos de aeropuertos una sola vez fuera del bucle
    airports_db = LoadAirports("Airports.txt")

    # Creamos o abrimos el archivo KML para escribir el mapa
    f = open(filename, "w")

    # Escribimos la cabecera estándar del archivo KML
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Flights Map</name>\n')
    f.write('  <Style id="schengenFlight">\n')
    f.write('    <LineStyle><color>ff00ff00</color><width>3</width></LineStyle>\n')
    f.write('  </Style>\n')
    f.write('  <Style id="nonSchengenFlight">\n')
    f.write('    <LineStyle><color>ff0000ff</color><width>3</width></LineStyle>\n')
    f.write('  </Style>\n')

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
                if IsSchengenAirport(vuelo.origin[:2]):
                    f.write('    <styleUrl>#schengenFlight</styleUrl>\n')
                else:
                    f.write('    <styleUrl>#nonSchengenFlight</styleUrl>\n')
                f.write('    <LineString>\n')
                f.write('      <altitudeMode>clampToGround</altitudeMode>\n')
                f.write('      <coordinates>\n')
                # En KML primero va la Longitud y luego la Latitud
                f.write(f'        {coords_origen[1]},{coords_origen[0]},0\n')
                f.write(f'        {coords_lebl[1]},{coords_lebl[0]},0\n')
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

    # Convertimos grados a radianes
    phi1 = lat1 * c_rad
    phi2 = lat2 * c_rad
    lam1 = lon1 * c_rad
    lam2 = lon2 * c_rad

    # Calculamos las diferencias de latitud y longitud en radianes
    d_phi = abs(phi1 - phi2)
    d_lam = abs(lam1 - lam2)

    # Calculamos los terminos principales de la formula Haversine
    a = math.sin(d_phi / 2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(d_lam / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    # Distancia final en kilometros
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

        # Control de None: si el aeropuerto de origen no existe, saltamos al siguiente
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
    # Lee el archivo de salidas y crea aviones solo con datos de salida.
    departures_list = []
    try:
        f = open(filename, 'r')
        # Saltamos la cabecera
        f.readline()

        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()
            if len(datos) == 4 and TimeToMinutes(datos[2]) != -1:
                icao = datos[0]  # Identificador del avion
                destination = datos[1]  # Aeropuerto de destino
                departure = datos[2]  # Hora de salida
                airline = datos[3]  # Aerolinea

                # Para salidas puras, origen y llegada se dejan vacios.
                vuelo = Aircraft(icao, "", "", airline, destination, departure)
                departures_list.append(vuelo)

            linea = f.readline()
        f.close()
    except FileNotFoundError:
        return []
    return departures_list


def MergeMovements(arrivals, departures):
    # Une llegadas y salidas compatibles usando el identificador del avion.
    if len(arrivals) == 0 or len(departures) == 0:
        return -1

    merged_list = []
    used_departures = []

    # Primero recorremos las llegadas y buscamos su mejor salida posterior.
    i = 0
    while i < len(arrivals):
        ac_arr = arrivals[i]
        arr_minutes = TimeToMinutes(ac_arr.arrival)

        best_departure_index = -1
        best_departure_minutes = 24 * 60 + 1

        j = 0
        while j < len(departures):
            ac_dep = departures[j]
            dep_minutes = TimeToMinutes(ac_dep.departure)

            used = False
            k = 0
            while k < len(used_departures):
                if used_departures[k] == j:
                    used = True
                k += 1

            # La salida es compatible si es del mismo avion y ocurre despues de la llegada.
            if ac_arr.ICAO == ac_dep.ICAO and not used:
                if arr_minutes != -1 and dep_minutes != -1:
                    if arr_minutes < dep_minutes and dep_minutes < best_departure_minutes:
                        best_departure_index = j
                        best_departure_minutes = dep_minutes

            j += 1

        if best_departure_index != -1:
            ac_dep = departures[best_departure_index]

            new_ac = Aircraft(
                ac_arr.ICAO,
                ac_arr.origin,
                ac_arr.arrival,
                ac_arr.airline,
                ac_dep.destination,
                ac_dep.departure
            )

            merged_list.append(new_ac)
            used_departures.append(best_departure_index)
        else:
            new_ac = Aircraft(
                ac_arr.ICAO,
                ac_arr.origin,
                ac_arr.arrival,
                ac_arr.airline,
                "",
                ""
            )
            merged_list.append(new_ac)

        i += 1

    j = 0
    while j < len(departures):
        used = False

        k = 0
        while k < len(used_departures):
            if used_departures[k] == j:
                used = True
            k += 1

        if not used:
            ac_dep = departures[j]
            # Las salidas no usadas son aviones que ya estaban en Barcelona al empezar el dia.
            night_ac = Aircraft(
                ac_dep.ICAO,
                "",
                "",
                ac_dep.airline,
                ac_dep.destination,
                ac_dep.departure
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
        if ac.origin == "" and ac.arrival == "" and ac.destination != "" and ac.departure != "":
            night_list.append(ac)

        i += 1

    return night_list


def AssignGatesAtTime(bcn, aircrafts, time):
    # Asigna puertas dinamicamente dentro de la hora indicada.
    if len(aircrafts) == 0:
        return -1

    from LEBL import AssignGate
    from LEBL import FreeGate

    start_minutes = TimeToMinutes(time)

    if start_minutes == -1:
        return -1

    end_minutes = start_minutes + 60
    events = []

    # Construimos una lista de eventos de salida y llegada dentro del intervalo.
    i = 0
    while i < len(aircrafts):
        ac = aircrafts[i]
        arrival_minutes = TimeToMinutes(ac.arrival)
        departure_minutes = TimeToMinutes(ac.departure)

        if departure_minutes != -1 and start_minutes <= departure_minutes < end_minutes:
            events.append([departure_minutes, "departure", ac])

        if ac.origin != "" and arrival_minutes != -1 and start_minutes <= arrival_minutes < end_minutes:
            events.append([arrival_minutes, "arrival", ac])

        i += 1

    events.sort(key=lambda event: (event[0], 0 if event[1] == "departure" else 1))

    not_assigned = 0

    # Primero se liberan salidas y luego se asignan llegadas de la misma hora.
    i = 0
    while i < len(events):
        event = events[i]
        ac = event[2]

        if event[1] == "departure":
            FreeGate(bcn, ac.ICAO)
        else:
            result = AssignGate(bcn, ac)

            if result != 0:
                not_assigned += 1

        i += 1

    return not_assigned


def CountTerminalOccupancy(bcn):
    # Cuenta las puertas ocupadas de cada terminal en el estado actual de bcn.
    terminal_counts = []

    t = 0
    while t < len(bcn.terminals):
        terminal = bcn.terminals[t]
        occupied = 0

        a = 0
        while a < len(terminal.boarding_areas):
            area = terminal.boarding_areas[a]

            g = 0
            while g < len(area.gates):
                if area.gates[g].occupied:
                    occupied += 1

                g += 1

            a += 1

        terminal_counts.append(occupied)
        t += 1

    return terminal_counts


def PlotDayOccupancy(bcn, aircrafts):
    # Recorre todo el dia assignando por hora
    if len(aircrafts) == 0:
        return -1

    hours = []
    not_assigned_counts = []
    terminal_counts = []

    t = 0
    while t < len(bcn.terminals):
        terminal_counts.append([])
        t += 1

    hour = 0
    while hour < 24:
        time = f"{hour:02d}:00"
        not_assigned = AssignGatesAtTime(bcn, aircrafts, time)

        # Guardamos los datos de la hora para dibujarlos al final.
        hours.append(hour)
        not_assigned_counts.append(not_assigned)

        counts = CountTerminalOccupancy(bcn)

        t = 0
        while t < len(counts):
            terminal_counts[t].append(counts[t])
            t += 1

        hour += 1

    t = 0
    while t < len(bcn.terminals):
        plt.plot(hours, terminal_counts[t], marker="o", label=bcn.terminals[t].name + " occupied gates")
        t += 1

    plt.bar(hours, not_assigned_counts, alpha=0.35, color="red", label="Unassigned arrivals")
    plt.xlabel("Hour of day")
    plt.ylabel("Number of aircraft / gates")
    plt.title("Gate occupancy during the day")
    plt.xticks(hours)
    plt.legend()
    plt.tight_layout()
    plt.show()

    return not_assigned_counts


if __name__ == "__main__":
    aircraft = LoadArrivals("arrivals.txt")
    departures = LoadDepartures("Departures.txt")

    print("--- VERSION 4 TEST ---")
    print("Arrivals loaded:", len(aircraft))
    print("Departures loaded:", len(departures))

    movements = MergeMovements(aircraft, departures)

    if movements == -1:
        print("MergeMovements error")
    else:
        print("Merged movements:", len(movements))

        night_aircraft = NightAircraft(movements)

        if night_aircraft == -1:
            print("NightAircraft error")
        else:
            print("Night aircraft:", len(night_aircraft))

        try:
            from LEBL import LoadAirportStructure
            from LEBL import AssignNightGates

            bcn = LoadAirportStructure("Terminals.txt")

            if bcn == -1:
                print("LEBL structure could not be loaded.")
            else:
                AssignNightGates(bcn, night_aircraft)
                unassigned = AssignGatesAtTime(bcn, movements, "06:00")
                print("Unassigned arrivals from 06:00 to 06:59:", unassigned)

        except ImportError:
            print("LEBL dynamic gate functions are not available.")
