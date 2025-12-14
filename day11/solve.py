"""Day 11: Reactor."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run


from functools import lru_cache


def parse(f):
    """Parse input file.
    Args:
        f: File handle.
    Returns:
        Directed graph as dict[str, list[str]]."""
    g = {}
    for line in f:
        line = line.strip()
        if not line:
            continue
        src, rest = line.split(":")
        g[src] = rest.strip().split()
    return g


def count_part1(graph) -> int:
    """Solve part 1.
    Counts all directed paths from 'you' to 'out'.
    Args:
        graph: Directed graph.
    Returns:
        Total number of paths."""

    @lru_cache(None)
    def paths(node):
        if node == "out":
            return 1
        return sum(paths(nxt) for nxt in graph.get(node, []))

    return paths("you")


def count_part2(graph) -> int:
    """Solve part 2.
    Counts all directed paths from 'svr' to 'out' that pass
    through both 'dac' and 'fft' in any order.
    Args:
        graph: Directed graph.
    Returns:
        Total number of valid paths."""

    @lru_cache(None)
    def paths(src, dst):
        if src == dst:
            return 1
        return sum(paths(nxt, dst) for nxt in graph.get(src, []))

    return paths("svr", "dac") * paths("dac", "fft") * paths("fft", "out") + paths(
        "svr", "fft"
    ) * paths("fft", "dac") * paths("dac", "out")


if __name__ == "__main__":
    run(__file__, parse, count_part1, count_part2)
