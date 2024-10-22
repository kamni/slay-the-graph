"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

from typing import List, Optional

from pydantic import BaseModel


class Location(BaseModel):
    """
    Location of a Node in a directed graph.
    """

    column: int
    row: int


class Node(BaseModel):
    """
    A node on the directed graph.
    """

    id: int
    location: Location
    connections: Optional[List['Node']] = None

    @property
    def name(self):
        return f"{self.location.column}, {self.location.row}"


class Graph(BaseModel):
    """
    Directed graph that the player will navigate
    """

    nodes: List[List[Node]]

    def flatten_nodes(self):
        vertices: List[Node] = []
        for column in self.nodes:
            for row in column:
                vertices.append(row)
        return vertices
