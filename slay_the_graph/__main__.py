"""
SPDX-FileCopyrightText: J Leadbetter <j@jleadbetter.com>
SPDX-License-Identifier: MIT
"""

from .controller import generate_graph
from .view import display_graph


if __name__ == '__main__':
    graph = generate_graph(2)
    display_graph(graph)
    import pdb; pdb.set_trace()
