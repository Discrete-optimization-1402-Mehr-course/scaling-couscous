from networkx import shortest_path
from problem import Problem
from typing import List


def dijkstra_shortest_path(p: Problem, weight: str) -> List[str]:
    return shortest_path(p.map.city_graph, p.start_node, p.end_node, weight=weight)


def dijkstra_shortest_path_by_time(p: Problem):
    return dijkstra_shortest_path(p, "time")
