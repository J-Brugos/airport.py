
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

def PrintAirport(airport):
    print(airport.ICAO)
    print(airport.latitude)
    print(airport.longitude)
    print(airport.SCHENGEN)

def converttodegrees(coord):
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
def convertfromdegrees (value, is_lat=True):
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

def LoadAirports (filename):
    p = []

    with open (filename, 'r') as f:
        for linea in f:
            datos = linea.strip().split()
            ICAO = datos[0]
            latitude = converttodegrees((datos[1]))
            longitude = converttodegrees(datos[2])
            airport = Airport(ICAO,latitude,longitude,SCHENGEN= False)
            p.append(airport)
    return p

def SaveSchengenAirports(airports, filename):
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

