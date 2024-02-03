from osmium.osm import Location
from networkx import MultiDiGraph
from typing import List, Dict
from haversine import haversine


def distance(a: Location, b: Location):
    return haversine(a.lat, a.lon, b.lat, b.lon)


def addEdges(
    G: MultiDiGraph,
    path: List[int | str],
    multiplier: float,
    reversed: bool = False,
    data: Dict = {},
):
    for i in range(len(path) - 1):
        # if path[i] == "8900421469_98.1":
        # breakpoint()
        if path[i] in G.nodes and path[i + 1] in G.nodes:
            n1 = G.nodes[path[i]]
            n2 = G.nodes[path[i + 1]]
            d = distance(n1["location"], n2["location"])
            data["time"] = d / multiplier

            G.add_edge(path[i], path[i + 1], **data)

            if reversed:
                G.add_edge(path[i + 1], path[i], **data)
        # else:
        #     print(path[i])
        #     print(path[i+1])
