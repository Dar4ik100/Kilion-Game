# lvl2.py
from pygame import *


def start_level_2():
    # Ініціалізація Pygame, налаштування вікна та інші параметри
    init()
    wd, hgt = 950, 750
    window = display.set_mode((wd, hgt))
    display.set_caption("Kilion Game | Level 2")

    # Тут код для гри на другому рівні
    # ...

    # Основний цикл гри на рівні 2
    game = True
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False

        # Тут ваша логіка гри на другому рівні
        window.fill((0, 0, 0))  # Очистка екрану
        display.update()  # Оновлення вікна


