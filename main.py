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
COLOUR = (20, 20, 20)
SIZE = 10

# incline - наклон, который задумано получать с гироскопа,
# здесь относительный, в долях единицы
# если 0 то горизонтально поверхности земли
# если 1 то поверхность наклонена на 90 градусов etc...
incline = {
    'x': 0,
    'y': 0.1,
}

class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.t = 0
        self.softness = random.uniform(MIN_SOFTNESS, MAX_SOFTNESS)

    def move(self, incline):
        self.position = self.get_next_position(incline)
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
        return (dx, dy)

    def get_next_position(self, incline, scale=1):
        # масштабирование scale используется для экстраполяции значений
        # (например необходимо при отрисовке направлений во время паузы)
        x, y = self.position
        dx, dy = self.get_increment()

        # нормирование скоростей, в зависимости от угла наклона поверхности
        dy *= incline['y'] * scale
        dx *= incline['x'] * scale

        return (x + dx, y + dy)

    def collision(self, incline):
        # todo сделать тоже самое с ударением шариков друг об друга
        x, y = self.get_next_position(incline)
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

pause = True
GAME_END = False

# симуляция наклона поверхности с помощь. кнопок вверх, вниз, влево, вправо
commands_incline = {
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN',
    pygame.K_LEFT: 'LEFT',
    pygame.K_RIGHT: 'RIGHT'
}

def update_inclane(command, incline):
    if command == 'UP' and incline['y'] < 1:
        incline['y'] += 0.001
    elif command == 'DOWN' and incline['y'] > -1:
        incline['y'] -= 0.001
    if command == 'LEFT' and incline['x'] < 1:
        incline['x'] += 0.001
    elif command == 'RIGHT' and incline['x'] > -1:
        incline['x'] -= 0.001
    # print(incline)


balls = []
balls_combinations = []

def correct_collision(balls_combinations):
    for ball, other_ball in balls_combinations:
        # 1. если уже произошло слипание - разнести шарики в разные стороны
        # 2. если на следующем ходу будет наложение - сменить траекторию
        pass


while not GAME_END:
    game_screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_END = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            balls.append(Ball(pos, (0, 0)))
            balls_combinations = list(combinations(balls, 2))

    if not pause:
        pressed = pygame.key.get_pressed()
        for command in (commands_incline[key] for key in commands_incline if pressed[key]):
            update_inclane(command, incline)

        correct_collision(balls_combinations)
        for ball in balls:
            ball.collision(incline)
            ball.move(incline)
            ball.show(game_screen)
    else:
        for ball in balls:
            ball.show(game_screen)
            print(ball.get_next_position(incline))
            pygame.draw.aaline(game_screen, (0, 255, 255),
                               ball.position,
                               ball.get_next_position(incline, 50))



    pygame.display.update()



pygame.quit()
quit()
