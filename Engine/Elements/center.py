class Center:
    has_starting_tile = True

    def __init__(self):
        self.tiles = []

    def is_empty(self):
        return self.tiles == []

    def add_tile(self, tile_type: int):
        self.tiles += [tile_type]

    def claim_tile(self, color):
        ret = []
        remaining = []
        for tile in reversed(self.tiles):
            if tile == color:
                ret.append(self.tiles.pop())
            else:
                remaining.append(self.tiles.pop())
        self.tiles = remaining
        if ret == []:
            return False, []
        return True, ret


