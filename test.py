import pygame
from random import randint
from math import cos, sin, acos, asin, pi

# parameters
width = 800
height = 600
pause = True
game_end = False
YELLOW = (225, 225, 0)
aim_radius = 80
height_log = 50

colors = {
    "user": (0, 255, 0),
    "enemy": (255, 0, 255),
}

# init_block
clock = pygame.time.Clock()
pygame.init()
gameScreen = pygame.display.set_mode((width, height + height_log))
pygame.display.set_caption("point_derection")
f1 = pygame.font.Font(None, 36)


class Bullet():
    all = []
    hp_max = 255

    def __init__(self, direction, position, delay, caliber, color):
        self.step = 0
        self.delay = delay
        self.speed = speed
        self.direction = direction
        self.position = position
        self.caliber = caliber
        self.color = color
        self.hp = 255
        Bullet.all.append(self)

    def get_position_and_size_hp_bar(self):
        x, y = self.position
        x_hp = x - self.caliber
        y_hp = y - self.caliber - 3
        size_x = int(2 * self.caliber * self.hp / 255)
        size_y = 2
        return (x_hp, y_hp, size_x, size_y, self.color)

    def edit_position(self, max_position):
        x, y = self.position
        x_max, y_max = max_position
        cos_, sin_ = self.direction
        new_cos = cos_ if 0 + self.caliber < x < x_max - self.caliber else -cos_
        new_sin = sin_ if 0 + self.caliber < y < y_max - self.caliber else -sin_
        self.direction = (new_cos, new_sin)

    def get_new_direction(self, other_direction, reflection_plane):
        cos_1, sin_1 = self.direction
        cos_2, sin_2 = other_direction
        cos_p, sin_p = reflection_plane
        f_cos = lambda cos_p, cos_1, sin_p, sin_1: cos_p ** 2 * cos_1 - sin_p ** 2 * cos_1 + 2 * cos_p * sin_p * sin_1
        f_sin = lambda cos_p, cos_1, sin_p, sin_1: 2 * cos_p * sin_p * cos_1 - cos_p ** 2 * sin_1 + sin_p ** 2 * sin_1
        cos_1_c = f_cos(cos_p, -cos_1, sin_p, -sin_1)
        sin_1_c = f_sin(cos_p, -cos_1, sin_p, -sin_1)
        cos_2_c = f_cos(-cos_p, cos_2, -sin_p, sin_2)
        sin_2_c = f_sin(-cos_p, cos_2, -sin_p, sin_2)
        return (cos_1_c, sin_1_c), (cos_2_c, sin_2_c)

    def collision(self, other):
        x1, y1 = self.position
        x2, y2 = other.position
        r1 = self.caliber
        r2 = other.caliber

        if ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** (1 / 2) < r1 + r2:
            if r1 > r2:
                self.caliber += 1
                other.hp = other.hp - 20 if other.hp > 20 else 0
            elif r2 > r1:
                other.caliber += 1
                self.hp = self.hp - 20 if self.hp > 20 else 0
            else:
                self.caliber += 1
                other.caliber += 1
            sred, sgreen, sblue = self.color
            ored, ogreen, oblue = other.color
            sred = 255 - self.hp
            sgreen = self.hp
            ored = 255 - other.hp
            ogreen = other.hp
            self.color = (sred, sgreen, sblue)
            other.color = (ored, ogreen, oblue)

            cosp = (x2 - x1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2) if ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (
                        1 / 2) != 0 else 1
            sinp = (y2 - y1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2) if ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (
                        1 / 2) != 0 else 1
            reflection_plane = (cosp, sinp)
            self.direction = (-cosp, -sinp)
            other.direction = (cosp, sinp)
            # self.direction, other.direction = self.get_new_direction(other.direction, reflection_plane)

    def delete_bullet(self):
        for i in range(len(Bullet.all) - 1):
            if self == Bullet.all[i]: del Bullet.all[i]

    def get_new_enemy_pos(self, field_size):

        self.step = self.step + 1

        if self.step != 0:
            self.step = self.step % self.delay

            self.step = int(self.step)

        if self.step == 0:
            self.edit_position(field_size)
            cos_beta, sin_beta = self.direction
            x, y = self.position
            x += speed * cos_beta
            y += speed * sin_beta
            self.position = (x, y)


def get_angle(cos_, sin_):
    asn = asin(sin_)
    acs = acos(cos_)
    if cos_ < 0: asn = pi - asn
    if sin_ < 0: acs = 2 * pi - acs
    if cos_ > 0 and sin_ < 0:
        asn = 2 * pi + asn
    return (acs + asn) / 2


def get_mouse_angle(unit_pos, mouse_pos):
    (x1, y1) = unit_pos
    (x2, y2) = mouse_pos
    # alpha - viewing angle
    sin_ = (y2 - y1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2)
    cos_ = (x2 - x1) / ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** (1 / 2)
    print(get_angle(cos_, sin_))

    return (cos_, sin_)


def get_point_intersection_circle_and_line(unit_pos, mouse_pos, radius):
    x0, y0 = unit_pos
    cos_alpha, sin_alpha = get_mouse_angle(unit_pos, mouse_pos)
    x = x0 + radius * cos_alpha
    y = y0 + radius * sin_alpha
    return (int(x), int(y))


def draw_line(unit_pos, mouse_pos, radius):
    aim_end = get_point_intersection_circle_and_line(unit_pos, mouse_pos, radius)
    pygame.draw.aaline(gameScreen, YELLOW, list(unit_pos), list(aim_end))


def move_enemy(enemy_pos, caliber, color):
    pygame.draw.circle(gameScreen, color, (int(enemy_pos[0]), int(enemy_pos[1])), caliber)


mouse_pos = (0, 0)
unit_pos = (400, 300)
speed = 2
enemy_pos = (400, 300)
cos_beta, sin_beta = get_mouse_angle(unit_pos, mouse_pos)
caliber = 5

while not game_end:
    gameScreen.fill((0, 0, 0))
    for event in pygame.event.get():
        mouse_pos = pygame.mouse.get_pos() if pygame.mouse.get_pos() else mouse_pos
        if event.type == pygame.QUIT:
            game_end = True
        elif event.type == pygame.MOUSEMOTION and not pause:
            draw_line(unit_pos, mouse_pos, aim_radius)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_b:
                bullet = Bullet(get_mouse_angle(unit_pos, mouse_pos), unit_pos, 1, 10, (0, 255, 0))
            if event.key == pygame.K_SPACE:
                pause = not pause
                draw_line(unit_pos, mouse_pos, aim_radius)

    if not pause:
        draw_line(unit_pos, mouse_pos, aim_radius)
        count_bullet = f1.render(str(len(Bullet.all)), 1, (180, 0, 0))
        gameScreen.blit(count_bullet, (10, 50))
        for bullet in Bullet.all:
            if bullet.hp == 0:
                bullet.delete_bullet()

        for i in range(0, len(Bullet.all)):
            bullet = Bullet.all[i]
            bullet.get_new_enemy_pos((width, height))
            move_enemy(bullet.position, bullet.caliber, bullet.color)
            x_hp, y_hp, size_x, size_y, color = bullet.get_position_and_size_hp_bar()
            pygame.draw.rect(gameScreen, bullet.color, (x_hp, y_hp, size_x, size_y))
            # print(bullet.position)
            for j in range(i + 1, len(Bullet.all)):
                other_bullet = Bullet.all[j]
                bullet.collision(other_bullet)

        clock.tick(100)
    pygame.display.update()
pygame.quit()
quit()