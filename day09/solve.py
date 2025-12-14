"""Day 9: Polygon Rectangles - Find largest rectangles in/from polygon vertices."""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def parse(f):
    """Parse polygon vertices from comma-separated coordinates.
    Args:
        f: File handle.
    Returns:
        List of (x, y) tuples."""
    return [tuple(map(int, line.strip().split(","))) for line in f]


def count_part1(parsed) -> int:
    """Find largest rectangle using any two vertices as opposite corners.
    Args:
        parsed: List of (x, y) vertices.
    Returns:
        Area of largest rectangle."""
    max_area = 0
    for idx, (x1, y1) in enumerate(parsed):
        for x2, y2 in parsed[idx + 1 :]:
            max_area = max(max_area, (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1))
    return max_area


def count_part2(parsed) -> int:
    """Find largest axis-aligned rectangle fully contained within the polygon.
    Args:
        parsed: List of (x, y) vertices forming the polygon.
    Returns:
        Area of largest contained rectangle."""
    polygon = Polygon(parsed)
    shape_sizes = []
    for start_point in parsed:
        for end_point in parsed:
            edge_1 = Point(start_point[0], end_point[1])
            edge_2 = Point(end_point[0], start_point[1])
            rectangle = Polygon([start_point, edge_1, end_point, edge_2])
            if polygon.contains(rectangle):
                shape_sizes.append(
                    (abs(start_point[0] - end_point[0]) + 1)
                    * (abs(start_point[1] - end_point[1]) + 1)
                )
    return max(shape_sizes)


if __name__ == "__main__":
    run(__file__, parse, count_part1, count_part2)
