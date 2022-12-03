import pygame
import math
from random import choice
from random import randint as rnd
pygame.init()

FPS = 60

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1000
HEIGHT = 700


def main():
    class Ball:
        def __init__(self, angle):
            self.x = gun.x + 50 + 74 * math.cos(angle)
            self.y = gun.y + 77 + 74 * math.sin(angle)
            self.r = 10
            self.vx = 0
            self.vy = 0
            self.color = choice(GAME_COLORS)
            self.lifetime = 40

        def move(self):
            'движение шара после выстрела'
            self.x += self.vx
            self.y += self.vy
            if self.x <= 10:
                self.vx = abs(self.vx)
            if self.x >= 990:
                self.vx = -abs(self.vx)
            if self.y >= 670:
                self.vy = -abs(self.vy)

        def move_with_gun(self, angle):
            'движение шара до выстрела'
            self.x = gun.x + 50 + 74 * math.cos(angle)
            self.y = gun.y + 78 + 74 * math.sin(angle)

        def draw(self):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

        def speed_change(self):
            'гравитация, трение'
            if self.y < 670:
                self.vy += 0.4
            if self.x <= 10 or self.x >= 990 or self.y >= 670:
                self.vx /= 1.2
            if self.y >= 670:
                self.vy /= 1.2
            if self.y >= 670 and abs(self.vy) <= 0.2:
                self.vy = 0

        def hittest(self, obj):
            'попадание в мишень'
            if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
                return True
            return False

    class Gun:
        def __init__(self):
            self.f2_power = 0
            self.f2_on = False
            self.x = 10
            self.y = 400

        def power(self):
            'сила выстрела'
            if self.f2_on and self.f2_power <= 25:
                self.f2_power += 0.3
            pygame.draw.rect(screen, GREEN, (gun.x + 10, gun.y - 30, self.f2_power * 4, 10))

        def draw1(self):
            screen.blit(image1, (self.x, self.y))

        def draw2(self, surface, angle):
            surface_rot = pygame.transform.rotate(surface, angle)
            rect = surface_rot.get_rect(center=(self.x + 50, self.y + 77))
            screen.blit(surface_rot, rect)

        def move(self):
            'движение пушки'
            if keys[pygame.K_w] and self.y >= -10:
                self.y -= 5
            elif keys[pygame.K_s] and self.y <= 530:
                self.y += 5


    class Target:
        def __init__(self):
            self.color = RED
            self.life = rnd(1, 4)
            self.vx = rnd(-3, 3)
            self.vy = rnd(-3, 3)
            self.r = rnd(10, 50)
            self.ampl = rnd(100, 300)
            self.s = 0
            number_of_1 = coord.count(1)
            ind_1 = rnd(1, number_of_1)
            n = 0
            ind = -1
            while n < ind_1:
                ind += 1
                if coord[ind] == 1:
                    n += 1
            ind += 1
            r = ind % 352
            if r != 0:
                y0 = ind // 352 + 1
                x0 = r
            else:
                y0 = ind // 352
                x0 = 352
            self.x = x0 + 599
            self.y = y0 + 49

        def del_coord(self):
            'убирает координаты, в которых не могут появляться мишени (чтобы не пересекались друг с другом)'
            for x in range(max(1, self.x - 599 - self.r - 49), min(353, self.x - 599 + self.r + 50)):
                for y in range(max(1, self.y - 49 - self.r - 49), min(582, self.y - 49 + self.r + 50)):
                    coord[(y - 1) * 352 + x - 1] = 0

        def move(self):
            if self.x < 600 or self.y < 50 or self.x > 950 or self.y > 630 or self.s >= self.ampl:
                self.vx = -self.vx
                self.vy = -self.vy
                self.s = 0
            self.x += self.vx
            self.y += self.vy
            self.s += (self.vx ** 2 + self.vy ** 2) ** 0.5

        def draw(self):
            pygame.draw.circle(screen, self.color, (self.x, self.y), self.r)

    f_score = pygame.font.SysFont('arial', 30)
    f_bullets = pygame.font.SysFont('cambria', 26)
    f_gameover = pygame.font.SysFont('cambriamath', 90)

    def scr():
        sc = f_score.render('Счёт: ' + str(score), False, RED)
        screen.blit(sc, (10, 10))

    def num_bullets():
        n_bull = f_bullets.render('Пули: ' + str(bullets), False, (200, 50, 50))
        screen.blit(n_bull, (10, 650))

    def game_over_txt():
        text1 = f_gameover.render('Игра окончена', False, (220, 0, 200))
        text2 = f_gameover.render('Ваш счёт: ' + str(score), False, (220, 0, 200))
        screen.blit(text1, (240, 220))
        screen.blit(text2, (250, 300))

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill(WHITE)
    floor = pygame.Surface((1000, 40))
    floor.fill(GREY)

    gun = Gun()
    image1 = pygame.image.load('pushka.png')
    image1 = pygame.transform.scale(image1, (150, 150))
    image1 = pygame.transform.rotate(image1, -90)
    image2 = pygame.image.load('stvol.png')
    image2 = pygame.transform.scale(image2, (110, 110))
    image2 = pygame.transform.rotate(image2, -90)
    surf = pygame.Surface((200, 200))
    surf.fill((255, 255, 255))
    surf.set_colorkey((255, 255, 255))

    clock = pygame.time.Clock()
    targets = []
    coord = [1] * 581 * 352
    for i in range(rnd(1, 4)):
        targets.append(Target())
        targets[-1].del_coord()
    bullets = 0
    balls = []
    timer = 0
    bullets_add = 0
    an = 0
    for t in targets:
        bullets_add += t.life
    bullets_add = int(bullets_add * 1.2) + 1
    bullets += bullets_add
    game_over = False
    mouse_pressed = False
    score = 0
    finished = False

    while not finished:
        screen.fill(WHITE)
        screen.blit(floor, (0, 680))
        mouse_pos = pygame.mouse.get_pos()
        an = math.atan2(mouse_pos[1] - (gun.y + 77), mouse_pos[0] - (gun.x + 50))

        clock.tick(FPS)
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True

            elif event.type == pygame.MOUSEBUTTONDOWN and not mouse_pressed and bullets > 0:
                mouse_pressed = True
                ball = Ball(an)
                gun.f2_on = True
            elif event.type == pygame.MOUSEBUTTONUP and bullets > 0 and 'ball' in locals():
                mouse_pressed = False
                ball.vx = gun.f2_power * math.cos(an)
                ball.vy = -gun.f2_power * math.sin(-an)
                balls.append(ball)
                bullets -= 1
                gun.f2_on = False
                gun.f2_power = 0

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    balls = []
                    targets = []
                    bullets = 0
                    score = 0
                    gun = Gun()
                    main()
                    screen.fill(WHITE)
                    finished = True

        if len(targets) == 0:
            if timer >= 50:
                bullets_add = 0
                balls.clear()
                coord = [1] * 581 * 352
                for i in range(rnd(1, 4)):
                    targets.append(Target())
                    targets[-1].del_coord()
                for t in targets:
                    bullets_add += t.life
                bullets_add = int(bullets_add * 1.2) + 1
                bullets += bullets_add
                timer = 0
            else:
                timer += 1
        else:
            if bullets == 0 and len(balls) == 0:
                game_over = True
        for t in targets:
            for b in balls:
                if b.hittest(t):
                    t.life -= 1
                    balls.remove(b)
            if t.life <= 0:
                targets.remove(t)
                score += 1

        gun.move()
        gun.power()

        for b in balls:
            b.speed_change()
            b.move()
            if abs(b.vx) <= 0.001 and abs(b.vy) <= 0.001:
                b.lifetime -= 1
            if b.lifetime <= 0:
                balls.remove(b)
        num_bullets()
        scr()
        for b in balls:
            b.draw()
        if mouse_pressed:
            ball.move_with_gun(an)
            ball.draw()
        surf.blit(image2, (91, 55))
        gun.draw2(surf, math.degrees(-an))
        gun.draw1()
        for t in targets:
            t.move()
            t.draw()
            f_life = pygame.font.SysFont('arial', int(1.5 * t.r))
            text_life = f_life.render(str(t.life), False, BLACK)
            rect = text_life.get_rect(centerx=t.x, centery=t.y)
            screen.blit(text_life, rect)
        if game_over:
            timer += 1
            if timer >= 50:
                game_over_txt()
        pygame.display.update()


main()

pygame.quit()
