from osmium import Node, Relation, SimpleHandler, Way

from problem import BusLine, PublicStation, Map, SubwayLine
from util import distance, addEdges
from itertools import pairwise


class MapGraphHandler(SimpleHandler):
    def __init__(self):
        super().__init__()
        self.map = Map()
        self.ways = {}

    def node(self, n: Node):
        self.map.city_graph.add_node(
            str(n.id),
            location=n.location,
            name=n.tags.get("name", f"node_{n.id}"),
        )

    def way(self, w: Way):
        w_nodes = [str(node.ref) for node in w.nodes]

        addEdges(
            self.map.city_graph,
            w_nodes,
            1.42,
            reversed=True,
            data={"route_name": "foot", "cost": 0},
        )

    def relation(self, r: Relation):
        match dict(r.tags):
            case {"type": "route", "route": route}:
                match route:
                    case "bus":
                        self.map.bus_lines.append(
                            BusLine(*self.relation_public_transport(r))
                        )

                    case "subway" | "light_rail":
                        self.map.subway_lines.append(
                            SubwayLine(*self.relation_public_transport(r))
                        )

            case {"type": "public_transport", "public_transport": public_transport}:
                assert public_transport.startswith("stop_area")

                self.map.public_stations.append(
                    PublicStation([n.ref for n in r.members])
                )

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

        return (route_name, stops, r.tags.get("ref") or 0)

    def apply_file(self, *args, **kwargs) -> None:
        super().apply_file(*args, **kwargs)
        stops = {}
        for b in self.map.bus_lines:
            for s in b.stops:
                if str(s) in stops:
                    stops[str(s)].append(b)
                else:
                    stops[str(s)] = [b]

        for k, _v in stops.items():
            if not k in self.map.city_graph.nodes:
                continue
            original_node = self.map.city_graph.nodes[k]
            for v in _v:
                self.map.city_graph.add_node(
                    f"{k}_{v.id}",
                    location=original_node["location"],
                    name=f"{original_node['name']}_{v.id}",
                )
                self.map.city_graph.add_edge(f"{k}_{v.id}", k, time=0, cost=0)
                self.map.city_graph.add_edge(k, f"{k}_{v.id}", time=600, cost=1200)
            for i, j in pairwise(_v):
                self.map.city_graph.add_edge(
                    f"{k}_{i.id}", f"{k}_{j.id}", time=600, cost=1200
                )
                self.map.city_graph.add_edge(
                    f"{k}_{j.id}", f"{k}_{i.id}", time=600, cost=1200
                )

        for b in self.map.bus_lines:
            new_stops = [f"{s}_{b.id}" for s in b.stops]
            addEdges(
                self.map.city_graph,
                new_stops,
                5,
                reversed=True,
                data={"route_name": b.route_name, "cost": 0},
            )
