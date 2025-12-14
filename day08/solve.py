"""Day 8: Playground - Connect closest junction boxes in 3D space."""

import sys
import os
from itertools import combinations

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


class UnionFind:
    """Union-Find data structure for tracking connected components.
    Args:
        n: Number of elements."""
    
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        """Find root of element with path compression.
        Args:
            x: Element index.
        Returns:
            Root index."""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        """Union two elements by rank.
        Args:
            x: First element index.
            y: Second element index."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
    
    def component_sizes(self):
        """Get sizes of all connected components.
        Returns:
            Counter of component sizes."""
        from collections import Counter
        return Counter(self.find(i) for i in range(len(self.parent)))


def build_circuits(parsed):
    """Build sorted distances and UnionFind for points.
    Args:
        parsed: List of 3D points.
    Returns:
        Tuple of (sorted distances, UnionFind instance)."""
    distances = []
    for i, j in combinations(range(len(parsed)), 2):
        distances.append((distance_sq(parsed[i], parsed[j]), i, j))
    distances.sort()
    return distances, UnionFind(len(parsed))


def count_part1(parsed, num_connections=1000) -> int:
    """Connect closest pairs, multiply 3 largest circuit sizes.
    Args:
        parsed: List of 3D points.
        num_connections: Number of connections to make.
    Returns:
        Product of 3 largest circuit sizes."""
    distances, uf = build_circuits(parsed)
    
    for _, i, j in distances[:num_connections]:
        uf.union(i, j)
    
    sizes = sorted(uf.component_sizes().values(), reverse=True)
    return sizes[0] * sizes[1] * sizes[2]


def count_part2(parsed) -> int:
    """Connect until all in one circuit, return product of last pair's X coords.
    Args:
        parsed: List of 3D points.
    Returns:
        Product of X coordinates of last connected pair."""
    distances, uf = build_circuits(parsed)
    
    for _, i, j in distances:
        if uf.find(i) != uf.find(j):
            uf.union(i, j)
            if len(uf.component_sizes()) == 1:
                return parsed[i][0] * parsed[j][0]
    return 0


if __name__ == "__main__":
    run(__file__, parse, count_part1, count_part2)
