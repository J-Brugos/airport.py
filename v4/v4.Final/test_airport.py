from project.airport import Airport, SetSchengen, PrintAirport, LoadAirports, MapAirports, RemoveAirport, AddAirport, PlotAirports
from project.aircraft import LoadArrivals, PlotArrivals
airport = Airport('LEBL', 41.297445, 2.0832941, None)
SetSchengen(airport)
PrintAirport(airport)

print("Testing Barcelona...")
airport1 = Airport("LEBL", 41.297445, 2.0832941, None)
SetSchengen(airport1)
PrintAirport(airport1)

print("Testing London Heathrow...")
airport2 = Airport("EGLL", 51.470020, -0.454295,None )
SetSchengen(airport2)
PrintAirport(airport2)

print("Testing New York JFK...")
airport3 = Airport("KJFK", 40.641311, -73.778139, None)
SetSchengen(airport3)
PrintAirport(airport3)

resultado = LoadAirports("Airports")
for line in resultado:
    SetSchengen(line)
    PrintAirport(line)
    print('\n')

MapAirports(resultado, "Mapa_Aeropuertos.kml")

lista_vuelos = LoadArrivals("arrivals.txt") # Cargamos los datos del archivo que creamos
PlotArrivals(lista_vuelos) # Llamamos a la función de gráfico

print("\n--- TEST: Comprobando AddAirport y RemoveAirport ---")

lista_airports = LoadAirports("Airports")
longitud_inicial = len(lista_airports)
print(f"Longitud inicial: {longitud_inicial}")

# Creamos un aeropuerto ficticio para añadir
nuevo_aeropuerto = Airport("TEST", 0.0, 0.0, True)

print("Añadiendo aeropuerto TEST...")
AddAirport(lista_airports, nuevo_aeropuerto)
for line in lista_airports:
    SetSchengen(line)
    PrintAirport(line)
    print('\n')
print("Eliminando aeropuerto TEST...")
RemoveAirport(lista_airports, "TEST")
for line in lista_airports:
    SetSchengen(line)
    PrintAirport(line)
    print('\n')

PlotAirports(resultado)



