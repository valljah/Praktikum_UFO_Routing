from itertools import pairwise
from math import sqrt, acos, pi
import time


def fly_to(sim, p: tuple, z: float) -> None:
    print(f"{'t':>3}{'x':>11}{'y':>7}{'z':>7}  ")
    takeoff(sim, z)
    cruise(sim, p)
    landing(sim)


def takeoff(sim, z: float) -> None:
    # Das Ufo fliegt senkrecht nach oben mit 10 km/h.
    sim.setI(90)
    sim.requestDeltaV(10)
    print(format_flight_data(sim))

    # Rechtzeitig vor dem Erreichen der Zielhoehe, bremst das Ufo auf 1 km/h.
    while sim.getZ() < z - 2:
        time.sleep(0.05)
        print(format_flight_data(sim))
    sim.requestDeltaV(-9)
    print(format_flight_data(sim))

    # Wenn das Ufo ganz nahe dran ist, stoppt es und richtet sich horizontal aus.
    while sim.getZ() < z - 0.05:
        time.sleep(0.05)
        print(format_flight_data(sim))
    sim.requestDeltaV(-1)
    sim.setI(0)
    print(format_flight_data(sim))


def cruise(sim, p: tuple) -> None:
    # Das Ufo ist in der aktuellen Position gestartet.
    fro_p = (sim.getX(), sim.getY())
    print(format_flight_data(sim))

    # Weiter geht es in Richtung Ziel. Die zu fliegende Distanz ist dist.
    sim.setD(int(angle(fro_p, p)))
    dist = sim.getDist() + distance(fro_p, p)
    print(format_flight_data(sim))

    # Das Ufo beschleunigt auf 15 km/h.
    sim.requestDeltaV(15)
    print(format_flight_data(sim))

    # Wenn der Abstand zum Ziel 4m ist, bremst das Ufo auf 1 km/h.
    while dist - sim.getDist() > 4:
        time.sleep(0.05)
        print(format_flight_data(sim))
    sim.requestDeltaV(-14)
    print(format_flight_data(sim))

    # Wenn der Abstand zum Ziel 0.05m ist, stoppt das Ufo.
    while dist - sim.getDist() > 0.05:
        time.sleep(0.05)
        print(format_flight_data(sim))
    sim.requestDeltaV(-1)
    print(format_flight_data(sim))


def landing(sim) -> None:
    # Das Ufo fliegt senkrecht nach unten mit 10 km/h.
    sim.setI(-90)
    sim.requestDeltaV(10)
    print(format_flight_data(sim))

    # Wenn die Hoehe 3m erreicht, bremst das Ufo auf 1 km/h.
    while sim.getZ() > 3:
        time.sleep(0.05)
        print(format_flight_data(sim))
    sim.requestDeltaV(-9)
    print(format_flight_data(sim))

    # Das Ufo ist gelandet, wenn die Hoehe kleiner gleich 0 ist.
    while sim.getZ() > 0:
        time.sleep(0.05)
        print(format_flight_data(sim))


def distance(p1: tuple, p2: tuple) -> float:
    return sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)


def distance_from_zero(p: tuple) -> float:
    return distance((0.0, 0.0), p)


def angle(p1: tuple, p2: tuple) -> float:
    # p2[0] = x2, p1[0] = x1
    scalar_product_h1_h2 = 10 * (p2[0] - p1[0])
    length_h1 = 10
    length_h2 = distance(p1, p2)
    phi = 0.0
    if not (length_h2 * length_h1 == 0):
        cos_phi = scalar_product_h1_h2 / (length_h1 * length_h2)
        phi = acos(cos_phi) * 180 / pi
        # p2[1] = y2, p1[1] = y1
        if phi != 180 and p2[1] < p1[1]:
            phi = 360 - phi
    return phi


def flight_distance(p1: tuple, p2: tuple, z: float) -> float:
    return 2 * z + distance(p1, p2)


def flight_distance_mult(destinations: list, z: float) -> float:
    result = flight_distance((0.0, 0.0), destinations[0], z)
    for p1, p2 in pairwise(destinations):
        result += flight_distance(p1, p2, z)
    result += flight_distance(destinations[-1], (0.0, 0.0), z)
    return result


def format_flight_data(sim) -> str:
    t, x, y, z = sim.getTime(), sim.getX(), sim.getY(), sim.getZ()
    return f"{t:>4.1f} s: [{x:>6.1f}{y:>7.1f}{z:>7.1f}]"
