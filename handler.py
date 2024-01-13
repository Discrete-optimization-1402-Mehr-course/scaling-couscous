from osmium import SimpleHandler, Node, Way
from networkx import Graph
from itertools import pairwise
from util import distance

class FileGraphHandler(SimpleHandler):
    def __init__(self):
        super().__init__()
        self.graph = Graph()

    def node(self, n: Node):
        self.graph.add_node(n.id, location=n.location)

    def way(self, w: Way):
        self.graph.add_edges_from(pairwise(node.ref for node in w.nodes))

        if w.is_closed() and len(w.nodes) > 1:
            self.graph.add_edge(w.nodes[-1].ref, w.nodes[0].ref)

    def apply_file(self, *args, **kwargs) -> None:
        super().apply_file(*args, **kwargs)
        self._calculate_weights()
        
    def _calculate_weights(self):
        graph = self.graph

        for edge in graph.edges:
            fr, to = (self.graph.nodes[i]["location"] for i in edge)

            graph.edges[edge]["distance"] = distance(fr, to)



