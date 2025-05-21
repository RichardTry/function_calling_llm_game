from consts import TILE_SIZE


class Tile:
    def __init__(self, tile_type, image):
        self.tile_type = tile_type
        self.image = image
        self.object = None

    def draw(self, surface, x, y):
        surface.blit(self.image, (x * TILE_SIZE, y * TILE_SIZE))
