from Engine.Player.player import Player
from Engine.Elements.bag import Bag
from Engine.Elements.board import Board
from Engine.Elements.center import Center
from Engine.Elements.discard import Discard
from Engine.Elements.factory import Factory

PlayerCount = int
default_bag = {
    0: 20,
    1: 20,
    2: 20,
    3: 20,
    4: 20
}


class Game:
    i = 0

    def __init__(self, n: PlayerCount):
        self.num_players = n
        self.bag: Bag
        self.discard: Discard
        self.factories: list[Factory]
        self.players: list[Player]

        if n == 2:
            num_factories = 5
        elif n == 3:
            num_factories = 7
        elif n == 4:
            num_factories = 9
        else:
            raise ValueError

        self.bag = Bag(list(default_bag.keys()), list(default_bag.values()))
        self.discard = Discard(self.bag)
        self.center = Center()

        self.factories = []
        for i in range(0, num_factories):
            self.factories += Factory(self.center)

        self.players = []
        for i in range(0, n):
            player = Player(i, Board(), self.factories, )
            self.players.append(player)

        for i in range(0, n):
            opponents: list[Player] = self.players.copy()
            opponents.pop(i)
            self.players[i].set_opponents(opponents)
        self.starting_player: Player = self.players[0]

    def fill_factories(self):
        self.center.has_starting_tile = True
        for factory in self.factories:
            self.check_bag()
            factory.fill_factory(self.bag)

        for player in self.players:
            if player.has_starting_marker:
                self.starting_player = player
                player.has_starting_marker = False

    def check_bag(self):
        if self.bag.count == 0:
            self.bag.add_bag(self.discard)
        if self.bag.count() < 4:
            tiles = self.discard.draw_tiles(4 - self.bag.count())
            for tile in tiles:
                self.bag.add_tile(tile)

    def set_starting_player(self):
        idx = self.players.index(self.starting_player)

        for i in range(0, idx):
            self.players.append(self.players.pop(0))
        return

    def player_request(self):
        # provide state to agent
        return self.i, self.players[self.i].state()

    def player_action(self, args):
        # False if error
        # substitute with argument parsing
        success = self.players[self.i].make_choice(Factory(Center()), 0, 0)

        if not success:
            return False
        self.i = (self.i + 1) % self.num_players

        if self.no_tiles_remain():
            for player in self.players:
                player.end_turn_reset()
            self.fill_factories()

        state = self.players[self.i].state()
        score = self.players[self.i].score
        end_game = self.end_game_cond_met()
        # return True, new state, current score estimate, end game condition met
        return True, state, score, end_game

    def end_game_cond_met(self):
        return any([player.end_game_condition_met() for player in self.players])

    def no_tiles_remain(self):
        for factory in self.factories:
            if not factory.is_empty():
                return False

        if self.center.is_empty():
            return True
        return False
