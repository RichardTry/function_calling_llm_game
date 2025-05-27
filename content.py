from os import listdir, path, makedirs
from pathlib import Path
from yaml import safe_load
import pygame

from tile import Tile
from consts import TILE_SIZE

class Content:
    def __init__(self, schemas: Path):
        self.tiles = {}
        self.objects = {}
        self.images = {}
        
        for file in (schemas / 'tiles').iterdir():
            tile = file.stem
            with open(file, 'r', encoding='utf-8') as file:
                schema = safe_load(file)
            image = pygame.image.load(f'textures/{tile}.png').convert()
            image = pygame.transform.scale(image, (TILE_SIZE,) * 2)
            self.tiles[tile] = Tile(tile, image)

        for file in (schemas / 'objects').iterdir():
            object = file.stem
            with open(file, 'r', encoding='utf-8') as file:
                schema = safe_load(object)
            image = pygame.image.load(f'textures/{object}.png').convert()
            image = pygame.transform.scale(image, (TILE_SIZE,) * 2)
            self.tiles[tile] = Tile(object, image)
