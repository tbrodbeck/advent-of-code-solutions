"""Day 10: [Problem Title] - [Brief description]."""

from z3 import Int, Optimize, Sum, sat
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import run


def _parse_diagram(diagram: str) -> set[int]:
    """Parse a diagram string into a set of integers.
    Args:
        diagram: The diagram string to parse.
    Returns:
        A set of integers representing the diagram."""
    parsed = set()
    for idx, character in enumerate(diagram):
        if character == "#":
            parsed.add(idx)
        elif character != ".":
            raise ValueError(f"Invalid character: {character}")
    return parsed


def _parse_joltage(joltage: str) -> list[int]:
    """Parse a joltage string into an integer.
    Args:
        joltage: The joltage string to parse.
    Returns:
        An integer representing the joltage."""
    return [int(joltage) for joltage in joltage.strip("{}").split(",")]


def parse(f):
    """Parse input file into a list of (diagram, schematics, joltage) tuples.
    Args:
        f: File handle.
    Returns:
        A list of (diagram, schematics, joltage) tuples."""
    lines = []
    for line in f:
        line = line.strip().split(" ")
        diagram = _parse_diagram(line[0][1:-1])
        schematics = []
        for schematic_raw in line[1:-1]:
            schematic = [int(action) for action in schematic_raw.strip("()").split(",")]
            schematics.append(schematic)
        joltage = _parse_joltage(line[-1])
        lines.append((diagram, sorted(schematics, key=len), joltage))
    return lines


class DiagramSolver:
    """Solver for a diagram.
    Args:
        diagram: The diagram to solve.
        schematics: The schematics to use.
        level: The level of the diagram.
        all_diagrams: The list of all diagrams encountered so far.
    """

    def __init__(
        self,
        diagram: set[int],
        schematics: list[int],
        level: int = 0,
        all_diagrams: list[set[int]] = [],
    ):
        self.diagram = diagram.copy()
        self.schematics = schematics
        self.level = level
        self.childSolvers = []
        self.all_diagrams = all_diagrams
        self.all_diagrams.append(diagram)

    def solve(self) -> int:
        """Solve the diagram.
        Returns:
            The inception level of the diagram."""
        inception_level = 0
        while True:
            if self._solve_level(inception_level):
                return inception_level
            inception_level += 1

    def _solve_level(self, inception_level: int):
        """Solve the diagram at a given level.
        Args:
            inception_level: The level to solve.
        Returns:
            True if the diagram is solved, False otherwise."""
        if not self.diagram:
            return True

        if self.level == inception_level:
            self._add_child_solvers()

        if self.level < inception_level:
            for childSolver in self.childSolvers:
                if childSolver._solve_level(inception_level):
                    return True

        return False

    def _add_child_solvers(self):
        """Add child solvers to the current solver."""
        for schematic in self.schematics:
            diagram_candidate = self.diagram.copy()
            for action in schematic:
                if action in diagram_candidate:
                    diagram_candidate.discard(action)
                else:
                    diagram_candidate.add(action)
            if diagram_candidate not in self.all_diagrams:
                self.childSolvers.append(
                    DiagramSolver(
                        diagram_candidate,
                        self.schematics,
                        self.level + 1,
                        self.all_diagrams,
                    )
                )


def _solve_min_sum(eq_list):
    """Solve linear equalities over ℕ₀ minimizing total variable sum.
    Args:
        eq_list: List of (total, idxs) constraints meaning sum(x[i] for i in idxs) == total.
    Returns:
        List of variable values (x0..x{n-1}) for an optimal model, or None if unsat."""
    # infer variables
    n = max(i for total, idxs in eq_list for i in idxs) + 1
    x = [Int(f"x{i}") for i in range(n)]

    opt = Optimize()

    # domain ℕ₀
    opt.add([xi >= 0 for xi in x])

    # constraints (duplicates are fine)
    for total, idxs in eq_list:
        opt.add(Sum(x[i] for i in idxs) == total)

    # objective: minimize total sum of all variables
    opt.minimize(Sum(x))

    if opt.check() != sat:
        return None

    m = opt.model()
    sol = [m[x[i]].as_long() for i in range(n)]
    return sol


def count_part1(parsed) -> int:
    """Solve part 1 by summing the inception levels of all diagrams.
    Args:
        parsed: Parsed input data.
    Returns:
        Answer for part 1."""
    presses = 0
    for diagram, schematics, _ in parsed:
        solver = DiagramSolver(diagram, schematics, all_diagrams=[])
        presses += solver.solve()
    return presses


def count_part2(parsed) -> int:
    """Solve part 2.
    Args:
        parsed: Parsed input data.
    Returns:
        Answer for part 2."""
    presses = 0
    for _, schematics, joltages in parsed:
        relevant_schematics = []
        for jolt_idx, joltage in enumerate(joltages):
            schematics_found = [
                (schem_idx, schematic)
                for schem_idx, schematic in enumerate(schematics)
                if jolt_idx in schematic
            ]

            schematics_found_1 = []
            for schem_idx, schematic in schematics_found:
                schematics_found_1.append((schem_idx))
            relevant_schematics.append((joltage, schematics_found_1))
        solution = _solve_min_sum(relevant_schematics)
        presses += sum(solution)
    return presses


if __name__ == "__main__":
    run(__file__, parse, count_part1, count_part2)
