import pygame
from pygame import *
import random
from lvl_2 import *

# Ініціалізація Pygame
pygame.init()
mixer.init()
mixer.music.load("funny_game.mp3")
mixer.music.play(-1)
mixer.music.set_volume(0.2)

# Розміри вікна
wd = 950
hgt = 750
cell_size = 50
wall_thickness = 5
player_x_size = 40
player_y_size = 40

# Налаштування вікна Pygame
window = display.set_mode((wd, hgt))
display.set_caption("Kilion Game | Level 1")

# Завантаження фону
bag = transform.scale(image.load("fon_purp.png"), (wd, hgt))
menu_bg = transform.scale(image.load("fon_purp.png"), (wd, hgt))


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
        old_x, old_y = self.rect.x, self.rect.y

        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load("girly.png"), (player_x_size, player_y_size))
        if keys[K_RIGHT] and self.rect.x < wd - player_x_size:
            self.rect.x += self.speed
            self.image = transform.scale(image.load("girly_2.png"), (player_x_size, player_y_size))
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < hgt - player_y_size:
            self.rect.y += self.speed

        for wall in walls:
            if self.rect.colliderect(wall.rect):
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


class Door(sprite.Sprite):
    def __init__(self, dor_img, dor_w, dor_h, dor_x, dor_y):
        super().__init__()
        self.image = transform.scale(image.load(dor_img), (dor_w, dor_h))
        self.rect = self.image.get_rect()
        self.rect.x = dor_x
        self.rect.y = dor_y

    def draw_door(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Key(sprite.Sprite):
    def __init__(self, key_img, key_w, key_h, key_x, key_y):
        super().__init__()
        self.image = transform.scale(image.load(key_img), (key_w, key_h))
        self.rect = self.image.get_rect()
        self.rect.x = key_x
        self.rect.y = key_y
        self.collected = False

    def draw_key(self):
        if not self.collected:
            window.blit(self.image, (self.rect.x, self.rect.y))


# Генерація лабіринту з використанням DFS
cols = wd // cell_size
rows = hgt // cell_size
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


def find_random_empty_cell():
    empty_cells = [(x, y) for y in range(rows) for x in range(cols) if maze[y][x] == 0]
    return random.choice(empty_cells)


# Встановлення гравця, дверей і ключа в випадкових клітинах
def reset_level():
    global player, key_l, door, finish
    start_x, start_y = find_random_empty_cell()
    player = Player("girly.png", start_x * cell_size, start_y * cell_size, 4)

    door_x, door_y = find_random_empty_cell()
    door = Door("dor_cl.png", 50, 50, door_x * cell_size, door_y * cell_size)

    key_x, key_y = find_random_empty_cell()
    key_l = Key("key.png", 30, 40, key_x * cell_size, key_y * cell_size)
    finish = False


reset_level()

walls = []
for y in range(rows):
    for x in range(cols):
        if maze[y][x] == 1:
            if y > 0 and maze[y - 1][x] == 0:
                wall = Wall((0, 0, 0), x * cell_size, y * cell_size, cell_size, wall_thickness)
                walls.append(wall)
            if x > 0 and maze[y][x - 1] == 0:
                wall = Wall((0, 0, 0), x * cell_size, y * cell_size, wall_thickness, cell_size)
                walls.append(wall)


# Функція для відображення меню
def show_menu():
    menu_open = True
    while menu_open:
        window.blit(menu_bg, (0, 0))

        font = pygame.font.Font(None, 80)
        continue_text = font.render("Continue", True, (255, 255, 255))
        reset_text = font.render("Reset", True, (255, 255, 255))
        exit_text = font.render("Exit", True, (255, 0, 0))

        continue_rect = continue_text.get_rect(center=(wd // 2, hgt // 2 - 100))
        reset_rect = reset_text.get_rect(center=(wd // 2, hgt // 2))
        exit_rect = exit_text.get_rect(center=(wd // 2, hgt // 2 + 100))

        window.blit(continue_text, continue_rect)
        window.blit(reset_text, reset_rect)
        window.blit(exit_text, exit_rect)

        for e in event.get():
            if e.type == QUIT:
                quit()
            elif e.type == MOUSEBUTTONDOWN:
                if continue_rect.collidepoint(e.pos):
                    menu_open = False
                elif reset_rect.collidepoint(e.pos):
                    reset_level()
                    menu_open = False
                elif exit_rect.collidepoint(e.pos):
                    quit()
            elif e.type == KEYDOWN and e.key == K_ESCAPE:
                menu_open = False
        display.update()


# Основний ігровий цикл

game = True
finish = False
clock = time.Clock()
fps = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            show_menu()

    if not finish:
        window.blit(bag, (0, 0))
        player.update(walls)
        door.draw_door()
        key_l.draw_key()
        player.reset()

        if player.rect.colliderect(key_l.rect) and not key_l.collected:
            key_l.collected = True
            door.image = transform.scale(image.load("dor_op.png"), (50, 50))

        if player.rect.colliderect(door.rect) and key_l.collected:
            finish = True
            start_level_2()

        for wall in walls:
            wall.draw_wall()

    display.update()
    clock.tick(fps)


