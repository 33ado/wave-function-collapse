class Tile:
    def __init__(self, img):
        self.img = img
        self.index = -1
        self.edges = []
        self.up = []
        self.right = []
        self.down = []
        self.left = []

    def draw(self, win, x, y):
        win.draw(self.img, x, y)

    def set_rules(self, tiles):
        for tile in tiles:
            # Upper edge
            if self.edges[0] == tile.edges[2]:
                self.up.append(tile)

            # Right edge
            if self.edges[1] == tile.edges[3]:
                self.right.append(tile)

            # Lower edge
            if self.edges[2] == tile.edges[0]:
                self.down.append(tile)

            # Left edge
            if self.edges[3] == tile.edges[1]:
                self.down.append(tile)
