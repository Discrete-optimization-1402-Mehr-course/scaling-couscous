import sys
from networkx import shortest_path
from handler import FileGraphHandler

def main(osmfile):
    h = FileGraphHandler()
    h.apply_file(osmfile)

    print("Graph: %s" % h.graph)
    print(shortest_path(h.graph, 269147990, 695550988, "distance"))

    return 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python %s <osmfile>" % sys.argv[0])
        sys.exit(-1)

    exit(main(sys.argv[1]))
