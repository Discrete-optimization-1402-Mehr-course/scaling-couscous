from networkx import Graph, add_cycle, add_path
from osmium import Node, Relation, SimpleHandler, Way

from util import distance


class MapGraphHandler(SimpleHandler):
    def __init__(self):
        super().__init__()
        self.map = Graph()
        self.bus_lines = {}
        self.subway_lines = {}
        self.public_stations = []

    def node(self, n: Node):
        self.map.add_node(
            n.id,
            location=n.location,
            name=n.tags.get("name", f"node_{n.id}"),
        )

    def way(self, w: Way):
        if w.is_closed():
            adder = add_cycle
        else:
            adder = add_path

        adder(self.map, (node.ref for node in w.nodes))

    def relation(self, r: Relation):
        match r.tags["type"]:
            case "route":
                match r.tags["route"]:
                    case "bus":
                        self.bus_lines[r.id, r.tags.get("note")] = [
                            n.ref for n in r.members
                        ]

                    case "subway" | "light_rail":
                        self.subway_lines[r.id, r.tags.get("note")] = [
                            n.ref for n in r.members
                        ]

            case "public_transport":
                assert r.tags["public_transport"].startswith("stop_area")

                self.public_stations.append([n.ref for n in r.members])

    def apply_file(self, *args, **kwargs) -> None:
        super().apply_file(*args, **kwargs)
        self._calculate_weights()

    def _calculate_weights(self):
        for edge in self.map.edges:
            fr, to = (self.map.nodes[i]["location"] for i in edge)

            self.map.edges[edge]["distance"] = distance(fr, to)
