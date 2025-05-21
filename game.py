import pygame
import pygame_gui
import sys
import random

from consts import *
from player import Player
from generate import generate_map

from model import generation_pipeline

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

def draw_input_box(screen, input_active, input_box, input_text, input_color, input_font):
    # Отрисовка текстового поля
    pygame.draw.rect(screen, input_color, input_box, 2)
    text_surface = input_font.render(input_text, True, (255, 255, 255))
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    if input_active:
        # Отрисовка курсора
        pygame.draw.rect(screen, input_color, (input_box.x + text_surface.get_width() + 10, input_box.y + 5, 2, 30))

def main():
    # Инициализация Pygame
    pygame.init()

    manager = pygame_gui.UIManager((800, 600))

    input_box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((50, 500), (700, 40)),
        manager=manager
    )

    print(generate_map(3, 3))

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Клеточное поле")
    clock = pygame.time.Clock()

    # Загрузка изображений тайлов
    tiles = load_images()
    player = Player(0, 0, "textures/player.png")

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

    time_delta = 0.0
    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == input_box:
                print("Ввод:", event.text)
                input_box.set_text("")
            manager.process_events(event)


        keys = pygame.key.get_pressed()
        player.move(keys)

        manager.update(time_delta)
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
        player.draw(screen)

        manager.draw_ui(screen)

        pygame.display.flip()  # Обновление экрана
        time_delta = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()
