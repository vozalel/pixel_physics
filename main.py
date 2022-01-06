import pygame
import random
from math import sqrt
clock = pygame.time.Clock()
pygame.init()

WIDTH = 600
HEIGHT = 600
SOFTNESS = 0.04

GRAVITY = 0.0001
# INCLINE - наклон получаемый с гироскопа, здесь относительный в долях единицы
# от -1: наклон правой/нижней стороной вверх до +1 наклон левой/верхней стороной вверх
# если 0 то горизонтально поверхности земли
INCLINE_X = 0
INCLINE_Y = 0.1
COLOUR = (180, 180, 180)
SIZE = 10

# инициализация одной клетки в случайном месте поля

class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.t = 0

    def move(self):
        self.position = self.get_next_position()
        self.t += 1

    def show(self, screen):
        pygame.draw.circle(
            screen,
            COLOUR,
            self.position,
            SIZE
        )

    def get_increment(self):
        dx, dy = self.direction
        dx += (GRAVITY * INCLINE_X) * self.t ** 2 / 2
        dy += (GRAVITY * INCLINE_Y) * self.t ** 2 / 2
        return (dx, dy)

    def get_next_position(self):
        x, y = self.position
        dx, dy = self.get_increment()
        return (int(x + dx), int(y + dy))

    def collision(self):
        x, y = self.get_next_position()
        if SIZE > x or x > WIDTH - SIZE:
            dx, dy = self.get_increment()
            self.direction = (-dx, dy)
            self.t = 0
        if SIZE > y or y > HEIGHT - SIZE:
            dx, dy = self.get_increment()
            self.direction = (dx, -dy)
            self.t = 0






x = WIDTH / 2 # random.randint(SIZE, WIDTH - SIZE)
y = HEIGHT / 2 # random.randint(SIZE, HEIGHT - SIZE)
dx2 = 0 # random.random()
dy2 = 1 - dx2

ball = Ball(
    (x, y),
    (sqrt(dx2), sqrt(dy2))
)


game_screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("pixel physics")

pause = True
GAME_END = False

commands_move = {
    pygame.K_UP: 'UP',
    pygame.K_DOWN: 'DOWN',
    pygame.K_LEFT: 'LEFT',
    pygame.K_RIGHT: 'RIGHT'
}

def update_inclane(command):
    if command == 'UP': pass
    elif command == 'DOWN': pass
    elif command == 'LEFT': pass
    elif command == 'RIGHT': pass

while not GAME_END:
    game_screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_END = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause
                print(pause)

    pressed = pygame.key.get_pressed()

    if not pause:
        for command in (commands_move[key] for key in commands_move if pressed[key]):
            update_inclane(command)
            print(command)
        ball.collision()
        ball.move()
        ball.show(game_screen)

    pygame.display.update()



pygame.quit()
quit()