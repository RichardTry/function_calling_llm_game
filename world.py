import random
from noise import pnoise2

from tile import Tile

class World:
    def __init__(self, tiles, size_x, size_y):
        self.size_x = size_x
        self.size_y = size_y
        self.tiles = tiles
        self.map = []

        self.generate_map()

    def generate_map(self, scale=10.0, octaves=6, persistence=0.5, lacunarity=2.0, seed=None):
        if seed is None:
            seed = random.randint(0, 10000)

        def get_tile_by_height(height_value):
            if height_value < 0:
                return 'water'
            elif height_value < 0.1:
                return 'sand'
            elif height_value < 0.4:
                return 'dirt'
            else:
                return 'grass'

        self.map = []
        for y in range(self.size_y):
            row = []
            for x in range(self.size_x):
                nx = x / scale
                ny = y / scale
                height_value = pnoise2(nx, ny, octaves=octaves, persistence=persistence, lacunarity=lacunarity, repeatx=1024, repeaty=1024, base=seed)
                tile = self.tiles[get_tile_by_height(height_value)]
                row.append(tile)
            self.map.append(row)

        return self.map

    def draw(self, surface):
        for y in range(self.size_y):
            for x in range(self.size_x):
                tile: Tile = self.map[y][x]
                tile.draw(surface, x, y)
