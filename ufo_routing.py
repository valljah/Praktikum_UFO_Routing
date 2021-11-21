import itertools

from ufo_autopilot import flight_distance_mult


def fac(m: int = 1, n: int = 1) -> int:
    if m < 0:
        raise ValueError('Die Fakultätsfunktion ist nur für ganze Zahlen > 0 definiert!')
    elif m < 2 or m < n:
        return 1
    elif m == n:
        return m
    return n * fac(m - 1, n + 1) * m


def find_shortest_route(destinations: list) -> list:
    routes = list(itertools.permutations(destinations))
    shortest_route = routes[0]
    for r in routes:
        if flight_distance_mult(r, 1.0) < flight_distance_mult(shortest_route, 1.0):
            shortest_route = r
    return shortest_route
