from Engine.Elements.bag import Bag


class Discard(Bag):
    def __init__(self, bag: Bag):
        super(Discard, self).__init__(list(bag.tiles.keys()), [0]*len(bag.tiles))
