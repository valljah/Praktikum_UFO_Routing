from py4j.java_gateway import JavaGateway
from ufo_autopilot import flight_distance_mult, distance_from_zero
from ufo_autopilot import fly_to
from operator import itemgetter

# Initialisierung des Gateways zur Java-Ufo-Simulation
from ufo_routing import fac, find_shortest_route

gateway = JavaGateway()

# In der folgenden Zeile definieren wir eine Referenz auf die Simulation.
sim = gateway.entry_point

# Vor dem Losfliegen die Simulation resetten.
sim.reset()

# Oeffnen einer View, die immer on Top angezeigt wird.
# Die Skalierung ist 10 m pro Pixel.
sim.openViewWindow(True, 10)

# Hier Konsoleingabe des Ziels x, y und der Flughoehe z ergaenzen
z = 20.0
destinations = [(1.0, 0.0), (1.0, 1.0), (0.0, 1.0)]

destinations = find_shortest_route(destinations)
# destinations.sort(key=itemgetter(0))
# destinations.sort(key=distance_from_zero)

for point in destinations:
    sim.addDestination(point[0], point[1])

# Simulationsgeschwindigkeit setzen
sim.setSpeedup(10)

# Meldung auf die Konsole ausgeben und auf Eingabe warten
input("Press return to start...")

# Hier Konsolausgabe der zu fliegenden Distanz ergaenzen
print(round(flight_distance_mult(destinations, z), 2))

# Fliege das Ufo zum Ziel
for point in destinations:
    fly_to(sim, point, z)
fly_to(sim, (0.0, 0.0), z)

# Hier Konsolausgabe der tatsaechlich geflogenen Distanz ergaenzen
print(round(sim.getDist(), 2))
print(f"Es existieren {fac(len(destinations))} verschiedene Routen mit den angegebenen Punkten!")
