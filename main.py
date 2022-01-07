# скорость это расстояние за единицу времени,
# для упрощения скорость это просто изменение расстояния за итерацию,
# или просто dx, или dy
import pygame
clock = pygame.time.Clock()
pygame.init()

WIDTH = 1000
HEIGHT = 1000
SOFTNESS = 0.5

GRAVITY = 0.9
COLOUR = (255, 18, 255)
SIZE = 10

# incline - наклон, который задумано получать с гироскопа,
# здесь относительный, в долях единицы
# если 0 то горизонтально поверхности земли
# если 1 то поверхность наклонена на 90 градусов etc...
incline = {
    'x': 0,
    'y': 1,
}

class Ball:
    def __init__(self, position, direction):
        self.position = position
        self.direction = direction
        self.t = 0

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

    def get_next_position(self, incline):
        x, y = self.position
        dx, dy = self.get_increment()

        # нормирование скоростей, в зависимости от угла наклона поверхности
        dy *= incline['y']
        dx *= incline['x']
        return (x + dx, y + dy)

    def collision(self, incline):
        # todo сделать тоже самое с ударением шариков друг об друга
        x, y = self.get_next_position(incline)
        if SIZE > x or x > WIDTH - SIZE:
            dx, dy = self.get_increment()
            self.direction = (-dx * SOFTNESS, dy)
            self.t = 0
            return True
        if SIZE > y or y > HEIGHT - SIZE:
            dx, dy = self.get_increment()
            self.direction = (dx, -dy * SOFTNESS)
            self.t = 0
            return True
        return False

start_position = (WIDTH/2, HEIGHT/2)
start_direction = (0, 0)
ball = Ball(start_position, start_direction)


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

def update_inclane(command, inclane):
    if command == 'UP' and inclane['y'] < 1:
        inclane['y'] += 0.001
    elif command == 'DOWN' and inclane['y'] > -1:
        inclane['y'] -= 0.001
    if command == 'LEFT' and inclane['x'] < 1:
        inclane['x'] += 0.001
    elif command == 'RIGHT' and inclane['x'] > -1:
        inclane['x'] -= 0.001
    print(inclane)


while not GAME_END:
    game_screen.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            GAME_END = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pause = not pause

    if not pause:
        pressed = pygame.key.get_pressed()
        for command in (commands_incline[key] for key in commands_incline if pressed[key]):
            update_inclane(command, incline)

        ball.collision(incline)
        ball.move(incline)

    ball.show(game_screen)
    pygame.display.update()



pygame.quit()
quit()
