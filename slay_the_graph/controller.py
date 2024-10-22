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


def _get_already_connected(column: List[Node]) -> List[Tuple[Node, Node]]:
    """
    Find the already existing connections in a given column

    @param column: list of nodes representing a column in the Graph
    @return: list of nodes that are connected together
    """
    already_connected: List[Tuple[Node, Node]] = []
    for connected_node in column:
        for connection in (connected_node.connections or []):
            already_connected.append((connected_node, connection))
    return already_connected


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

    already_connected = _get_already_connected(current_column)
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


def _find_valid_backwards_connections(
    node: Node,
    current_column: List[Node],
    previous_column: List[Node],
) -> List[Tuple[int, Node]]:
    """
    Select nodes from the previous column that can connect to the specified node

    @param node: node to connect to
    @param current_column: column that the node belongs to
    @param previous_column: column preceding the one that the node belongs to
    @return: list of viable nodes where a connection can be made, with the
        number of connections the node already has.
    """

    already_connected = _get_already_connected(previous_column)
    proposed_nodes = previous_column[
        max(0, node.location.row-1):min(len(previous_column)-1, node.location.row+1)
    ]
    proposed_connections: List[Tuple[Node, Node]] = []
    for possible_connection in proposed_nodes:
        proposed_connections.append((node, possible_connection))
    unused_connections = list(set(proposed_connections).difference(set(already_connected)))

    viable_nodes: List[Tuple[int, Node]] = []
    for _, possible_node in unused_connections:
        if _does_not_cross(possible_node, node, already_connected):
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

def _pick_connections(
    node: Node,
    current_column: List[Node],
    next_column: List[Node],
    max_connections: Optional[int] = None,
 ) -> List[Node]:
    """
    Select nodes from the next column that are viable to connect to.

    @param node: node to verify
    @param current_column: column of nodes to hook up
    @param next_column: column of nodes that will be hooked up to
    @param num_connections: if specified, maximum number of connections
        to pick.
    @return: list of nodes to add a new connection
    """
    potential_connections = _find_valid_connections(
        node,
        current_column,
        next_column,
    )
    if not potential_connections:
        return []

    num_connections = random.randint(
        1,
        min(max_connections or 1, len(potential_connections)),
    )
    if num_connections < len(potential_connections):
        # We prioritize selection based on the fewest number of connections
        chance_weights: List[int] = []
        for conn, _ in potential_connections:
            chance_weights.append(3 - conn)
        selected_connections = random.choices(
            potential_connections,
            weights=chance_weights,
            k=num_connections,
        )
    else:
        selected_connections = potential_connections

    new_connections: List[Node] = []
    for _, snode in selected_connections:
        new_connections.append(snode)

    return new_connections


def _pick_backwards_connection(
    node: Node,
    current_column: List[Node],
    previous_column: List[Node],
) -> Node:
    """
    Select a single node to create a backwards connection.

    @param node: node that needs a connection
    @param current_column: column that the node belongs to
    @param previous_column: column of nodes that will connect to this node
    @return: node in previous_column that will connect to the node
    """
    potential_connections = _find_valid_backwards_connections(
        node,
        current_column,
        previous_column,
    )
    if len(potential_connections) == 0:
        return None

    if len(potential_connections) == 1:
        return potential_connections[0][1]

    chance_weights: List[int] = []
    for conn, _ in potential_connections:
        chance_weights.append(3 - conn)
    selected_connection = random.choice(
        potential_connections,
        weights=chance_weights,
    )
    return selected_connection[1]


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

            node.connections.extend(
                _pick_connections(
                    node,
                    current_column,
                    next_column,
                ),
            )

    return connected_nodes


def _second_pass_correction(nodes: List[List[Node]]) -> List[List[Node]]:
    """
    Ensure there are no incorrectly-connected nodes

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

        # There must always be a forward connection
        for jdx, row in enumerate(current_column):
            if len(row.connections) == 0:
                new_connections = _pick_connections(
                    row,
                    current_row,
                    next_row,
                    max_connections=1,
                )
                if not new_connections:
                    # Indicates problem in the algorithm and requires a rewrite.
                    # A user should never see this.
                    raise RuntimeError(
                        f"Unable to generate valid forward connection ({idx}, {jdx}): {connected_nodes}"
                    )

                row.connections.extend(new-connections)

        # Now we need to check the backwards connections
        for jdx, row in enumerate(next_column):
            already_connected = _get_already_connected(current_column)
            connected_to_row = list(
                filter(
                    lambda x: x[1] == row,
                    already_connected,
                ),
            )
            if len(connected_to_row) == 0:
                new_connection = _pick_backwards_connection(
                    row,
                    next_column,
                    current_column,
                )
                if not new_connection:
                    # Indicates a problem in the algorithm and requires a rewrite.
                    # A user should never see this.
                    raise RuntimeError(
                        f"Unable to generate valid backward connection ({idx, jdx}): {connected_nodes}"
                    )

                new_connection.connections.append(row)

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
