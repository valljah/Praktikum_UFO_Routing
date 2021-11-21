import math
from py4j.java_gateway import JavaGateway
from ufo_autopilot import distance
from ufo_autopilot import distance_from_zero
from ufo_autopilot import angle
from ufo_autopilot import flight_distance
from ufo_autopilot import flight_distance_mult
from ufo_autopilot import fly_to
from ufo_autopilot import format_flight_data
from ufo_autopilot import takeoff
from ufo_autopilot import cruise
from ufo_autopilot import landing
from ufo_routing import fac
from ufo_routing import find_shortest_route

# Globale Variablen
test = 0
ergebnis = ""

# Funktionen zur Testauswertung
def assertEqual(ist, soll, msg=""):
    global test
    global ergebnis
    test = test + 1
    if ist != soll:
        ergebnis = ergebnis + "\n" + msg + " IST " + str(ist) + " SOLL " + str(soll)

def assertAlmostEqual(ist, soll, delta, msg=""):
    global test
    global ergebnis
    test = test + 1
    if abs(ist - soll) > delta:
        ergebnis = ergebnis + "\n" + msg + " IST " + str(ist) + " SOLL " + str(soll)

def assertNotEqual(ist, soll, msg=""):
    global test
    global ergebnis
    test = test + 1
    if ist == soll:
        ergebnis = ergebnis + "\n" + msg + " IST " + str(ist) + " SOLL ungleich " + str(soll)

# Initialisierung der Ufo-Simulation
gateway = JavaGateway()
sim = gateway.entry_point
sim.setSpeedup(20)

# Tests
assertAlmostEqual(distance((1.0, 1.0), (0.0, 2.0)), math.sqrt(2.0), 1e-3, "distance((1.0, 1.0), (0.0, 2.0))")
assertAlmostEqual(distance_from_zero((1.0, -2.0)), math.sqrt(5.0), 1e-3, "distance_from_zero((1.0, -2.0))")
assertAlmostEqual(angle((1.0, 1.0), (2.0, 0.0)), 315.0, 1e-3, "angle((1.0, 1.0), (2.0, 0.0))")
assertAlmostEqual(flight_distance((1.0, 1.0), (0.0, 2.0), 10.0), math.sqrt(2.0)+20.0, 1e-3, "flight_distance((1.0, 1.0), (0.0, 2.0), 10.0)")
assertAlmostEqual(flight_distance_mult([(20.0, 20.0), (20.0, 0.0)], 10.0), math.sqrt(800.0)+100.0, 1e-3, "flight_distance_mult([(20.0, 20.0), (20.0, 0.0)], 10.0)")

sim.reset()
format_flight_data(sim)

sim.reset()
fly_to(sim, (20.0, 20.0), 10.0)
assertAlmostEqual(sim.getX(), 20.0, 1.0, "nach fly_to(sim, (20.0, 20.0), 10.0): sim.getX()")
assertAlmostEqual(sim.getY(), 20.0, 1.0, "nach fly_to(sim, (20.0, 20.0), 10.0): sim.getY()")
assertAlmostEqual(sim.getZ(), 0.0, 0.1, "nach fly_to(sim, (20.0, 20.0), 10.0): sim.getZ()")

sim.reset()
takeoff(sim, 10.0)
cruise(sim, (20.0, 20.0))
landing(sim)
assertAlmostEqual(sim.getX(), 20.0, 1.0, "nach takeoff(sim, 10.0), cruise(sim, (20.0, 20.0)), landing(sim): sim.getX()")
assertAlmostEqual(sim.getY(), 20.0, 1.0, "nach takeoff(sim, 10.0), cruise(sim, (20.0, 20.0)), landing(sim): sim.getY()")
assertAlmostEqual(sim.getZ(), 0.0, 0.1, "nach takeoff(sim, 10.0), cruise(sim, (20.0, 20.0)), landing(sim): sim.getZ()")

sim.reset()
fly_to(sim, (10.0, 0.0), 10)
assertAlmostEqual(sim.getX(), 10.0, 1.0, "nach fly_to(sim, (10.0, 0.0), 10): sim.getX()")
assertAlmostEqual(sim.getY(), 0.0, 1.0, "nach fly_to(sim, (10.0, 0.0), 10): sim.getY()")
assertAlmostEqual(sim.getZ(), 0.0, 0.1, "nach fly_to(sim, (10.0, 0.0), 10): sim.getZ()")

assertEqual(fac(5,3), 60, "fac(5,3)")
assertEqual(fac(4), 24, "fac(4)")

destinations = [(55.0, 20.0), (-116.5, 95.0), (-10.0, -40.0), (-115.0, 95.0)]
assertAlmostEqual(flight_distance_mult(find_shortest_route(destinations), 10.0), 559.0149, 1e-3, "flight_distance_mult(find_shortest_route(destinations), 10.0)")
assertAlmostEqual(flight_distance_mult(find_shortest_route([(0.0, 10.0)]), 0.0), 20.0, 1e-3, "flight_distance_mult(find_shortest_route([(0.0, 10.0)]), 0.0)")

# Ausgabe des Testergebnisses
print()
print("Es wurden", test, "Tests ausgefuehrt. ", end="")
if ergebnis == "":
    print("OK.")
else:
    print(ergebnis)
