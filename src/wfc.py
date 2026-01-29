import random

from PIL import Image


class Pattern:
    def __init__(self, data, index):
        self.data = data  # tuple of pixels
        self.index = index
        self.up = set()
        self.right = set()
        self.down = set()
        self.left = set()


class WFC:
    def __init__(self, sample_img, pattern_size, out_width, out_height):
        self.sample_img = sample_img.convert("RGB")
        self.pattern_size = pattern_size
        self.out_width = out_width
        self.out_height = out_height

        self.patterns = []
        self.pattern_map = {}
        self._extract_patterns()
        self._build_adjacency()

        self.grid = [
            [set(range(len(self.patterns))) for _ in range(out_width)]
            for _ in range(out_height)
        ]

    def _extract_patterns(self):
        pixels = self.sample_img.load()
        w, h = self.sample_img.size
        n = self.pattern_size

        for y in range(h - n + 1):
            for x in range(w - n + 1):
                block = tuple(
                    pixels[x + dx, y + dy] for dy in range(n) for dx in range(n)
                )
                if block not in self.pattern_map:
                    idx = len(self.patterns)
                    self.pattern_map[block] = idx
                    self.patterns.append(Pattern(block, idx))

    def _build_adjacency(self):
        n = self.pattern_size
        for a in self.patterns:
            for b in self.patterns:
                if self._match_right(a.data, b.data, n):
                    a.right.add(b.index)
                if self._match_left(a.data, b.data, n):
                    a.left.add(b.index)
                if self._match_down(a.data, b.data, n):
                    a.down.add(b.index)
                if self._match_up(a.data, b.data, n):
                    a.up.add(b.index)

    def _match_right(self, A, B, n):
        for y in range(n):
            if A[y * n + 1 : (y + 1) * n] != B[y * n : (y + 1) * n - 1]:
                return False
        return True

    def _match_left(self, A, B, n):
        return self._match_right(B, A, n)

    def _match_down(self, A, B, n):
        return A[n:] == B[:-n]

    def _match_up(self, A, B, n):
        return self._match_down(B, A, n)

    def collapse(self):
        while True:
            cell = self._lowest_entropy_cell()
            if cell is None:
                return True

            x, y = cell
            choice = random.choice(list(self.grid[y][x]))
            self.grid[y][x] = {choice}

            if not self._propagate(x, y):
                return False

    def _lowest_entropy_cell(self):
        min_e = float("inf")
        best = None
        for y in range(self.out_height):
            for x in range(self.out_width):
                if len(self.grid[y][x]) > 1:
                    if len(self.grid[y][x]) < min_e:
                        min_e = len(self.grid[y][x])
                        best = (x, y)
        return best

    def _propagate(self, x, y):
        stack = [(x, y)]
        while stack:
            cx, cy = stack.pop()
            opts = self.grid[cy][cx]

            for dx, dy, dir in [
                (0, -1, "up"),
                (1, 0, "right"),
                (0, 1, "down"),
                (-1, 0, "left"),
            ]:
                nx, ny = cx + dx, cy + dy
                if not (0 <= nx < self.out_width and 0 <= ny < self.out_height):
                    continue

                allowed = set()
                for p in opts:
                    allowed |= getattr(self.patterns[p], dir)

                before = self.grid[ny][nx]
                new = before & allowed

                if not new:
                    return False

                if new != before:
                    self.grid[ny][nx] = new
                    stack.append((nx, ny))
        return True

    def render(self):
        n = self.pattern_size
        img = Image.new("RGB", (self.out_width + n - 1, self.out_height + n - 1))
        pixels = img.load()

        if not pixels:
            return img
            
        for y in range(self.out_height):
            for x in range(self.out_width):
                p = next(iter(self.grid[y][x]))
                data = self.patterns[p].data
                for dy in range(n):
                    for dx in range(n):            
                        pixels[x + dx, y + dy] = data[dy * n + dx]

        return img
