"""Day 8: Playground - Connect closest junction boxes in 3D space.

Uses networkx for graph operations.
"""

import sys
import os
from itertools import combinations

import networkx as nx

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run


def parse(f) -> list[tuple[int, int, int]]:
    """Parse 3D coordinates.
    Args:
        f: File handle.
    Returns:
        List of (x, y, z) tuples."""
    return [tuple(map(int, line.strip().split(','))) for line in f]


def distance_sq(p1, p2) -> int:
    """Squared Euclidean distance between two 3D points.
    Args:
        p1: First point (x, y, z).
        p2: Second point (x, y, z).
    Returns:
        Squared distance."""
    return (p1[0]-p2[0])**2 + (p1[1]-p2[1])**2 + (p1[2]-p2[2])**2


def build_sorted_edges(parsed):
    """Build sorted list of edges by distance.
    Args:
        parsed: List of 3D points.
    Returns:
        List of (distance, i, j) tuples sorted by distance."""
    edges = []
    for i, j in combinations(range(len(parsed)), 2):
        edges.append((distance_sq(parsed[i], parsed[j]), i, j))
    edges.sort()
    return edges


def count_part1(parsed, num_connections=1000) -> int:
    """Connect closest pairs, multiply 3 largest circuit sizes.
    Args:
        parsed: List of 3D points.
        num_connections: Number of connections to make.
    Returns:
        Product of 3 largest circuit sizes."""
    edges = build_sorted_edges(parsed)

    G = nx.Graph()
    G.add_nodes_from(range(len(parsed)))

    for _, i, j in edges[:num_connections]:
        G.add_edge(i, j)

    sizes = sorted([len(c) for c in nx.connected_components(G)], reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def count_part2(parsed) -> int:
    """Connect until all in one circuit, return product of last pair's X coords.
    Args:
        parsed: List of 3D points.
    Returns:
        Product of X coordinates of last connected pair."""
    edges = build_sorted_edges(parsed)

    G = nx.Graph()
    G.add_nodes_from(range(len(parsed)))

    for _, i, j in edges:
        if not nx.has_path(G, i, j):
            G.add_edge(i, j)
            if nx.number_connected_components(G) == 1:
                return parsed[i][0] * parsed[j][0]
    return 0


if __name__ == "__main__":
    run(__file__, parse, count_part1, count_part2)
