from pygame import *
import random


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_x_size, player_y_size))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self, walls):
        keys = key.get_pressed()
        old_x, old_y = self.rect.x, self.rect.y  # Збереження старого положення для відкату при зіткненні

        # Перевірка натискання клавіш і рух
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load("girly.png"), (player_x_size, player_y_size))
        if keys[K_RIGHT] and self.rect.x < wd - 80:
            self.rect.x += self.speed
            self.image = transform.scale(image.load("girly_2.png"), (player_x_size, player_y_size))
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < hgt - 80:
            self.rect.y += self.speed

        # Перевірка зіткнень зі стінами
        for wall in walls:
            if self.rect.colliderect(wall.rect):
                # Якщо зіткнення, повертаємо гравця на стару позицію
                self.rect.x, self.rect.y = old_x, old_y
                break


class Wall(sprite.Sprite):
    def __init__(self, color, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.image = Surface((wall_width, wall_height))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Door(GameSprite):

    def draw_door(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Розміри вікна
wd = 900
hgt = 700
cell_size = 50  # Розмір клітини для побудови лабіринту
wall_thickness = 5  # Товщина стінок лабіринту
player_x_size = 40
player_y_size = 40
door = Door("dor_cl.png",850,650,0)

cols = wd // cell_size  # Кількість стовпців
rows = hgt // cell_size  # Кількість рядків

# Налаштування вікна Pygame
window = display.set_mode((wd, hgt))
display.set_caption("Kilion Game")

# Завантаження фону
bag = transform.scale(image.load("fon_purp.png"), (wd, hgt))

# Генерація лабіринту з використанням DFS
maze = [[1 for _ in range(cols)] for _ in range(rows)]


def generate_maze(x, y):
    maze[y][x] = 0
    directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    random.shuffle(directions)

    for dx, dy in directions:
        nx, ny = x + dx * 2, y + dy * 2
        if 0 <= nx < cols and 0 <= ny < rows and maze[ny][nx] == 1:
            maze[y + dy][x + dx] = 0
            generate_maze(nx, ny)


generate_maze(0, 0)


# Функція для пошуку випадкової вільної клітини
def find_random_empty_cell():
    empty_cells = [(x, y) for y in range(rows) for x in range(cols) if maze[y][x] == 0]
    return random.choice(empty_cells)


# Встановлення гравця в випадковій вільній клітині
start_x, start_y = find_random_empty_cell()
player = Player("girly.png", start_x * cell_size, start_y * cell_size, 4)

# Створення вузьких стін для кожної межі клітин лабіринту
walls = []
for y in range(rows):
    for x in range(cols):
        if maze[y][x] == 1:
            if y > 0 and maze[y - 1][x] == 0:  # Верхня стіна
                wall = Wall((0, 0, 0), x * cell_size, y * cell_size, cell_size, wall_thickness)
                walls.append(wall)
            if x > 0 and maze[y][x - 1] == 0:  # Ліва стіна
                wall = Wall((0, 0, 0), x * cell_size, y * cell_size, wall_thickness, cell_size)
                walls.append(wall)

# Основний ігровий цикл
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
        player.update(walls)
        player.reset()
        door.draw_door()

        # Малюємо всі стіни
        for wall in walls:
            wall.draw_wall()

    display.update()
    clock.tick(fps)
