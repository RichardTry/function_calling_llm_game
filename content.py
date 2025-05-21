from os import listdir, path, makedirs
from pathlib import Path
from yaml import safe_load
import pygame

from tile import Tile
from consts import TILE_SIZE

class Content:
    def __init__(self, schemas_directory):
        self.tiles = {}
        self.images = {}
        for filename in listdir(schemas_directory):
            file_path = Path(path.join(schemas_directory, filename))
            tile = file_path.stem
            with open(file_path, 'r', encoding='utf-8') as file:
                schema = safe_load(file)
            texture_filename = f'textures/{tile}.png'
            image = pygame.image.load(texture_filename).convert()
            image = pygame.transform.scale(image, (TILE_SIZE,) * 2)
            self.tiles[tile] = Tile(tile, image)
