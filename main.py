from pygame import *

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed):
        super().__init__()

        self.image = transform.scale(image.load(player_image),(65,65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load("girly.png"), (65, 65))
        if keys[K_RIGHT] and self.rect.x < wd-80:
                self.rect.x += self.speed
                self.image = transform.scale(image.load("girly_2.png"),(65,65))
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < wd-80:
                self.rect.y += self.speed

class Wall(sprite.Sprite):
    def __init__(self,color_1,color_2,color_3,wall_x,wall_y,wall_width,wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.wall_height = wall_height
        self.wall_width = wall_width
        self.image = Surface((self.wall_width,self.wall_height))
        self.image.fill((color_1,color_2,color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y

    def draw_wall(self):
        window.blit(self.image,(self.rect.x,self.rect.y))

wd = 1500
hgt = 1200

window = display.set_mode((wd,hgt))
display.set_caption("Kilion")
bag = transform.scale(image.load("fon_purp.png"),(wd,hgt))
player = Player("girly.png",5,50,4)


game = True
finish = False
clock = time.Clock()
fps = 60

while game:
    for e in event.get():
        if e.type == QUIT:
            game = False

    if finish != True:

        window.blit(bag,(0,0))
        player.update()
        player.reset()


    display.update()
    clock.tick(fps)

