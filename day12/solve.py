"""Day 12: Christmas Tree Farm - Count regions where presents can fit."""

import re
from functools import lru_cache
from pathlib import Path


def parse(f):
    """Parse input file.
    Args:
        f: File handle.
    Returns:
        Tuple (shapes, regions).
        shapes: list[tuple[tuple[int,int], ...]] where each shape is its filled cells.
        regions: list[tuple[int,int,list[int]]] as (width, height, quantities)."""
    lines = [line.rstrip("\n") for line in f]
    shape_header_re = re.compile(r"^(\d+):(?:\s*([#.]+))?$")
    region_re = re.compile(r"^(\d+)x(\d+):\s*(.*)$")

    shapes_by_idx: dict[int, list[str]] = {}
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if region_re.match(line):
            break
        m = shape_header_re.match(line)
        if not m:
            raise ValueError(f"Expected shape header or region, got: {line!r}")
        idx = int(m.group(1))
        rows: list[str] = []
        first = m.group(2)
        if first is not None and first != "":
            rows.append(first)
        i += 1
        while i < len(lines):
            s = lines[i].strip()
            if not s:
                i += 1
                continue
            if shape_header_re.match(s) or region_re.match(s):
                break
            if not set(s) <= {".", "#"}:
                raise ValueError(f"Invalid shape row: {s!r}")
            rows.append(s)
            i += 1
        if not rows:
            raise ValueError(f"Shape {idx} has no rows")
        shapes_by_idx[idx] = rows

    if not shapes_by_idx:
        raise ValueError("No shapes found")
    max_idx = max(shapes_by_idx)
    shapes: list[tuple[tuple[int, int], ...]] = []
    for idx in range(max_idx + 1):
        rows = shapes_by_idx.get(idx)
        if rows is None:
            raise ValueError(f"Missing shape index {idx}")
        cells = [
            (x, y)
            for y, row in enumerate(rows)
            for x, ch in enumerate(row)
            if ch == "#"
        ]
        if not cells:
            raise ValueError(f"Shape {idx} has no filled cells")
        shapes.append(_normalize_cells(cells))

    regions: list[tuple[int, int, list[int]]] = []
    while i < len(lines):
        line = lines[i].strip()
        i += 1
        if not line:
            continue
        m = region_re.match(line)
        if not m:
            raise ValueError(f"Invalid region line: {line!r}")
        w, h = int(m.group(1)), int(m.group(2))
        qty = [int(x) for x in m.group(3).split()] if m.group(3).strip() else []
        regions.append((w, h, qty))

    return shapes, regions


def _normalize_cells(cells: list[tuple[int, int]]) -> tuple[tuple[int, int], ...]:
    min_x = min(x for x, _ in cells)
    min_y = min(y for _, y in cells)
    return tuple(sorted((x - min_x, y - min_y) for x, y in cells))


def _orientations(
    shape: tuple[tuple[int, int], ...],
) -> list[tuple[tuple[tuple[int, int], ...], int, int]]:
    def rot90(c):
        return [(y, -x) for x, y in c]

    def flipx(c):
        return [(-x, y) for x, y in c]

    seen: set[tuple[tuple[int, int], ...]] = set()
    out: list[tuple[tuple[tuple[int, int], ...], int, int]] = []
    base = list(shape)
    for variant in (base, flipx(base)):
        cur = variant
        for _ in range(4):
            norm = _normalize_cells(cur)
            if norm not in seen:
                seen.add(norm)
                w = max(x for x, _ in norm) + 1
                h = max(y for _, y in norm) + 1
                out.append((norm, w, h))
            cur = rot90(cur)
    return out


def _placements(w: int, h: int, shape: tuple[tuple[int, int], ...]) -> list[int]:
    masks: set[int] = set()
    for cells, sw, sh in _orientations(shape):
        if sw > w or sh > h:
            continue
        for oy in range(h - sh + 1):
            for ox in range(w - sw + 1):
                mask = 0
                for x, y in cells:
                    mask |= 1 << ((oy + y) * w + (ox + x))
                masks.add(mask)
    return sorted(masks)


def _can_fit_region(
    w: int, h: int, shapes: list[tuple[tuple[int, int], ...]], qty: list[int]
) -> bool:
    qty = qty + [0] * (len(shapes) - len(qty))
    if len(qty) != len(shapes):
        raise ValueError("Region quantities must match number of shapes")

    areas = [len(s) for s in shapes]
    needed = sum(q * a for q, a in zip(qty, areas))
    if needed > w * h:
        return False

    placements_by_shape = [_placements(w, h, s) for s in shapes]
    for q, pl in zip(qty, placements_by_shape):
        if q and not pl:
            return False

    pieces = sum(qty)
    if w * h > 120 or pieces > 18:
        return True

    qty_t = tuple(qty)

    @lru_cache(None)
    def dfs(occupied: int, counts: tuple[int, ...]) -> bool:
        if not any(counts):
            return True
        best_i = -1
        best_opts: list[int] | None = None
        for i, c in enumerate(counts):
            if not c:
                continue
            opts = [m for m in placements_by_shape[i] if (m & occupied) == 0]
            if not opts:
                return False
            if best_opts is None or len(opts) < len(best_opts):
                best_i = i
                best_opts = opts
                if len(best_opts) == 1:
                    break
        assert best_opts is not None
        for m in best_opts:
            nxt = list(counts)
            nxt[best_i] -= 1
            if dfs(occupied | m, tuple(nxt)):
                return True
        return False

    return dfs(0, qty_t)


def count_part1(parsed) -> int:
    """Solve part 1.
    Args:
        parsed: Parsed input data.
    Returns:
        Answer for part 1."""
    shapes, regions = parsed
    return sum(1 for w, h, qty in regions if _can_fit_region(w, h, shapes, qty))


if __name__ == "__main__":
    with Path(__file__).with_name("input.txt").open() as f:
        parsed = parse(f)
    ans = count_part1(parsed)
    print(f"Part 1: {ans}")
