from networkx import DiGraph, Graph, add_cycle, add_path, subgraph_view
from osmium import Node, Relation, SimpleHandler, Way

from problem import BusLine, PublicStation, PublicTransportationRoute, Map, SubwayLine
from util import distance


class MapGraphHandler(SimpleHandler):
    def __init__(self):
        super().__init__()
        self.map = Map()
        self.ways = {}

    def node(self, n: Node):
        self.map.city_graph.add_node(
            n.id,
            location=n.location,
            name=n.tags.get("name", f"node_{n.id}"),
        )

    def way(self, w: Way):
        if w.is_closed():
            adder = add_cycle
        else:
            adder = add_path

        adder(self.map.city_graph, (node.ref for node in w.nodes), way_id=w.id)

    def relation(self, r: Relation):
        match dict(r.tags):
            case {"type": "route", "route": route}:
                match route:
                    case "bus":
                        self.map.bus_lines.append(BusLine(*self.relation_public_transport(r)))

                    case "subway" | "light_rail":
                        self.map.subway_lines.append(SubwayLine(*self.relation_public_transport(r)))

            case {"type": "public_transport", "public_transport": public_transport}:
                assert public_transport.startswith("stop_area")

                self.map.public_stations.append(
                    PublicStation([n.ref for n in r.members])
                )

    def edge_filter(self, way_ids: set[int]):
        def filter(a: int, b: int):
            return self.map.city_graph.edges[a, b] in way_ids

        return filter

    def relation_public_transport(self, r: Relation):
        route_name = (r.tags.get("ref") or "") + (r.tags.get("name") or "")
        stops = []

        way_ids: set[int] = set()
        for member in r.members:
            match member.type:
                case "n":
                    if member.role.startswith("stop") or member.role.startswith(
                        "platform"
                    ):
                        stops.append(member.ref)
                case "w":
                    way_ids.add(member.ref)

        route = subgraph_view(
            self.map.city_graph, filter_edge=self.edge_filter(way_ids)
        )

        return (route_name, route, stops)

    def apply_file(self, *args, **kwargs) -> None:
        super().apply_file(*args, **kwargs)
        self._calculate_weights()  # TODO: move this to router class

    def _calculate_weights(self):
        for edge in self.map.city_graph.edges:
            fr, to = (self.map.city_graph.nodes[i]["location"] for i in edge)

            self.map.city_graph.edges[edge]["distance"] = distance(fr, to)
