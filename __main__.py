import sys

from networkx import shortest_path

from handler import MapGraphHandler


def main(osmfile):
    h = MapGraphHandler()
    h.apply_file(osmfile)

    print("Graph: %s" % h.map.city_graph)
    print(
        [
            h.map.city_graph.nodes[i]["name"]
            for i in shortest_path(h.map.city_graph, 269147990, 695550988, "distance")
        ]
    )

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
