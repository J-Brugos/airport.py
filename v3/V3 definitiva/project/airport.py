class Airport:
    def __init__(self, ICAO, latitude, longitude, SCHENGEN):
        self.ICAO = ICAO
        self.latitude = latitude
        self.longitude = longitude
        self.SCHENGEN = SCHENGEN

    def __str__(self):
        return f"{self.ICAO} ({self.latitude}, {self.longitude}) - Schengen: {self.SCHENGEN}"


def IsSchengenAirport (airport):
    schengen = False
    j=0
    list1 = ['LO', 'EB', 'LK', 'LC', 'EK', 'EE', 'EF', 'LF', 'ED', 'LG', 'EH', 'LH',
        'BI','LI', 'EV', 'EY', 'EL', 'LM', 'EN', 'EP', 'LP', 'LZ', 'LJ', 'LE', 'ES',
        'LS']
    while j<len(list1) and not schengen:
        if list1[j] == airport:
            schengen = True
        else:
            j=j+1
    return schengen
def SetSchengen(airport):
    resultat = IsSchengenAirport(airport.ICAO[:2])
    airport.SCHENGEN = resultat

def PrintAirport(airport): #Imprimimos la informacion del aeropuerto
    print(airport.ICAO)
    print(airport.latitude)
    print(airport.longitude)
    print(airport.SCHENGEN)

def converttodegrees(coord):   #convertimos coordenadas de tipo norte, sur, este, oeste a grados
    coord = coord.strip().upper()
    if coord[0] == 'S'or coord[0] =='W':
        sign = -1
    else :
        sign= 1
    coord_num = coord[1:]
    if coord[0] == 'N' or coord[0] == 'S': #lat
        degrees = float(coord_num[0:2])
        minutes = float(coord_num[2:4])
        seconds = float(coord_num[4:])
    else: #lon
        degrees = float(coord_num[0:3])
        minutes = float(coord_num[3:5])
        seconds = float(coord_num[5:])
    decimal = degrees + minutes / 60 + seconds / 3600

    return sign * decimal
def convertfromdegrees (value, is_lat=True): #Al revés que la función anterior
    if value >= 0:
        sign = 'N'
    else:
        sign = 'S'
    if not is_lat:
        if value >= 0:
            sign = 'E'
        else :
            sign ='W'

    value = abs(value)
    degrees = int(value)
    minutes = int((value - degrees) * 60)
    seconds = (value - degrees - minutes/60) * 3600

    if is_lat:
        return f"{sign}{degrees:02d}{minutes:02d}{seconds:05.2f}"
    else:
        return f"{sign}{degrees:03d}{minutes:02d}{seconds:05.2f}"


def LoadAirports(filename):
    airports_list = []
    try:
        f = open(filename, 'r')

        # Saltamos la cabecera (La primera línea del fichero que contiene "AIRPORTS")
        f.readline()

        linea = f.readline()
        while linea != "":
            datos = linea.strip().split()

            # Solo procesamos si la línea tiene los datos mínimos requeridos
            if len(datos) >= 4:
                # Extraemos los datos según la estructura de tu archivo
                icao = datos[0]
                latitude = converttodegrees(datos[1])
                longitude = converttodegrees(datos[2])

                # Volvemos a juntar el nombre del aeropuerto por si tiene espacios
                nombre = ""
                k = 3
                while k < len(datos):
                    nombre += datos[k] + " "
                    k += 1
                nombre = nombre.strip()

                # Creamos el objeto de tipo Airport y lo añadimos

                nuevo_aeropuerto = Airport(icao, latitude, longitude, nombre)
                airports_list.append(nuevo_aeropuerto)

            linea = f.readline()
        f.close()
    except FileNotFoundError:
        return []
    return airports_list

def SaveSchengenAirports(airports, filename): #Gaurda solo los aeropuertos Schengen
    try:
        schengen_airports = []

        for airport in airports:
            SetSchengen(airport)  # ← Añadimos el elemento booleano Schengen
            if airport.SCHENGEN:
                schengen_airports.append(airport)

        with open(filename, 'w') as f:  #esto sirve para añadirlo al fichero
                                    # el cual queremos que se indique los aerpuertos shengen
            for airport in schengen_airports:
                lat = convertfromdegrees(airport.latitude, is_lat=True)
                lon = convertfromdegrees(airport.longitude, is_lat=False)
                f.write(f"{airport.ICAO} {lat} {lon}\n")

    except Exception:
        return -1  # error general

def AddAirport(airports, airport):
    i = 0
    found = False
    while i < len(airports) and not found:
        if airports[i].ICAO == airport.ICAO:
            found = True
        else:
            i += 1

    if not found:
        airports.append(airport)

def RemoveAirport(airports, code):
    i = 0
    found = False
    while i < len(airports) and not found:     # Buscamos el aeropuerto
        if airports[i].ICAO == code:
            found = True
        else:
            i += 1

    # Desplazmos elementos hacia la izquierda
    while i < (len(airports) - 1):
        airports[i] = airports[i + 1]
        i += 1

    del airports[-1]  # Eliminamos el último elemento duplicado, usamos "del" porque el 0 al final podria dar problemas para comprobar.


def PlotAirports(airports):
    import matplotlib.pyplot as pyplot

    schengen_count = 0
    not_schengen_count = 0
    i = 0

    while i < len(airports):
        airport = airports[i]

        if airport.SCHENGEN == True:
            schengen_count += 1
        else:
            not_schengen_count += 1

        i += 1

    pyplot.bar(["Airports"], [schengen_count])
    pyplot.bar(["Airports"], [not_schengen_count], bottom=[schengen_count])

    pyplot.title("Schengen airports")
    pyplot.ylabel("Count")

    pyplot.show()

def MapAirports(airports, filename="airports.kml"):
    f = open(filename, 'w')

    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write('<kml xmlns="http://www.opengis.net/kml/2.2">\n')
    f.write('<Document>\n')
    f.write('  <name>Airports Map</name>\n')

    for a in airports:

        if a.SCHENGEN == True:
            color = "ff0000ff"
        else:
            color = "ffff0000"

        #Escribimos la "chincheta" (Placemark) para cada aeropuerto de la lista.
        f.write('  <Placemark>\n')
        f.write('    <name>' + a.ICAO + '</name>\n')
        f.write('    <Style>\n')
        f.write('      <IconStyle>\n')
        f.write('        <color>' + color + '</color>\n')
        f.write('      </IconStyle>\n')
        f.write('    </Style>\n')
        f.write('    <Point>\n')

        f.write('      <coordinates>' + str(a.longitude) + ',' + str(a.latitude) + ',0</coordinates>\n')
        f.write('    </Point>\n')
        f.write('  </Placemark>\n')

    f.write('</Document>\n')
    f.write('</kml>\n')
    f.close()
    print(f"Archivo {filename} generado. Ábrelo con Google Earth.")


