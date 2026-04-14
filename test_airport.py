from project.airport import Airport, SetSchengen, PrintAirport, LoadAirports

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
