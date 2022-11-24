import pygame
from pygame.draw import *
from random import randint
pygame.init()

FPS = 60
screen = pygame.display.set_mode((1000, 750))
screen.fill((255, 255, 255))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


class Ball:
    def __init__(self):
        self.x = randint(100, 900)
        self.y = randint(100, 650)
        self.r = randint(10, 100)
        self.color = COLORS[randint(0, 5)]
        self.life_time = randint(200, 350)
        self.speedx = randint(-10, 10)
        self.speedy = randint(-10, 10)

    def draw_ball(self):
        '''рисует шарик'''
        circle(screen, self.color, (self.x, self.y), self.r)

    def click(self):
        '''попадание'''
        if (event.pos[0] - self.x) ** 2 + (event.pos[1] - self.y) ** 2 <= self.r ** 2:
            return True

    def move(self):
        '''перемещение'''
        if self.x - self.r <= 0 or self.x + self.r >= 1000:
            self.speedx = -self.speedx
        if self.y - self.r <= 0 or self.y + self.r >= 750:
            self.speedy = -self.speedy
        self.x += self.speedx
        self.y += self.speedy


class SpecialTarget:
    def __init__(self):
        self.x = randint(50, 900)
        self.y = randint(50, 650)
        self.length = randint(50, 100)
        self.height = randint(10, 30)
        self.color = COLORS[randint(0, 5)]
        self.centerx = self.x + self.length / 2
        self.centery = self.y + self.height / 2
        self.lifetime = randint(400, 500)
        self.x2 = self.centerx - self.height / 2
        self.y2 = self.centery - self.length / 2
        self.sp_speedx = randint(-10, 10)
        self.sp_speedy = randint(-10, 10)

    def draw_target(self):
        rect(screen, self.color, (self.x, self.y, self.length, self. height))
        rect(screen, self.color, (self.x2, self.y2, self.height, self.length))

    def special_click(self):
        if (event.pos[0] >= self.x and event.pos[0] <= self.x + self.length and event.pos[1] >= self.y
            and event.pos[1] <= self.y + self.height) or (event.pos[0] >= self.x2
                                                          and event.pos[0] <= self.x2 + self.height and
                                                          event.pos[1] >= self.y2 and
                                                          event.pos[1] <= self.y2 + self.length):
            return True

    def sp_move(self):
        self.x += self.sp_speedx
        self.x2 += self.sp_speedx
        self.y += self.sp_speedy
        self.y2 += self.sp_speedy
        if self.x <= 0 or self.x + self.length >= 1000:
            self.sp_speedx *= -1
        if self.y2 <= 0 or self.y2 +self.length >= 750:
            self.sp_speedy *= -1
    def sp_change(self):
        self.sp_speedx = randint(-10, 10)
        self.sp_speedy = randint(-10, 10)




def score():
    '''вывод счета'''
    font = pygame.font.SysFont('arial', 36)
    text = font.render('score: ' + str(sc), True, (255, 0, 0))
    textpos = (10, 10)
    screen.blit(text, textpos)


def balls():
    '''список шариков'''
    l_balls = []
    for i in range(randint(1, 4)):
        l_balls.append(Ball())
    return l_balls


sc = 0


time = 0

sp_time = 0

list_balls = balls()

sp_tg = SpecialTarget()

draw_tg = True

time_spawn = randint(150, 200)

sp_time_spawn = randint(500, 600)

time_speed_change = randint(10, 30)

time_speed = 0


pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    del_balls = []
    score()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
            print('Your score: ', sc)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for x in list_balls:
                if x.click():
                    sc += 1
                    del_balls.append(x)
            if sp_tg.special_click() and draw_tg:
                draw_tg = False
                sc += 2

    time += 1
    sp_time += 1
    time_speed += 1
    for i in range(len(list_balls)):
        list_balls[i].move()
        list_balls[i].life_time -= 1
        if list_balls[i].life_time <= 0:
            del_balls.append(list_balls[i])
    for x in del_balls:
        list_balls.remove(x)
    if time >= time_spawn:
        list_balls.extend(balls())
        time = 0
        time_spawn = randint(150, 200)
    for x in list_balls:
        x.draw_ball()
    if sp_time >= sp_time_spawn:
        draw_tg = True
        sp_tg = SpecialTarget()
        sp_time = 0
        time_speed = 0
        sp_time_spawn = randint(500, 600)
    if time_speed >= time_speed_change:
        sp_tg.sp_change()
        time_speed = 0
        time_speed_change = randint(10, 30)
    sp_tg.sp_move()
    if draw_tg and sp_tg.lifetime >= sp_time:
        sp_tg.draw_target()
    pygame.display.update()
    screen.fill((255, 255, 255))

pygame.quit()
