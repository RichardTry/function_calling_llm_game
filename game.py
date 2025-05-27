import pygame
import pygame_gui
import sys
import random

from consts import *
from character import Character
from model import get_pipeline, get_function
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

    # Создание окна
    screen = pygame.display.set_mode((WIDTH, HEIGHT))#, pygame.FULLSCREEN)
    pygame.display.set_caption("Клеточное поле")
    clock = pygame.time.Clock()

    content = Content('tiles')
    world = World(content.tiles, 5, 4)
    player = Character(0, 0, "textures/player.png")

    # Создание pipeline один раз при запуске
    generation_pipeline = get_pipeline("DiTy/gemma-2-9b-it-russian-function-calling-GGUF")

    time_delta = 0.0
    # Основной игровой цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and event.ui_element == input_box:
                print("CALL FUNCTION:", get_function(generation_pipeline, event.text))
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
