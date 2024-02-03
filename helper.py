import os
from typing import List
from itertools import pairwise
from problem import Problem
from gpx_converter import Converter


def pretty_print_route(p: Problem, route: List[str]):
    # TODO: print route in a human readable form
    print(route)


def export_gpx(p: Problem, route: List[str], filename: str):
    f = open(f"{filename}.csv", "w")
    f.write("lon,lat\n")
    for r in route:
        lon = p.map.city_graph.nodes[r]["location"].lon
        lat = p.map.city_graph.nodes[r]["location"].lat
        f.write(f"{lon},{lat}\n")
    f.flush()
    Converter(input_file=f"{filename}.csv").csv_to_gpx(
        lats_colname="lat", longs_colname="lon", output_file=filename
    )
    os.remove(f"{filename}.csv")
