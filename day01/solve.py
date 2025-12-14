"""Day 1: Secret Entrance - Dial starts at 50, numbers 0-99 (circular)."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run_parts, parse_lines


def parse(lines: list[str]) -> Iterator[int]:
    """Parse input lines.
    Args: lines: Raw input lines.
    Returns: Iterator of (direction, distance)."""

    def parse_line(line: str) -> Iterator[int]:
        if line[0] == "R":
            yield int(line[1:])
        elif line[0] == "L":
            yield -int(line[1:])
        else:
            raise ValueError(f"Invalid direction: {line[0]}")

    return parse_lines(lines, parse_line)


class DialSimulator(ABC):
    """Base class for Day 1 simulation."""

    def __init__(self) -> None:
        """Initialize simulator state."""
        self.position = 50
        self.counter = 0

    @abstractmethod
    def process_rotation(self, distance: int) -> None:
        """Process one rotation.
        Args:
              distance: Rotation distance."""
        pass

    @classmethod
    def solve(cls, lines: list[str]) -> int:
        """Solve Day 1 for this simulator.
        Args: lines: Raw input lines.
        Returns: Answer for this part."""
        simulator = cls()
        for distance in parse(lines):
            simulator.process_rotation(distance)
        return simulator.counter


class Part1Simulator(DialSimulator):
    """Day 1 Part 1 simulator."""

    def process_rotation(self, distance: int) -> None:
        """Process one rotation.
        Args:
              distance: Rotation distance."""
        self.position += distance
        self.position = self.position % 100
        if self.position == 0:
            self.counter += 1


class Part2Simulator(DialSimulator):
    """Day 1 Part 2 simulator."""

    def _count_zero_crossings(self) -> int:
        """Check if the position is between 0 and 99.
        Args:
            position: Current position.
            previous_position: Previous position.
        Returns:
            True if the position is between 0 and 99, False otherwise."""
        if self.previous_position < 100 <= self.position:
            self.counter += self.position // 100
        elif self.position <= 0 < self.previous_position:
            self.counter += -self.position // 100 + 1
        elif self.previous_position == 0 and self.position <= -100:
            self.counter += -self.position // 100

    def process_rotation(self, distance: int) -> None:
        """Process one rotation.
        Args: direction: Rotation direction.
              distance: Rotation distance."""
        self.previous_position = self.position
        self.position += distance
        self._count_zero_crossings()
        self.position = self.position % 100


if __name__ == "__main__":
    run_parts(Part1Simulator.solve, Part2Simulator.solve)
