"""Day 1: Secret Entrance - Dial starts at 50, numbers 0-99 (circular)."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts, parse_lines


def parse(lines: list[str]) -> Iterator[tuple[str, int]]:
    """Parse input lines into rotation instructions.
    Args:
        lines: Raw input lines containing rotation commands.
    Yields:
        Tuples of (direction, distance) where direction is 'L' or 'R'."""

    def parse_line(line: str) -> Iterator[tuple[str, int]]:
        yield line[0], int(line[1:])

    return parse_lines(lines, parse_line)


class DialSimulator(ABC):
    """Abstract base class for simulating dial rotations and counting."""

    def __init__(self) -> None:
        """Initialize dial simulator with position 50 and count 0."""
        self.position = 50
        self.count = 0

    def _update_position(self, direction: str, distance: int) -> None:
        """Update dial position based on rotation.
        Args:
            direction: 'L' for left, 'R' for right.
            distance: Number of clicks to rotate."""
        if direction == "L":
            self.position = (self.position - distance) % 100
        else:
            self.position = (self.position + distance) % 100

    @abstractmethod
    def process_rotation(self, direction: str, distance: int) -> None:
        """Process a single rotation with counting logic.
        Args:
            direction: 'L' for left, 'R' for right.
            distance: Number of clicks to rotate."""
        pass

    def _simulate(self, rotations: Iterator[tuple[str, int]]) -> int:
        """Simulate all rotations and return final count.
        Args:
            rotations: Iterator of (direction, distance) tuples.
        Returns:
            Final count after all rotations."""
        for direction, distance in rotations:
            self.process_rotation(direction, distance)
        return self.count

    @classmethod
    def solve(cls, lines: list[str]) -> int:
        """Solve by parsing lines and simulating.
        Args:
            lines: Raw input lines containing rotation instructions.
        Returns:
            Solution result."""
        simulator = cls()
        return simulator._simulate(parse(lines))


class Part1Simulator(DialSimulator):
    """Counts times dial points at 0 after rotation."""

    def process_rotation(self, direction: str, distance: int) -> None:
        """Count logic for part 1: count when position becomes 0.
        Args:
            direction: 'L' for left, 'R' for right.
            distance: Number of clicks to rotate."""
        self._update_position(direction, distance)
        if self.position == 0:
            self.count += 1


class Part2Simulator(DialSimulator):
    """Counts every instance dial points at 0 during rotation."""

    def _count_zero_crossings(self, direction: str, distance: int) -> int:
        """Count how many times dial crosses 0 during a rotation.
        Args:
            direction: 'L' for left, 'R' for right.
            distance: Number of clicks to rotate.
        Returns:
            Number of times 0 is crossed."""
        if direction == "R":
            return (self.position + distance) // 100
        else:  # direction == "L"
            if self.position == 0:
                return distance // 100
            elif distance > self.position:
                return 1 + (distance - self.position) // 100
            elif distance == self.position:
                return 1
            else:
                return 0

    def process_rotation(self, direction: str, distance: int) -> None:
        """Count logic for part 2: count crossings during rotation.
        Args:
            direction: 'L' for left, 'R' for right.
            distance: Number of clicks to rotate."""
        self.count += self._count_zero_crossings(direction, distance)
        self._update_position(direction, distance)


if __name__ == "__main__":
    run_parts(
        Part1Simulator.solve,
        Part2Simulator.solve,
    )
