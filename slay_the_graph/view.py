"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

from typing import List, Tuple

import igraph
from matplotlib import pyplot

from .model import Graph


def display_graph(graph: Graph):
    vertices = graph.flatten_nodes()
    num_vertices = len(vertices)
    edges: List[Tuple[int, int]] = []
    for vertex in vertices:
        for connection in (vertex.connections or []):
            edges.append((vertex.id, connection.id))

    ig = igraph.Graph(num_vertices, edges)

    fig, ax = pyplot.subplots(figsize=(5,5))
    igraph.plot(
        ig,
        target=ax,
        layout="sugiyama",
        vertex_size=30,
        vertex_color=["steelblue" for vertex in vertices],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        vertex_label=[vertex.name for vertex in vertices],
        vertex_label_size=7.0,
        edge_color=["#7142cf" for vertex in vertices],
    )

    pyplot.show()
