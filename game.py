import pygame
import pygame_gui
import sys
import random

from consts import *
from player import Player
from generate import generate_map
# from model import get_function
from content import Content
from world import World


def main():
    # Инициализация Pygame
    pygame.init()
    manager = pygame_gui.UIManager((800, 600))

    input_box = pygame_gui.elements.UITextEntryLine(
        relative_rect=pygame.Rect((50, 500), (700, 40)),
        manager=manager
    )

    # print(generate_map(3, 3))

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Клеточное поле")
    clock = pygame.time.Clock()

    content = Content('tiles')
    world = World(content.tiles, 5, 4)
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
                print("CALL FUNCTION:", get_function(event.text))
                input_box.set_text("")
            manager.process_events(event)


        keys = pygame.key.get_pressed()
        player.move(keys)

        manager.update(time_delta)
        screen.fill(BACKGROUND_COLOR)

        world.draw(screen)
        # Отрисовка игрока
        player.draw(screen)

        manager.draw_ui(screen)

        pygame.display.flip()  # Обновление экрана
        time_delta = clock.tick(60) / 1000.0

if __name__ == "__main__":
    main()
