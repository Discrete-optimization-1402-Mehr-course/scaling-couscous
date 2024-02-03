from typing import NamedTuple
from networkx import DiGraph, MultiDiGraph, Graph


class PublicTransportationRoute(NamedTuple):
    route_name: str
    stops: list[int] = []
    id: int = 0


class BusLine(PublicTransportationRoute):
    pass


class SubwayLine(PublicTransportationRoute):
    pass


class PublicStation(NamedTuple):
    nodes: list[int]


class Map(NamedTuple):
    city_graph: DiGraph = DiGraph()
    bus_lines: list[BusLine] = []
    subway_lines: list[SubwayLine] = []
    public_stations: list[PublicStation] = []


class Problem(NamedTuple):
    map: Map

    walk_speed: float
    bus_speed: float

    start_node: str
    end_node: str

    def validate(self):
        return (
            self.start_node in self.map.city_graph.nodes
            and self.end_node in self.map.city_graph.nodes
        )
