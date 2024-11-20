from pygame import *

def start_level_2():
    # Ініціалізація Pygame та налаштування параметрів вікна
    init()
    wd, hgt = 950, 750
    window = display.set_mode((wd, hgt))
    display.set_caption("Kilion Game | Level 2")

    # Завантаження фону
    bg_image = transform.scale(image.load("fon_purp.png"), (wd, hgt))

    # Властивості гравця
    player_size = 40
    player_image = transform.scale(image.load("girly.png"), (player_size, player_size))
    player_x, player_y = wd // 2, hgt - player_size
    player_speed = 5
    jump_power = 15
    gravity = 1
    is_jumping = False
    y_velocity = 0

    # Платформи (паркур)
    platforms = [
        Rect(100, 600, 200, 20),
        Rect(400, 500, 150, 20),
        Rect(700, 400, 200, 20),
        Rect(300, 300, 150, 20),
        Rect(600, 200, 200, 20),
    ]
    platform_color = (0, 100, 255)  # Синій колір платформ

    # Основний ігровий цикл для рівня 2
    game = True
    clock = time.Clock()
    fps = 60

    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False

        # Отримання натискань клавіш
        keys = key.get_pressed()

        # Рух гравця ліворуч і праворуч
        if keys[K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[K_RIGHT] and player_x < wd - player_size:
            player_x += player_speed

        # Стрибок гравця
        if not is_jumping and keys[K_SPACE]:
            is_jumping = True
            y_velocity = -jump_power

        # Реалізація гравітації
        if is_jumping:
            player_y += y_velocity
            y_velocity += gravity
            if player_y >= hgt - player_size:
                player_y = hgt - player_size
                is_jumping = False
                y_velocity = 0

        # Перевірка зіткнень з платформами
        player_rect = Rect(player_x, player_y, player_size, player_size)
        for platform in platforms:
            if player_rect.colliderect(platform) and y_velocity > 0:
                player_y = platform.top - player_size
                is_jumping = False
                y_velocity = 0

        # Малювання елементів
        window.blit(bg_image, (0, 0))  # Фон
        for platform in platforms:
            draw.rect(window, platform_color, platform)  # Платформи
        window.blit(player_image, (player_x, player_y))  # Гравець

        display.update()
        clock.tick(fps)
