"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

from .model import Graph, Location, Node


def generate_graph():
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
    return graph
