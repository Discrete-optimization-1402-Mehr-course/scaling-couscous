import sys

import networkx
from handler import MapGraphHandler
from problem import Problem
from solver import dijkstra_shortest_path_by_time
from helper import pretty_print_route, export_gpx


def main(osmfile, start, end):
    h = MapGraphHandler()
    h.apply_file(osmfile)

    p = Problem(map=h.map, walk_speed=1.5, bus_speed=5, start_node=start, end_node=end)

    if not p.validate():
        print("Could not validate problem!")
        sys.exit(-2)

    time_optimized_route = dijkstra_shortest_path_by_time(p)

    print("route optimized for time:")
    pretty_print_route(p, time_optimized_route)

    filename = f"{start}_{end}.gpx"
    export_gpx(p, time_optimized_route, filename)
    print(f"gpx wrote in {filename}")

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python %s <osmfile> <start> <end>" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1], sys.argv[2], sys.argv[3]))
