from typing import NamedTuple
from networkx import DiGraph, Graph


class PublicTransportationRoute(NamedTuple):
    route_name: str
    route: DiGraph = DiGraph()
    stops: list[int] = []

class BusLine(PublicTransportationRoute):
    pass

class SubwayLine(PublicTransportationRoute):
    pass

class PublicStation(NamedTuple):
    nodes: list[int]


class Map(NamedTuple):
    city_graph: Graph = DiGraph()
    bus_lines: list[BusLine] = []
    subway_lines: list[SubwayLine] = []
    public_stations: list[PublicStation] = []

class Problem(NamedTuple):
    map: Map

    walk_speed: int
    bus_speed: int
    subway_speed: int

    start_node: int
    end_node: int
