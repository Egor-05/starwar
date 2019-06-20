#!/usr/bin/python
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

# класс для определения звёзд
class cl_star():

    def __init__(self, x, radius, color):
        self.x = x
        self.y = 0
        self.radius = radius
        self.color = color
        self.vel = random.randint(3, 10)

    def draw(self, win):
        pygame.draw.circle(win, self.color, (self.x, self.y), self.radius)


# класс для определения врага
class cl_enemy():

    def __init__(self, x):
        self.x = x
        self.y = 0
        self.vel = 6

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


#class cl_ebullet():
 #   def __init__(self, x, y, radius, color, facing):
  #      self.x = x
   #     self.y = y
    #    self.radius = radius
     #   self.color = color
      #  self.facing = facing
       # self.vel = 10 * facing
        #def draw(self, win):
        #pygame.draw.circle(win, self.color,(self.x, self.y), self.radius )


# класс для определения пуль
class cl_bullet():
    def __init__(self, x, y, radius, color, facing):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.facing = facing
        self.vel = 10 * facing
        self.number = 0

    def draw(self, win):
        if self.number == 8*i-1:
            self.number = 0
        else:
            self.number += 1
        win.blit(shoots[self.number//i], (self.x - shoots[self.number//i].get_width() // 2,
                                 self.y - shoots[self.number//i].get_height() // 2))

#    def size(self):
#        return {'w':shoot3_sprite.get_width(),'h':shoot3_sprite.get_height()}


# инициализация всего
def initAll():
    pygame.init()
    win = pygame.display.set_mode((scr_size_x, scr_size_y))     # объект окно
    pygame.display.set_caption("Starwars by Egor")
    return win


# обновление окна и корабля
def drawWindow(explode):
    if explode:
        win.blit(explosion_sprite, (x, y))
    else:
        win.blit(ship_sprite, (x, y))
    pygame.display.update()


shoots = []     # массив спрайтов выстрелов
#основная программа
win = initAll()
ship_img = pygame.image.load(image_dir + 'kosmolet.png')    # изображене корабля
enemy_img = pygame.image.load(image_dir + 'enemy.png')      # изображене врага
for counter in range(8):
    shoot_img = pygame.image.load(image_dir + 'fire' + str(counter + 1) + '.png')
    shoot_spr = pygame.transform.scale(shoot_img, (shoot_img.get_width() // 2,
                                        shoot_img.get_height() // 2))
    shoots.append(pygame.transform.rotate(shoot_spr, 90))    # спрайт пули
explosion_img = pygame.image.load(image_dir + 'explosion.png')      # изображене взрыва

ship_sprite = pygame.transform.scale(ship_img, (ship_img.get_width() // 40,   # спрайт корабля
                                        ship_img.get_height() // 40))
enemy_sprite = pygame.transform.scale(enemy_img, (enemy_img.get_width() // 9,
                                        enemy_img.get_height() // 9))     # спрайт врага
explosion_sprite = pygame.transform.scale(explosion_img, (explosion_img.get_width() // 10,
                                        explosion_img.get_height() // 10))    # спрайт взрыва
x = scr_size_x / 2      # текущая координата х корабля
y = scr_size_y - 50     # текущая координата у корабля
#ebullets = []
bullets = []    # массив объектов пуль
stars = []      # массив объектов звёзд
enemies = []    # массив объектов врагов
cycle_counter = 0   # счётчик циклов, используется для вызова паузы между выстрелами
run = True      # признак продолжения работы программы
exp = False     # признак изменения спрайта корабля
while run:
    pygame.time.delay(100)
    cycle_counter += 1
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for star in stars:
        if star.y <= scr_size_y and star.y >= 0:
            star.y += star.vel
        else:
            stars.pop(stars.index(star))

    for enemy in enemies:
        if enemy.y <= scr_size_y and enemy.y >= 0:
            enemy.y += enemy.vel
        else:
            enemies.pop(enemies.index(enemy))

    if len(stars) < 35:
        stars.append(cl_star(random.randint(0, scr_size_x),
                             random.randint(1, 5), (255, 255, 0)))

    if len(enemies) < 3:
        enemies.append(cl_enemy(random.randint(0, scr_size_x)))

    for bullet in bullets:
        if bullet.y < scr_size_y and bullet.y > 0:
            bullet.y += bullet.vel
        else:
            bullets.pop(bullets.index(bullet))

    for bullet in bullets:
        for enemy in enemies:
            if enemy.check(bullet.x, bullet.y):
                bullets.pop(bullets.index(bullet))
                enemies.pop(enemies.index(enemy))
                ekilled += 1

    for enemy in enemies:
        if enemy.check(x, y):
            exp = True
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x > 5:
        x -= speed
    if keys[pygame.K_RIGHT] and x < scr_size_x - ship_sprite.get_width():
        x += speed
    if keys[pygame.K_UP] and y > 5:
        y -= speed
    if keys[pygame.K_DOWN] and y < scr_size_y - ship_sprite.get_height():
        y += speed
    if keys[pygame.K_SPACE]:
        facing = -1
        if len(bullets) < 10 and cycle_counter > 5:
            cycle_counter = 0
            bullets.append(cl_bullet(x + ship_sprite.get_width() // 2,
                                     y + ship_sprite.get_height() // 2,
                                     3, (0, 0, 255), facing))

    win.fill((0, 0, 0))

    for bullet in bullets:
        bullet.draw(win)

    for star in stars:
        star.draw(win)

    for enemy in enemies:
        enemy.draw(win)
    f2 = pygame.font.Font(None, 36)
    text2 = f2.render(str(ekilled), 1, (255, 255, 255))
    win.blit(text2, (50, 50))
    drawWindow(exp)


f1 = pygame.font.Font(None, 36)
text1 = f1.render('Game Over', 1, (255, 255, 255))
win.blit(text1, (scr_size_x // 2, scr_size_y // 2))
pygame.display.update()

pygame.time.delay(1000)
pygame.quit()