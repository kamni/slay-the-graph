"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

import copy
import random
from typing import List, Optional, Tuple

from .model import Graph, Location, Node


def _populate_nodes(num_columns: int) -> List[List[Node]]:
    """
    Randomly generate unconnected nodes for the graph

    @param num_columns: integer representing the number of additional columns.
    @return: list of list of Nodes. Each list represents a column in the graph.
    """

    nodes: List[List[Node]] = []

    first_row: List[Node] = []
    for idx in range(3):
        first_row.append(
            Node(
                id=idx,
                location=Location(column=0, row=idx),
            ),
         )
    nodes.append(first_row)

    id_counter = 3
    # TODO: implement intermediate rows
    # increment id_counter
    # one less than specified rows (second-to-last-row isn't randomly generated)
    # intermediate node should be 2

    second_to_last_row: List[Node] = []
    for idx in range(2):
        second_to_last_row.append(
            Node(
                id=id_counter + idx,
                location=Location(column=len(nodes), row=idx),
            ),
        )
    id_counter += 2
    nodes.append(second_to_last_row)

    last_row = [
        Node(
            id=id_counter,
            location=Location(column=len(nodes), row=0),
        ),
    ]
    nodes.append(last_row)

    return nodes


def _does_not_cross(
    node: Node,
    possible_connection: Node,
    already_connected: List[Tuple[Node, Node]]
) -> bool:
    cross_points = list(
        filter(
            lambda x: (
                (
                    x[0].location.row > node.location.row
                    and x[1].location.row < possible_connection.location.row
                )
                or
                (
                    x[0].location.row < node.location.row
                    and x[1].location.row > possible_connection.location.row
                )
            ),
            already_connected,
        ),
    )
    return len(cross_points) == 0


def _find_valid_connections(
    node: Node,
    current_column: List[Node],
    next_column: List[Node]
) -> List[Tuple[int, Node]]:
    """
    Select nodes from the next column that are viable to connect to.

    @param node: node to verify
    @param current_column: column of nodes to hook up
    @param next_column: column of nodes that will be hooked up to
    @return: list of viable nodes where a connection can be made, with the
        number of connections the node already has.
    """

    # This are always fixed, to avoid weird graphs
    if len(current_column) == 2 and len(next_column) == 4:
        if node.location.row == 0:
            return [next_column[0], next_column[1]]
        else:
            return [next_column[2], next_column[3]]
    if len(current_column) == 4 and len(next_column) == 2:
        if node.location.row in (0, 1):
            return [next_column[0]]
        else:
            return [next_column[1]]

    already_connected: List[Tuple[Node, Node]] = []
    for connected_node in current_column:
        for connection in (connected_node.connections or []):
            already_connected.append((connected_node, connection))
    proposed_nodes = next_column[
        max(0, node.location.row-1):min(len(next_column)-1, node.location.row+1)
    ]
    proposed_connections: List[Tuple[Node, Node]] = []
    for possible_connection in proposed_nodes:
        proposed_connections.append((node, possible_connection))
    unused_connections = list(set(proposed_connections).difference(set(already_connected)))

    viable_nodes: List[Tuple[int, Node]] = []
    for _, possible_node in unused_connections:
        if _does_not_cross(node, possible_node, already_connected):
            num_connections = len(
                list(
                    filter(
                        lambda x: x[0] == possible_node,
                        already_connected,
                    ),
                ),
            )
            viable_nodes.append((num_connections, possible_node))
    return viable_nodes


def _first_pass_hookup(nodes: List[List[Node]]) -> List[List[Node]]:
    """
    Randomly hook the nodes up.
    This may generate an incorrect graph, but should be corrected in a
    subsequent step

    @param nodes: output from _populate_nodes()
    @return: list of list of Nodes
    """

    connected_nodes = copy.deepcopy(nodes)

    next_column: Optional[List[Node]] = None
    for idx, column in enumerate(nodes):
        if idx == len(connected_nodes) - 1:
            break

        if not next_column:
            current_column = connected_nodes[idx]
        else:
            current_column = next_column
        next_column = connected_nodes[idx+1]

        for jdx, node in enumerate(current_column):
            if not node.connections:
                node.connections = []

            if jdx == 0:
                node.connections.append(next_column[0])
            elif jdx == len(current_column) - 1:
                node.connections.append(next_column[len(next_column)-1])

            potential_connections = _find_valid_connections(
                node,
                current_column,
                next_column,
            )
            if not potential_connections:
                continue

            try:
                num_connections = random.randint(1, len(potential_connections))
            except:
                import pdb; pdb.set_trace()
            # We prioritize selection based on the fewest number of connections
            chance_weights: List[int] = []
            for conn, _ in potential_connections:
                chance_weights.append(3 - conn)
            selected_connections = random.choices(
                potential_connections,
                weights=chance_weights,
                k=num_connections,
            )
            for _, snode in selected_connections:
                node.connections.append(snode)

    return connected_nodes


def _second_pass_correction(nodes: List[List[Node]]) -> List[List[Node]]:
    connected_nodes = copy.deepcopy(nodes)
    return connected_nodes


def generate_graph(num_columns: Optional[int] = 0) -> Graph:
    """
    Randomly generate a directed graph.

    @param num_columns: integer representing the number of additional columns.
        If num_columns is 0, returns a first and last column.
    @return: directed graph
    """
    graph = Graph(nodes=[])
    base_nodes = _populate_nodes(num_columns)
    first_pass = _first_pass_hookup(base_nodes)
    final_pass = _second_pass_correction(first_pass)
    graph.nodes = final_pass
    return graph
