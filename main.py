import pygame
import random
from math import sqrt
clock = pygame.time.Clock()
pygame.init()

WIDTH = 600
HEIGHT = 600

GRAVITY = 10
# INCLINE - наклон получаемый с гироскопа, здесь относительный в долях единицы
# от -1: наклон правой/нижней стороной вверх до +1 наклон левой/верхней стороной вверх
# если 0 то горизонтально поверхности земли
INCLINE_X = 0
INCLINE_Y = 0
COLOUR = (180, 180, 180)
SIZE = 10
primitive_field = []

# инициализация одной клетки в случайном месте поля


class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction

    def move(self):
        x, y = self.position
        dx, dy = self.direction
        self.position = (x + dx, y + dy)

    def show(self, screen):
        pygame.draw.circle(
            screen,
            COLOUR,
            self.position,
            SIZE
        )


x = random.randint(SIZE, WIDTH - SIZE)
y = random.randint(SIZE, HEIGHT - SIZE)
dx2 = random.random()
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

field = []


dX, dY  = 0, 0
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
            print(command)

        ball.move()
        ball.show(game_screen)

    pygame.time.delay(15)



    pygame.display.update()



pygame.quit()
quit()