# скорость это расстояние за единицу времени,
# для упрощения скорость это просто изменение расстояния за итерацию,
# или просто dx, или dy
import random
from itertools import combinations
import pygame
clock = pygame.time.Clock()
pygame.init()

WIDTH = 1000
HEIGHT = 1000
MIN_SOFTNESS = 0.2
MAX_SOFTNESS = 0.8

GRAVITY = 0.9
COLOUR = (100, 100, 120)
SIZE = 10

# incline - наклон, который задумано получать с гироскопа,
# здесь относительный, в долях единицы
# если 0 то горизонтально поверхности земли
# если 1 то поверхность наклонена на 90 градусов etc...
INCLINE = {
    'x': 0,
    'y': 0.1,
}
PAUSE = True
GAME_END = False

# симуляция наклона поверхности с помощь. кнопок вверх, вниз, влево, вправо
COMMANDS_INCLINE = {
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN',
    pygame.K_LEFT: 'LEFT',
    pygame.K_RIGHT: 'RIGHT'
}

class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.t = 0
        self.softness = random.uniform(MIN_SOFTNESS, MAX_SOFTNESS)

    def move(self):
        self.position = self.get_next_position()
        # за каждую итерацию происходит увеличение внутреннего времени тела на 0.001
        self.t += 0.001

    def show(self, screen):
        pygame.draw.circle(
            screen,
            COLOUR,
            self.position,
            SIZE
        )

    def get_increment(self):
        dx, dy = self.direction
        dx = dx + GRAVITY * self.t
        dy = dy + GRAVITY * self.t
        return dx, dy

    def get_next_position(self, scale=1):
        # масштабирование scale используется для экстраполяции значений
        # (например необходимо при отрисовке направлений во время паузы)
        x, y = self.position
        dx, dy = self.get_increment()

        # нормирование скоростей, в зависимости от угла наклона поверхности
        dy *= INCLINE['y'] * scale
        dx *= INCLINE['x'] * scale

        return x + dx, y + dy

    def collision(self):
        # todo сделать тоже самое с ударением шариков друг об друга
        x, y = self.get_next_position()
        if SIZE > x or x > WIDTH - SIZE:
            dx, dy = self.get_increment()
            self.direction = (-dx * self.softness, dy)
            self.t = 0
            return True
        if SIZE > y or y > HEIGHT - SIZE:
            dx, dy = self.get_increment()
            self.direction = (dx, -dy * self.softness)
            self.t = 0
            return True
        return False


game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pixel physics")


def update_incline(command):
    if command == 'UP' and INCLINE['y'] < 1:
        INCLINE['y'] += 0.001
    elif command == 'DOWN' and INCLINE['y'] > -1:
        INCLINE['y'] -= 0.001
    if command == 'LEFT' and INCLINE['x'] < 1:
        INCLINE['x'] += 0.001
    elif command == 'RIGHT' and INCLINE['x'] > -1:
        INCLINE['x'] -= 0.001
    # print(incline)


balls = []
balls_combinations = []


def correct_collision(balls_combinations):
    for ball, other_ball in balls_combinations:
        # 1. если уже произошло слипание - разнести шарики в разные стороны
        # 2. если на следующем ходу будет наложение - сменить траекторию
        pass


while not GAME_END:
    game_screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_END = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            PAUSE = not PAUSE

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            balls.append(Ball(pos, (0, 0)))
            balls_combinations = list(combinations(balls, 2))

    if not PAUSE:
        pressed = pygame.key.get_pressed()

        for command in (COMMANDS_INCLINE[key] for key in COMMANDS_INCLINE if pressed[key]):
            update_incline(command)

        correct_collision(balls_combinations)
        for ball in balls:
            ball.collision()
            ball.move()
            ball.show(game_screen)
    else:
        for ball in balls:
            ball.show(game_screen)
            pygame.draw.aaline(game_screen, (0, 255, 255),
                               ball.position,
                               ball.get_next_position(scale=50))
    pygame.display.update()


pygame.quit()
quit()
