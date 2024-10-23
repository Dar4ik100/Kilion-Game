from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load("girly.png"), (65, 65))
        if keys[K_RIGHT] and self.rect.x < wd - 80:
            self.rect.x += self.speed
            self.image = transform.scale(image.load("girly_2.png"), (65, 65))
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < hgt - 80:
            self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Розміри вікна
wd = 1000
hgt = 900

# Налаштовуємо вікно Pygame
window = display.set_mode((wd, hgt))
display.set_caption("Kilion Game")

# Завантажуємо фон (необов'язково)
bag = transform.scale(image.load("fon_purp.png"), (wd, hgt))

# Гравець
player = Player("girly.png", 5, 5, 4)

# Масив лабіринту: 1 - стіна, 0 - прохід
maze = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    [1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 1],
    [1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1],
    [1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

# Розміри кожної комірки
cell_size = wd // len(maze[0])

# wall_width = cell_size // 8
# wall_height = cell_size

wall_width = cell_size  # Ширина залишається як була
wall_height = cell_size // 8  # Висота буде в 4 рази менша

# Створення стін з масиву лабіринту
walls = []
for y, row in enumerate(maze):
    for x, col in enumerate(row):
        if col == 1:  # якщо це стіна
            wall = Wall(0, 0, 0, x * cell_size+10, y * cell_size, wall_width, wall_height)
            walls.append(wall)  # додаємо стіну до масиву

# Основний цикл гри
game = True
finish = False
clock = time.Clock()
fps = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if not finish:
        window.blit(bag, (0, 0))
        player.update()
        player.reset()

        # Малюємо всі стіни
        for wall in walls:
            wall.draw_wall()

    display.update()
    clock.tick(fps)
