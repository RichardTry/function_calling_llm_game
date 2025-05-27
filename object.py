import pygame
from consts import TILE_SIZE
from world import World


class Object():
    def __init__(self, name: str, image: pygame.Surface, interior: World = None):
        self.name = name
        self.image = image
        self.interior = interior
    
    def draw(self, surface: pygame.Surface, x: int, y: int):
        if self.image:
            surface.blit(self.image, x * TILE_SIZE, y * TILE_SIZE)

    def go_inside(self) -> World:
        return self.interior
