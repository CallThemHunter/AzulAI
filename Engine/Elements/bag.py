from __future__ import annotations
from typing import List, Dict
import random


class Bag:
    def __init__(self, tile_types: List[int], tile_count: List[int]):
        self.tiles: Dict[int, int] = {}
        for (i, j) in zip(tile_types, tile_count):
            self.tiles[i] = j

    def is_empty(self):
        return 0 == sum(self.tiles.values())

    def count(self):
        return sum(self.tiles.values())

    def add_tile(self, tile_type):
        self.tiles[tile_type] += 1

    def add_bag(self, bag: Bag):
        for (tile_type, tile_count) in bag.tiles:
            if tile_type in self.tiles.keys():
                self.tiles[tile_type] += tile_count
            else:
                self.tiles[tile_type] = tile_count
            # reset dumped bag to 0
            bag.tiles[tile_type] = 0

    def draw_tile(self) -> int:
        tile: int = random.choices(list(self.tiles.keys()), list(self.tiles.values()), k=1)[0]
        self.tiles[tile] -= 1
        return tile

    def draw_tiles(self, n) -> List[int]:
        return [self.draw_tile() for _ in range(0, n)]
