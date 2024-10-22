"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

from .model import Graph, Location, Node

import igraph
from matplotlib import pyplot


def display_graph():
    graph = Graph(
        nodes=[
            [
                Node(
                    id=0,
                    location=Location(column=0, row=0),
                    connections=[
                        Node(id=1, location=Location(column=1, row=0)),
                        Node(id=2, location=Location(column=1, row=1)),
                    ],
                ),
            ],
            [
                Node(
                    id=1,
                    location=Location(column=1, row=0),
                    connections=[Node(id=3, location=Location(column=2, row=0))],
                ),
                Node(
                    id=2,
                    location=Location(column=1, row=1),
                    connections=[Node(id=3, location=Location(column=2, row=0))],
                ),
            ],
            [
                Node(
                    id=3,
                    location=Location(column=2, row=0),
                    connections=[],
                ),
            ],
        ],
    )

    vertices = graph.flatten_nodes()
    num_vertices = len(vertices)
    edges = [
        (node.id, connection.id)
        for node in vertices
        for connection in node.connections
    ]
    for node in vertices:
        for connection in node.connections:
            print((node.id, connection.id))

    g = igraph.Graph(num_vertices, edges)

    fig, ax = pyplot.subplots(figsize=(5,5))
    igraph.plot(
        g,
        target=ax,
        layout="sugiyama", # print nodes in a circular layout
        vertex_size=30,
        vertex_color=["steelblue" for vertex in vertices],
        vertex_frame_width=4.0,
        vertex_frame_color="white",
        vertex_label=[f"{node.location.column}, {node.location.row}" for node in vertices],
        vertex_label_size=7.0,
        edge_color=["#7142cf" for vertex in vertices],
    )

    pyplot.show()
