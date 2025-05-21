import pygame

from consts import TILE_SIZE, GRID_HEIGHT, GRID_WIDTH


class Player:
    def __init__(self, x, y, image):
        self.x = x
        self.y = y
        self.image = pygame.transform.scale(pygame.image.load(image).convert_alpha(), (TILE_SIZE,) * 2)

        self.speed = 10000
        self.move_delay = 1 / self.speed
        self.move_delay = 0
        print(self.move_delay)
        self.last_move_time = 0

    def move(self, keys):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < self.move_delay:
            return  # Ещё не прошло достаточно времени

        MIN_MOVE = 0.1
        moved = False
        if keys[pygame.K_UP] and self.y > MIN_MOVE:
            self.y -= MIN_MOVE
            moved = True
        elif keys[pygame.K_DOWN] and self.y < GRID_HEIGHT - MIN_MOVE:
            self.y += MIN_MOVE
            moved = True
        elif keys[pygame.K_LEFT] and self.x > MIN_MOVE:
            self.x -= MIN_MOVE
            moved = True
        elif keys[pygame.K_RIGHT] and self.x < GRID_WIDTH - MIN_MOVE:
            self.x += MIN_MOVE
            moved = True

        if moved:
            self.last_move_time = current_time

    def draw(self, surface):
        surface.blit(self.image, (self.x * TILE_SIZE, self.y * TILE_SIZE))
