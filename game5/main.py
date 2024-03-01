import os
import pygame
import pymunk
import pymunk.pygame_util
import math
import sys
import random
import time
import datetime


pygame.init()
pygame.display.set_caption('GOLF')
size = width, height = 1920, 1080
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

START_TIME = 0

levels = ['level1.txt']  # список уровней
random_level = True  # если == True, то уровень будет выбран случайно
level_name = 'level1.txt'  # название текущего уровня

FPS = 100


def on_end(ball):
    ball.ball_remove()
    global START_TIME

    t = time.perf_counter() - START_TIME
    all_time = str(datetime.datetime.fromtimestamp(t).strftime('%M:%S'))
    from game import Finish
    Finish(all_time, "color", "level", "sound_eff")


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, color_key=None):
    fullname = os.path.join('Sprites', name)
    try:
        image = pygame.image.load(fullname).convert()
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image


tile_images = {
    'wall': load_image('Tiles/box.png'),
    'empty': load_image('Tiles/grass.png'),
    'hole': load_image('Tiles/hole.png'),
    'diag/': load_image('Tiles/diag1.png'),
    'diag2': load_image('Tiles/diag2.png')
}
ball_image = load_image('Ball/ball.png')
tile_width = tile_height = 50

player = None

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
ball_group = pygame.sprite.Group()
tiles_collide = pygame.sprite.Group()
hole_group = pygame.sprite.Group()


def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1]) ** 2 + (p2[0] - p1[0]) ** 2)


def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y, space):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(tile_width * pos_x, tile_height * pos_y)
        if tile_type != 'empty':
            self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body.position = (self.rect.x + tile_width / 2, self.rect.y + tile_height / 2)
            if tile_type == 'diag2':
                self.shape = pymunk.Poly(self.body, [(- tile_width / 2, - tile_height / 2),
                                                     (- tile_width / 2, tile_height / 2),
                                                     (tile_width / 2, tile_height / 2)])
            elif tile_type == 'diag/':
                self.shape = pymunk.Poly(self.body, [(tile_width / 2, - tile_height / 2),
                                                     (- tile_width / 2, tile_height / 2),
                                                     (tile_width / 2, tile_height / 2)])
            else:
                self.shape = pymunk.Poly.create_box(self.body, (tile_width, tile_height))
            self.shape.elasticity = 0.4
            self.shape.friction = 0.6
            space.add(self.body, self.shape)


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - width // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - height // 2)


def load_level(filename):
    filename = "data/" + filename
    try:
        with open(filename, 'r') as mapFile:
            level_map = [line.strip() for line in mapFile]
    except FileNotFoundError:
        print('Level file "', filename, '" not found', sep='')
        terminate()

    max_width = max(map(len, level_map))

    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level, space):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y, space)
                pass
            elif level[y][x] == '#':
                Tile('wall', x, y, space)
            elif level[y][x] == '/':
                Tile('diag/', x, y, space)
            elif level[y][x] == '2':
                Tile('diag2', x, y, space)
            elif level[y][x] == '@':
                Tile('empty', x, y, space)
                new_ball = Ball(space, (x * tile_width + tile_width / 2, y * tile_height + tile_height / 2), 20, 10,
                                (255, 0, 0, 100))
            elif level[y][x] == '*':
                hole = Hole(x, y, space)
    return new_ball, x, y, hole


def draw(space, window, draw_options, line):
    window.fill("white")
    space.debug_draw(draw_options)
    if line and line[0]:
        pygame.draw.line(window, "black", line[0], line[1], 3)
    pygame.display.update()


class Ball:
    def __init__(self, space, position, radius, mass, color):
        self.body = pymunk.Body()
        self.body.position = position
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.mass = mass
        self.shape.color = color
        self.shape.elasticity = 0.6
        self.shape.friction = 0.6
        self.radius = radius
        self.space = space
        space.add(self.body, self.shape)

        self.rect = (radius * 2 + 1, radius * 2 + 1)


        self.sprite = pygame.sprite.Sprite(ball_group)
        self.sprite.image = pygame.transform.scale(load_image('Ball/ball.png'), self.rect)
        self.sprite.rect = self.sprite.image.get_rect()


    def ball_sprite_reposition_rotation(self, rect, position, angular_velocity):
        self.sprite.rect = pygame.Rect(position[0] - rect[0] / 2, position[1] - rect[1] / 2, rect[0], rect[1])
        # sprite.image = pygame.transform.rotate(sprite.image, angular_velocity)
        # sprite.rect = sprite.image.get_rect(center=sprite.rect.center)

    def ball_remove(self):
        self.sprite.kill()
        self.space.remove(self.body)
        del self


class Hole(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, space):
        super().__init__(tiles_group, all_sprites)
        self.add(hole_group)
        self.image = tile_images["hole"]
        self.rect = self.image.get_rect().move(tile_width * pos_x - 5, tile_height * pos_y - 5)
        self.body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.body.position = (pos_x * tile_width + tile_width / 2, pos_y * tile_height + tile_height / 2)
        self.shape = pymunk.Poly.create_box(self.body, (tile_width, tile_height))
        self.shape.color = (0, 255, 0, 100)
        space.add(self.body, self.shape)


def run():
    global START_TIME

    START_TIME = time.perf_counter()

    if random_level:  # выбирает случайный уровень, если это выбрано сверху в скрипте
        level_name = random.choice(levels)

    space = pymunk.Space()

    ball, level_x, level_y, hole = generate_level(load_level(level_name), space)


    camera = Camera()

    running = True

    space.gravity = (0, 981)
    draw_options = pymunk.pygame_util.DrawOptions(screen)
    dt = 1 / FPS

    pressed = None

    ball_group.draw(screen)

    while running:
        line = None
        if pressed:
            line = [ball.body.position, pygame.mouse.get_pos()]

        ball.ball_sprite_reposition_rotation(ball.rect, tuple(ball.body.position), -ball.body.angular_velocity)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pressed_pos = pygame.mouse.get_pos()
                if calculate_distance(pressed_pos, ball.body.position) <= ball.radius:
                    vel = ball.body.velocity
                    if vel.x < 7 and vel.y < 0.5:
                        pressed = True
            if event.type == pygame.MOUSEBUTTONUP:
                if pressed:
                    angle = calculate_angle(*line) - math.pi
                    force = calculate_distance(*line) * 5000
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_force_at_world_point((fx, fy), ball.body.position)
                    pressed = None
            if pygame.sprite.spritecollideany(ball.sprite, hole_group):
                running = False
                on_end(ball)

        screen.fill("white")
        all_sprites.draw(screen)
        ball_group.draw(screen)
        if line and line[0]:
            pygame.draw.line(screen, "black", line[0], line[1], 3)
        pygame.display.flip()
        space.step(dt)
        clock.tick(FPS)
    pygame.quit()

