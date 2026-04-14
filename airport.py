
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

def convert(coord):
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

def LoadAirports (filename):
    p = []

    with open (filename, 'r') as f:
        for linea in f:
            datos = linea.strip().split()
            ICAO = datos[0]
            latitude = convert((datos[1]))
            longitude = convert(datos[2])
            airport = Airport(ICAO,latitude,longitude,SCHENGEN= False)
            p.append(airport)
    return p


