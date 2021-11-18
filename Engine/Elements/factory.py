from typing import List
from Engine.Elements.bag import Bag
from Engine.Elements.center import Center


class Factory:
    def __init__(self, center: Center):
        self.center = center
        self.tiles: List[int] = []

    def is_empty(self) -> bool:
        return self.tiles == []

    def fill_factory(self, bag: Bag):
        # assume there are 4 tiles to draw
        self.tiles: List[int] = bag.draw_tiles(4)

    def claim_tile(self, color):
        drawn = []
        if color in self.tiles:
            for tile in reversed(self.tiles):
                if tile == color:
                    drawn.append(self.tiles.pop())
                else:
                    self.center.add_tile(self.tiles.pop())
            return True, drawn
        else:
            return False
