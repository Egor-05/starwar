# -*- coding: utf8 -*-

import pygame
import random
import os


scr_size_x = 750    # размер окна по х
scr_size_y = 500    # размер окна по у
image_dir = os.path.dirname(__file__) + "/img/"  # путь к каталогу с изображениями
speed = 10  # скорость корабля
ekilled = 0
i = scr_size_y // 10 / 8
number = 0


class ClObj:
    def __init__(self, x, vel):
        self.x = x
        self.vel = vel

    def draw(self):
        pass

    def fly(self):
        self.y += self.vel


# класс для определения корабля
class ClShip(ClObj):
    def __init__(self, x, y, vel):
        ClObj.__init__(self, x, vel)
        self.y = y

    def draw(self, win):
        win.blit(ship_sprite, (self.x, self.y))

    def up(self):
        if self.y > 5:
            self.y -= self.vel

    def down(self):
        if self.y < scr_size_y - ship_sprite.get_height():
            self.y += self.vel

    def left(self):
        if self.x > 5:
            self.x -= self.vel

    def right(self):
        if self.x < scr_size_x - ship_sprite.get_width():
            self.x += self.vel


# класс для определения звёзд
class ClStar(ClObj):

    def __init__(self, x, radius, color):
        ClObj.__init__(self, x, random.randint(3, 10))
        self.y = 0
        self.radius = radius
        self.color = color

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# класс для определения врага
class ClEnemy(ClObj):

    def __init__(self, x):
        ClObj.__init__(self, x, 6)
        self.y = 0

    def draw(self, win):    # отрисовка
        # pygame.draw.rect(win, self.color,(self.x - 15, self.y - 15, 30, 30))
        win.blit(enemy_sprite, (self.x - enemy_sprite.get_width() // 2,
                                self.y - enemy_sprite.get_height() // 2))

    def check(self, x, y):    # проверяет пересечение с точкой по переданным координатам
        if (x >= self.x - enemy_sprite.get_width() // 2) and \
           (x <= self.x + enemy_sprite.get_width() // 2) and \
           (y >= self.y - enemy_sprite.get_height() // 2) and \
           (y <= self.y + enemy_sprite.get_height() // 2):
            return True
        else:
            return False


# класс для определения пуль
class ClBullet(ClObj):
    def __init__(self, x, y, radius, color):
        ClObj.__init__(self, x, -10)
        self.y = y
        self.radius = radius
        self.color = color
        self.number = 0

    def draw(self, win):
        if self.number == 8 * i - 1:
            self.number = 0
        else:
            self.number += 1
        shoot = shoots[int(self.number//i)]
        win.blit(shoot, (self.x - shoot.get_width() // 2, self.y - shoot.get_height() // 2))


# инициализация всего
def initAll():
    pygame.init()
    win = pygame.display.set_mode((scr_size_x, scr_size_y))     # объект окно
    pygame.display.set_caption("Starwars by Egor")
    return win


def fly_obj(arr_obj):
    for obj in arr_obj:
        if scr_size_y >= obj.y >= 0:
            obj.fly()
            obj.draw(win)
        else:
            arr_obj.pop(arr_obj.index(obj))


exps = []
shoots = []     # массив спрайтов выстрелов
# основная программа
win = initAll()
ship_img = pygame.image.load(image_dir + 'kosmolet.png')    # изображене корабля
enemy_img = pygame.image.load(image_dir + 'enemy.png')      # изображене врага
for counter in range(8):
    shoot_img = pygame.image.load(image_dir + 'fire' + str(counter + 1) + '.png')
    shoot_spr = pygame.transform.scale(shoot_img, (shoot_img.get_width() // 2,
                                        shoot_img.get_height() // 2))
    shoots.append(pygame.transform.rotate(shoot_spr, 90))  # спрайт пули
for counter in range(8):
    exp_img = pygame.image.load(image_dir + 'exp' + str(counter + 1) + '.png')
    exp_spr = pygame.transform.scale(exp_img, (exp_img.get_width() // 2,
                                        exp_img.get_height() // 2))
    exps.append(exp_spr)    # спрайт взрыва
# explosion_img = pygame.image.load(image_dir + 'explosion.png')      # изображене взрыва

ship_sprite = pygame.transform.scale(ship_img, (ship_img.get_width() // 40,   # спрайт корабля
                                        ship_img.get_height() // 40))
enemy_sprite = pygame.transform.scale(enemy_img, (enemy_img.get_width() // 9,
                                        enemy_img.get_height() // 9))     # спрайт врага
bullets = []    # массив объектов пуль
stars = []      # массив объектов звёзд
enemies = []    # массив объектов врагов
cycle_counter = 0   # счётчик циклов, используется для вызова паузы между выстрелами
run = True      # признак продолжения работы программы
ship = ClShip(scr_size_x / 2, scr_size_y - 50, speed)
while run:
    pygame.time.delay(100)
    cycle_counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((0, 0, 0))

    if len(stars) < 35:
        stars.append(ClStar(random.randint(0, scr_size_x),
                            random.randint(1, 5), (255, 255, 0)))

    if len(enemies) < 3:
        enemies.append(ClEnemy(random.randint(0, scr_size_x)))

    for bullet in bullets:
        for enemy in enemies:
            if enemy.check(bullet.x, bullet.y):
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(enemy))
                ekilled += 1

    fly_obj(stars)
    fly_obj(enemies)
    fly_obj(bullets)

    for enemy in enemies:
        if enemy.check(ship.x, ship.y):
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ship.left()
    if keys[pygame.K_RIGHT]:
        ship.right()
    if keys[pygame.K_UP]:
        ship.up()
    if keys[pygame.K_DOWN]:
        ship.down()
    if keys[pygame.K_SPACE]:
        if len(bullets) < 10 and cycle_counter > 5:
            cycle_counter = 0
            bullets.append(ClBullet(ship.x + ship_sprite.get_width() // 2,
                                    ship.y + ship_sprite.get_height() // 2,
                                    3, (0, 0, 255)))

    f2 = pygame.font.Font(None, 36)
    text2 = f2.render(str(ekilled), 1, (255, 255, 255))
    win.blit(text2, (50, 50))
    ship.draw(win)

    pygame.display.update()

for counter in range(8):
    exp_spr = exps[counter]
    exp_rect = win.blit(exp_spr, (ship.x - exp_spr.get_width() // 2,
                                  ship.y - exp_spr.get_height() // 2))
    pygame.display.update(exp_rect)
    pygame.time.delay(300)
    exp_spr.fill((0, 0, 0))
    exp_rect = win.blit(exp_spr, (ship.x - exp_spr.get_width() // 2,
                                  ship.y - exp_spr.get_height() // 2))
    pygame.display.update(exp_rect)

f1 = pygame.font.Font(None, 36)
text1 = f1.render('Game Over', 1, (255, 255, 255))
win.blit(text1, (scr_size_x // 2, scr_size_y // 2))
pygame.display.update()

pygame.time.delay(1000)
pygame.quit()
