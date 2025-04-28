import pygame
import sys
import random

# Константы
WIDTH, HEIGHT = 1920, 1080
TILE_SIZE = 40
GRID_WIDTH = WIDTH // TILE_SIZE
GRID_HEIGHT = HEIGHT // TILE_SIZE
PLAYER_COLOR = (0, 255, 0)  # Зеленый цвет для игрока
BACKGROUND_COLOR = (0, 0, 0)  # Черный цвет фона

# Определяем классы для типов тайлов
class Tile:
    def __init__(self, tile_type, image):
        self.tile_type = tile_type
        self.image = image

    def draw(self, surface, x, y):
        surface.blit(self.image, (x * TILE_SIZE, y * TILE_SIZE))

# Функция для загрузки изображений
def load_images():
    res = {}
    for tile in ('grass', 'water', 'dirt', 'castle'):
        image = pygame.transform.scale(pygame.image.load(f'textures/{tile}.png').convert(), (TILE_SIZE,) * 2)
        res[tile] = Tile(tile, image)
    return res

def main():
    # Инициализация Pygame
    pygame.init()

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Клеточное поле")
    clock = pygame.time.Clock()

    # Загрузка изображений тайлов
    tiles = load_images()
    player = pygame.transform.scale(pygame.image.load('textures/player.png').convert_alpha(), (TILE_SIZE,) * 2)

    # Создаем сетку тайлов (пример 10x15)
    choices = ['grass', 'grass', 'water', 'castle']
    probabilities = [0.5, 0.3, 0.1, 0.01]
    grid = []
    for y in range(HEIGHT // TILE_SIZE):
        grid.append([])
        for x in range(WIDTH // TILE_SIZE):
            grid[y].append(random.choices(choices, weights=probabilities, k=1)[0])
    # grid = [
    #     ['grass', 'grass', 'water', 'water', 'grass'] * 2,
    #     ['grass', 'dirt', 'dirt', 'water', 'grass'] * 2,
    #     ['grass', 'grass', 'grass', 'grass', 'grass']* 2,
    #     ['water', 'water', 'water', 'water', 'water']* 2,
    #     ['dirt', 's', 'grass', 'grass', 'grass']* 2,
    # ]

    # Начальная позиция игрока
    player_x, player_y = 0, 0

    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 1
        if keys[pygame.K_DOWN] and player_y < GRID_HEIGHT - 1:
            player_y += 1
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 1
        if keys[pygame.K_RIGHT] and player_x < GRID_WIDTH - 1:
            player_x += 1

        # Отрисовка поля
        screen.fill(BACKGROUND_COLOR)

        # Отрисовка тайлов
        for y in range(len(grid)):
            for x in range(len(grid[y])):
                tile_type = grid[y][x]
                tile = tiles[tile_type]
                tile.draw(screen, x, y)
        
        # for y in range(GRID_HEIGHT):
        #     for x in range(GRID_WIDTH):
        #         rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        #         pygame.draw.rect(screen, (255, 255, 255), rect, 1)  # Рисуем клетки (белые линии)

        # Отрисовка игрока
        player_rect = pygame.Rect(player_x * TILE_SIZE, player_y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        screen.blit(player, (player_x * TILE_SIZE, player_y * TILE_SIZE))
        # pygame.draw.rect(screen, PLAYER_COLOR, player_rect)  # Рисуем игрока

        pygame.display.flip()  # Обновление экрана
        clock.tick(60)

if __name__ == "__main__":
    main()
