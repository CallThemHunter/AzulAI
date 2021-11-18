from __future__ import annotations
from Engine.Elements.board import Board
from Engine.Elements.center import Center
from Engine.Elements.discard import Discard
from Engine.Elements.factory import Factory
from typing import List, Union


class Player:
    has_starting_marker = False

    def __init__(self, player_id: int, board: Board, center: Center, discard: Discard, factories: List[Factory]):
        self.id = player_id
        self.score = 0
        self._board = board
        self._center = center
        self._discard = discard
        self._factories = factories
        self._opponents: List[Player] = []

    def set_opponents(self, opponents: List[Player]):
        self._opponents = opponents

    def end_game_condition_met(self):
        return self._board.end_game_condition_met

    def end_turn_reset(self):
        self._board.end_turn_reset_rows()
        deduction, discard_tiles = self._board.reset_floor()
        self._board.score -= deduction
        self.score = self._board.score
        self._discard.add_bag(discard_tiles)

    def state(self):
        start_tile = self._center.has_starting_tile
        rows = self._board.rows
        wall = self._board.wall
        opponent_rows = [player._board.rows for player in self._opponents]
        opponent_wall = [player._board.wall for player in self._opponents]
        center_tiles = [self._center.tiles]
        factory_tiles = [factory.tiles for factory in self._factories]

        return rows, wall, opponent_rows, opponent_wall, start_tile, center_tiles, factory_tiles

    # interface for AI to make choices

    def make_choice(self, source: Union[Center, Factory], color: int, row: int):
        # return True if valid choice
        # return False if invalid choice
        if isinstance(source, Factory):
            success, tiles = source.claim_tile(color)
            if not success:
                return False
        elif isinstance(source, Center):
            success, tiles = source.claim_tile(color)
            if not success:
                return False
            if source.has_starting_tile:
                self.has_starting_marker = True
                source.has_starting_tile = False
        else:
            return False

        # guaranteed to have 1 tile at least
        # return False if wrong color, color already on wall, or row filled
        success = self._board.fill_row(row, color, len(tiles))
        if not success:
            return False
        return True
