class Rectangle:
    x1: int = 0
    y1: int = 0
    x2: int = 0
    y2: int = 0

    def from_corners(self, x1: int, y1: int, x2: int, y2: int):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        return self

    def from_xywh(self, x, y, w, h):
        self.from_corners(x, y, x+w, y+h)
        return self

    def coordinates(self, scale: float = 1.0):
        return (int(self.x1 * scale), int(self.y1 * scale)), (int(self.x2 * scale), int(self.y2 * scale))

    def is_in(self, other) -> bool:
        if self.x1 < other.x1:
            return False
        if self.x2 > other.x2:
            return False
        if self.y1 < other.y1:
            return False
        if self.y2 > other.y2:
            return False
        return True

    def contains(self, other):
        return other.is_in(self)


