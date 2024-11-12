# Copyright (C) 2023-present The Project Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import pytest
from dataclasses import dataclass
from typing import List
from typing import Optional
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.patches import Rectangle
from cl.runtime.context.testing_context import TestingContext
from cl.runtime.testing.pytest.pytest_fixtures import local_dir_fixture


def test_smoke(local_dir_fixture):
    with TestingContext() as context:

        @dataclass
        class Node:
            title: str
            successors: Optional[List["Node"]] = None

        # Define the nodes with successors
        staff_a = Node(title="Staff A")
        staff_b = Node(title="Staff B")
        staff_c = Node(title="Staff C")
        staff_d = Node(title="Staff D")
        team_1 = Node(title="Team A Lead", successors=[staff_a, staff_b])
        team_2 = Node(title="Team B Lead", successors=[staff_c, staff_d])
        ceo = Node(title="CEO", successors=[team_1, team_2])

        # Create a directed graph
        G = nx.DiGraph()

        # Initialize position dictionary and label dictionary
        pos = {}
        labels = {}

        # Starting coordinates for the CEO
        x_start = 10
        y_start = 10
        x_offset = 6  # Horizontal distance between nodes
        y_offset = 2  # Vertical distance between each successor

        current_y = 0

        # Function to recursively add nodes and edges to the graph
        def add_nodes_recursive(graph, node, current_id, x, y, pos, labels) -> int:
            # Add the current node to the graph
            graph.add_node(current_id)
            pos[current_id] = (x, y)
            labels[current_id] = node.title

            # Add successors recursively
            if node.successors:
                for i, successor in enumerate(node.successors):
                    successor_id = len(pos)  # Create a new unique ID for each successor
                    # Add edge from the current node to the successor
                    graph.add_edge(current_id, successor_id)
                    # Position each successor progressively lower
                    y = y - (i + 1) * y_offset  # Adjust vertical spacing between successors
                    y = add_nodes_recursive(
                        graph, successor, successor_id, x + x_offset, y, pos, labels
                    )  # Adjust horizontal spacing
            return y

        # Add CEO node and its successors recursively
        add_nodes_recursive(G, ceo, 0, x_start, y_start, pos, labels)

        # Increase the canvas size using figsize (width, height in inches)
        fig, ax = plt.subplots(figsize=(12, 8))  # Adjust this to make the canvas bigger

        # Define a function to manually position the arrows
        def draw_edges_with_custom_arrows(graph, pos, ax):
            for edge in graph.edges():
                start_node, end_node = edge

                # Get the positions of the nodes
                start_x, start_y = pos[start_node]
                end_x, end_y = pos[end_node]

                # Define the exit point (right of the start node) and entry point (left of the end node)
                exit_x = start_x + 1.5  # Right side of the start node (assuming box width of 3)
                entry_x = end_x - 1.5  # Left side of the end node (assuming box width of 3)

                # Draw the arrow
                ax.annotate(
                    "",
                    xy=(entry_x, end_y),
                    xytext=(exit_x, start_y),
                    arrowprops=dict(
                        arrowstyle="-|>", lw=1.5, color="black", connectionstyle="arc3,rad=0.0"
                    ),  # Straight arrow
                )

        # Call the function to draw custom arrows
        draw_edges_with_custom_arrows(G, pos, ax)

        # Draw the labels
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black")

        # Manually draw boxes (rectangles) around the nodes
        for node, (x, y) in pos.items():
            # Define the size of each box (width and height can be adjusted)
            width = 3
            height = 1.5
            # Draw a rectangle centered on the node's position
            rect = Rectangle(
                (x - width / 2, y - height / 2), width, height, linewidth=1, edgecolor="black", facecolor="lightblue"
            )
            ax.add_patch(rect)

        # Dynamically calculate plot limits to ensure all boxes fit
        x_values = [x for x, y in pos.values()]
        y_values = [y for x, y in pos.values()]

        # Adjust the limits based on the positions and box sizes
        x_margin = width / 2 + 1  # Add margin for the box width and extra space
        y_margin = height / 2 + 1  # Add margin for the box height and extra space

        ax.set_xlim(min(x_values) - x_margin, max(x_values) + x_margin)
        ax.set_ylim(min(y_values) - y_margin, max(y_values) + y_margin)

        # Remove the default axes for a cleaner look
        ax.set_axis_off()

        # Add a title and display the plot
        # plt.savefig("test_successor_dag.png")


if __name__ == "__main__":
    pytest.main([__file__])
