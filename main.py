from typing import Any
from pygame import *
from random import randint
from time import time as timer
init()

W = 635
H = 720

window = display.set_mode((W, H))
display.set_caption("Maze")
display.set_icon(image.load('images/hero_r.png'))

bg = transform.scale(image.load('images/background.jpg'), (W, H))
clock = time.Clock()

font1 = font.SysFont("Arial", 35, bold=True)

class GameSprite(sprite.Sprite):
    # конструктор класу з властивостями
    def __init__(self, img, x, y, width, height, speed):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(img), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    # метод для малювання спрайту
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
            self.image = transform.scale(image.load('images/hero_l.png'), (self.width, self.height))
        if keys_pressed[K_d] and self.rect.x < W - self.width:
            self.rect.x += self.speed
            self.image = transform.scale(image.load('images/hero_r.png'), (self.width, self.height))
        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.x < H - self.height:
            self.rect.y += self.speed
        
class Wall(sprite.Sprite):
    def __init__(self, color1, color2, color3, width, height, x, y):
        super().__init__()
        self.color1 = color1
        self.color2 = color2
        self.color3 = color3
        self.width = width
        self.height = height
        self.image = Surface((self.width, self.height))
        self.image.fill((self.color1, self.color2, self.color3))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Enemy(GameSprite):
    direction = 'right'
    def update_r_l(self, start, end):
        if self.direction == 'right':
            self.rect.x += self.speed
        if self.direction == 'left':
            self.rect.x -= self.speed

        if self.direction == 'right' and self.rect.x >= end:
            self.direction = 'left'
            self.image = transform.scale(image.load('images/cyborg_l.png'), (self.width, self.height))
        if self.direction == 'left' and self.rect.x <= start:
            self.direction = 'right'
            self.image = transform.scale(image.load('images/cyborg_r.png'), (self.width, self.height))



player = Player("images/hero_r.png", 40, 40, 50, 50, 4)
enemy1 = Enemy('images/cyborg_r.png', 270, 570, 50, 50, 5)
enemy2 = Enemy('images/cyborg_r.png', 130, 180, 50, 50, 5)
coin1 = GameSprite('images/treasure.png', 200, 70, 50, 50, 0)
key1 = GameSprite('images/treasure.png', 100, 500, 50, 50, 0)
treasure1 = GameSprite('images/treasure.png', 520, 655, 50, 50, 0)


walls = sprite.Group()
#(color1, color2, color3, width, height, x, y)
wall1 = Wall(97, 139, 51, 15, 500, 20, 140)
wall2 = Wall(97, 139, 51, 445, 15, 20, 420)
wall3 = Wall(97, 139, 51, 350, 15, 100, 340)
wall4 = Wall(97, 139, 51, 15, 320, 100, 20)
wall5 = Wall(97, 139, 51, 15, 320, 100, 20)
wall6 = Wall(97, 139, 51, 450, 15, 20, 630)
wall7 = Wall(97, 139, 51, 15, 320, 600, 20)
wall8 = Wall(97, 139, 51, 300, 15, 100, 20)
wall9 = Wall(97, 139, 51, 300, 15, 300, 20)
wall10 = Wall(97, 139, 51, 15, 200, 20, 20)
wall11 = Wall(97, 139, 51, 100, 15, 20, 20)
wall12 = Wall(97, 139, 51, 15, 345, 600, 300)
wall13 = Wall(97, 139, 51, 15, 100, 340, 30)
wall14 = Wall(97, 139, 51, 15, 150, 450, 205)
wall15 = Wall(97, 139, 51, 15, 120, 230, 420)
wall16 = Wall(97, 139, 51, 15, 90, 230, 540)#двері 1
wall17 = Wall(97, 139, 51, 130, 15, 470, 630)#двері 2

walls_lst = [wall1, wall2, wall3, wall4, wall5, wall6, wall7, wall8, wall9, wall10, wall11, wall12, wall13, wall14, wall15, wall16, wall17]
walls = sprite.Group()
for wall in walls_lst:
    walls.add(wall)

finish = False 
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
    
    if finish is False:
        window.blit(bg, (0, 0))
        player.reset()
        player.update()

        walls.draw(window)

        enemy1.reset()
        enemy1.update_r_l(270, 550)

        enemy2.reset()
        enemy2.update_r_l(130, 380)

        coin1.reset()

        key1.reset()

        treasure1.reset()


        if sprite.collide_rect(player, enemy1) or sprite.collide_rect(player, enemy2):
            player.rect.x = 40
            player.rect.y = 40
        if sprite.spritecollide(player, walls, False):
            player.rect.x = 40
            player.rect.y = 40
        if sprite.collide_rect(player, coin1):
            walls.remove(wall16)
            coin1.rect.y = -200
        if sprite.collide_rect(player, key1):
            walls.remove(wall17)
            key1.rect.y = -200
        if sprite.collide_rect(player, treasure1):
            wins = font1.render('WIN', True, (0, 255, 0))
            window.blit(wins, (280, H / 2))
            finish = True
            
    else:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_r]:
            finish = False
            player.rect.x = 40
            player.rect.y = 40
            coin1.rect.y = 70
            key1.rect.y = 500
            walls.add(wall16, wall17)
            

        

    clock.tick(60)
    display.update()