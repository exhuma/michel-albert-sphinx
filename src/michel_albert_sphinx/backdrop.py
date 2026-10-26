"""Seeded contour-line backdrop.

Draws a seamless tile of topographic contour lines from a seed (by default the project
name), so every project gets its own terrain in the same style. Pure Python, deterministic:
the same seed always gives the same tile.

The field is a sum of a few cosine waves with integer frequencies, which makes it periodic,
so the tile repeats without seams. Contours come from marching squares, segments are joined
into polylines, and each polyline is drawn as a smooth curve through the midpoints of its
points.
"""

from __future__ import annotations

import hashlib
import math
import random
from collections import defaultdict

TILE = 1200  #: tile size in px (CSS)
GRID = 150  #: samples per side
WAVES = 9  #: cosine terms in the field
LEVELS = 22  #: contour lines between the lowest and highest point
ACCENT_EVERY = 6  #: every n-th level is an accent line (drawn in clay)

Point = tuple[float, float]


def _field(seed: str) -> list[list[float]]:
    rng = random.Random(int(hashlib.sha256(seed.encode("utf-8")).hexdigest()[:16], 16))
    waves = []
    while len(waves) < WAVES:
        kx, ky = rng.randint(-3, 3), rng.randint(-3, 3)
        if kx == 0 and ky == 0:
            continue
        waves.append((kx, ky, rng.uniform(0.4, 1.0) / math.hypot(kx, ky), rng.uniform(0, 2 * math.pi)))
    values = [
        [
            sum(a * math.cos(2 * math.pi * (kx * j + ky * i) / GRID + phase) for kx, ky, a, phase in waves)
            for j in range(GRID)
        ]
        for i in range(GRID)
    ]
    lo = min(min(row) for row in values)
    hi = max(max(row) for row in values)
    return [[(v - lo) / (hi - lo) for v in row] for row in values]


# Marching squares. Corners: 0 top-left, 1 top-right, 2 bottom-right, 3 bottom-left.
# Edges: "t" top (0-1), "r" right (1-2), "b" bottom (3-2), "l" left (0-3).
_CASES: dict[int, tuple[tuple[str, str], ...]] = {
    1: (("l", "t"),), 2: (("t", "r"),), 3: (("l", "r"),), 4: (("r", "b"),),
    6: (("t", "b"),), 7: (("l", "b"),), 8: (("b", "l"),), 9: (("b", "t"),),
    11: (("b", "r"),), 12: (("r", "l"),), 13: (("r", "t"),), 14: (("t", "l"),),
}  # 5 and 10 (saddles) are resolved in _segments


def _segments(f: list[list[float]], level: float) -> list[tuple[tuple, tuple]]:
    """Segments between edge keys; an edge key is shared by the two cells that touch it."""
    n = GRID
    out = []
    for i in range(n):
        i1 = (i + 1) % n
        for j in range(n):
            j1 = (j + 1) % n
            c = (f[i][j], f[i][j1], f[i1][j1], f[i1][j])
            case = (c[0] > level) | (c[1] > level) << 1 | (c[2] > level) << 2 | (c[3] > level) << 3
            if case in (0, 15):
                continue
            if case in (5, 10):
                centre_high = sum(c) / 4 > level
                if (case == 5) == centre_high:
                    pairs = (("l", "b"), ("t", "r"))
                else:
                    pairs = (("l", "t"), ("r", "b"))
            else:
                pairs = _CASES[case]
            keys = {"t": ("h", i, j), "b": ("h", i + 1, j), "l": ("v", i, j), "r": ("v", i, j + 1)}
            for a, b in pairs:
                out.append((keys[a], keys[b]))
    return out


def _point(f: list[list[float]], key: tuple, level: float) -> Point:
    kind, i, j = key
    n = GRID
    if kind == "h":  # between (i, j) and (i, j + 1)
        a, b = f[i % n][j % n], f[i % n][(j + 1) % n]
        t = (level - a) / (b - a) if b != a else 0.5
        x, y = j + t, i
    else:  # between (i, j) and (i + 1, j)
        a, b = f[i % n][j % n], f[(i + 1) % n][j % n]
        t = (level - a) / (b - a) if b != a else 0.5
        x, y = j, i + t
    scale = TILE / n
    return x * scale, y * scale


def _chains(segments: list[tuple[tuple, tuple]]) -> list[list[tuple]]:
    links: dict[tuple, list[int]] = defaultdict(list)
    for index, (a, b) in enumerate(segments):
        links[a].append(index)
        links[b].append(index)
    used = [False] * len(segments)
    chains = []
    for start in range(len(segments)):
        if used[start]:
            continue
        used[start] = True
        a, b = segments[start]
        chain = [a, b]
        for forward in (True, False):  # grow from both ends
            while True:
                end = chain[-1] if forward else chain[0]
                nxt = next((s for s in links[end] if not used[s]), None)
                if nxt is None:
                    break
                used[nxt] = True
                s0, s1 = segments[nxt]
                other = s1 if s0 == end else s0
                if forward:
                    chain.append(other)
                else:
                    chain.insert(0, other)
        chains.append(chain)
    return chains


def _path(points: list[Point]) -> str:
    """A smooth curve through the midpoints of consecutive points (quadratic Béziers)."""
    r = lambda v: f"{v:.0f}"
    if len(points) < 3:  # short pieces at the tile edge: a straight line keeps the seam closed
        return "".join(("M" if k == 0 else "L") + f"{r(x)} {r(y)}" for k, (x, y) in enumerate(points))
    mids = [((x0 + x1) / 2, (y0 + y1) / 2) for (x0, y0), (x1, y1) in zip(points, points[1:])]
    d = [f"M{r(points[0][0])} {r(points[0][1])}L{r(mids[0][0])} {r(mids[0][1])}"]
    for (cx, cy), (mx, my) in zip(points[1:-1], mids[1:]):
        d.append(f"Q{r(cx)} {r(cy)} {r(mx)} {r(my)}")
    d.append(f"L{r(points[-1][0])} {r(points[-1][1])}")
    return "".join(d)


def contour_tiles(seed: str) -> tuple[str, str]:
    """Return (lines, accent lines) as two SVG documents for a seamless tile."""
    f = _field(seed)
    thin, thick = [], []
    for index in range(LEVELS):
        level = 0.04 + 0.92 * index / (LEVELS - 1)
        for chain in _chains(_segments(f, level)):
            points = [_point(f, key, level) for key in chain]
            if len(points) > 8:  # thin out, but always keep both ends so tiles meet without gaps
                points = points[:-1:2] + [points[-1]]
            path = _path(points)
            if path:
                (thick if index % ACCENT_EVERY == ACCENT_EVERY // 2 else thin).append(path)

    def svg(paths: list[str], width: float) -> str:
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{TILE}" height="{TILE}" viewBox="0 0 {TILE} {TILE}">'
            f'<path d="{"".join(paths)}" fill="none" stroke="#fff" stroke-width="{width}" '
            'stroke-linecap="round" stroke-linejoin="round"/></svg>'
        )

    return svg(thin, 1.1), svg(thick, 1.6)

