import pygame
from consts import TILE_SIZE


class Tile:
    def __init__(self, tile_type, image: pygame.Surface):
        self.tile_type = tile_type
        self.image = image
        self.object = None

    def draw(self, surface: pygame.Surface, x, y):
        surface.blit(self.image, (x * TILE_SIZE, y * TILE_SIZE))
        if self.object is not None:
            self.object.draw(surface, x, y)
