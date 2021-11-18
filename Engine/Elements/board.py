from typing import List, Dict
from Engine.Elements.bag import Bag

# 0: Blue
# 1: Yellow
# 2: Red
# 3: Black
# 4: Cyan


def bag_from_dict(tile_dict: Dict[int, int]):
    return Bag(list(tile_dict.keys()), list(tile_dict.values()))


class Board:
    end_game_condition_met = False

    rows: List[int] = [0, 0, 0, 0, 0]
    row_color: List[int] = [None for _ in range(0, 5)]
    row_is_filled: List[bool] = [False for _ in range(0, 5)]

    wall_colors_filled: List[List[bool]] = [[False for _ in range(0, 5)] for _ in range(0, 5)]
    wall: List[List[bool]] = [[False for _ in range(0, 5)] for _ in range(0, 5)]

    # provide color
    floor: List[int] = []
    floor_penalty = [1, 1, 2, 2, 2, 3, 3]

    score = 0

    def end_turn_reset_rows(self):
        ret_tiles = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        for i, row in enumerate(self.rows):
            row_capacity = i + 1
            color = self.row_color[i]

            if row_capacity == self.rows[i]:
                self.fill_wall(i, color)
                self.rows[i] = 0
                ret_tiles[color] += row_capacity - 1

        return bag_from_dict(ret_tiles)

    def reset_floor(self):
        ret_tiles = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0
        }
        deduction = 0
        for i, color in enumerate(self.floor):
            if color != -1:
                ret_tiles[color] += 1
            deduction += self.floor_penalty[i]

        self.floor = []
        return deduction, bag_from_dict(ret_tiles)

    def fill_row(self, row: int, color: int, n: int):
        if self.row_color[row] is None:
            # starting to add a color to row
            self.row_color[row] = color
        elif self.row_color[row] != color:
            # trying to add a different color to the tile row
            return False
        elif color in self.wall_colors_filled[row]:
            # trying to add a color that's already present in the wall
            return False
        if self.row_is_filled[row]:
            return False

        row_capacity = row + 1
        tiles_in_row = self.rows[row]
        if tiles_in_row + n < row_capacity:
            self.rows[row] = tiles_in_row + n
        elif tiles_in_row + n == row_capacity:
            self.rows[row] = tiles_in_row + n
            self.row_is_filled[row] = True
        else:
            self.rows[row] = row_capacity
            self.row_is_filled[row] = True
            self.floor += [color] * (tiles_in_row + n - row_capacity)
        return True

    def fill_wall(self, i: int, color: int):
        # 0: Blue
        # 1: Yellow
        # 2: Red
        # 3: Black
        # 4: Cyan
        # right rotated by i rows
        col = (i + color) % 5
        self.wall[i][col] = True
        self.wall_colors_filled[i][color] = True
        self.score_tile(i, col)

    # updates score
    def score_tile(self, row, col):
        horizontal = self.count_connected_horizontal(row, col)
        vertical = self.count_connected_vertical(row, col)
        if horizontal == 0 and vertical == 0:
            self.score += 1
        else:
            self.score += horizontal + vertical

    def remove_tile(self, row, col):
        horizontal = self.count_connected_horizontal(row, col)
        vertical = self.count_connected_vertical(row, col)
        if horizontal == 0 and vertical == 0:
            self.score -= 1
        else:
            self.score -= horizontal + vertical

        self.wall[row][col] = False
        self.wall_colors_filled[row][(col - row) % 5] = False
        return self.score

    def count_connected_vertical(self, row, col):
        link_remains = True
        length = 0
        for i in range(row + 1, 5):
            if link_remains and self.wall[i][col]:
                length += 1
            else:
                link_remains = False

        link_remains = True
        for i in range(row - 1, -1, -1):
            if link_remains and self.wall[i][col]:
                length += 1
            else:
                link_remains = False

        if length != 0:
            return length + 1
        return 0

    def count_connected_horizontal(self, row, col):
        link_remains = True
        length = 0
        for i in range(col + 1, 5):
            if link_remains and self.wall[row][i]:
                length += 1
            else:
                link_remains = False

        link_remains = True
        for i in range(col - 1, -1, -1):
            if link_remains and self.wall[row][i]:
                length += 1
            else:
                link_remains = False

        if length != 0:
            length += 1
            if length == 5:
                self.end_game_condition_met = True
            return length
        return 0

    def score_bonus(self):
        pass
