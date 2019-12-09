#!/usr/bin/env python3

import os
import random
import pygame
from pygame.locals import * # Constants
import math
import sys

os.environ["SDL_VIDEO_CENTERED"] = "1"

screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("The Snake Game")

clock = pygame.time.Clock()

class Game(object):

    def __init__(self):
        self.player = SnakeObject()
        self.fruit = Fruit()

    def loop(self):

        if self.fruit.get_rect().colliderect(self.player.body[0]):
            print("Collision detected")
            self.player.append_body()
            self.fruit.reset()

        # RESET SCREEN
        screen.fill((255, 255, 255))

        # MOVE SNAKE
        self.player.move_snake()
        self.player.handle_keys()
        self.fruit.display_update()

        pygame.display.update()

class Fruit(object):

    def __init__(self):
        self.fruit_exists = False
        self.actual_fruit = self.create_fruit()

    def create_fruit(self):
        if self.fruit_exists is False:
            self.fruit_exists =  True
            return SnakeBodyPart(random.randrange(0, screen.get_width() - 1), random.randrange(0, screen.get_height() - 1))

    def display_update(self):
        self.actual_fruit.draw_again()

    def get_rect(self):
        return self.actual_fruit.get_rect()

    def reset(self):
        self.actual_fruit = self.create_fruit()

class SnakeObject(object):

    def __init__(self):
        self.body = [SnakeBodyPart(screen.get_width()//2, screen.get_height()//2)]
        self.move_direction = (random.randrange(-1, 1), random.randrange(-1, 1))

    def move_snake(self):
        for part in range(len(self.body)):
            before = 0
            current = self.body[part]
            xc, yc = current.get_position()
            current.move(self.move_direction[0] * 4, self.move_direction[1] * 4)
        pygame.display.update()
    
    def set_move_direction(self, ax, ay):
        self.move_direction = (ax, ay)

    def handle_keys(self):
        for e in pygame.event.get():
            if e.type == KEYDOWN:
                key = e.key
                if key == K_LEFT:
                    self.set_move_direction(-1, 0)
                if key == K_RIGHT:
                    self.set_move_direction(1, 0)
                if key == K_UP:
                    self.set_move_direction(0, -1)
                if key == K_DOWN:
                    self.set_move_direction(0, 1)

    def can_eat_fruit(self, var):
        self.body[0].is_colliding_with(var)

    def append_body(self):
        self.body.append(SnakeBodyPart(self.body[0].get_position()[0], self.body[0].get_position()[1]))

class SnakeBodyPart(object):

    def __init__(self, initx: int, inity: int):
        self.rect = pygame.draw.rect(screen, (0, 0, 128), (initx, inity, 16, 16))

    def move(self, x, y):
        self.draw_rect(x, y)
    
    def get_position(self):
        return (self.rect.x, self.rect.y)

    def draw_rect(self, x, y):
        self.rect = self.rect.move(x, y)
        self.rect = pygame.draw.rect(screen, (0, 0, 128), self.rect)

    def draw_again(self):
        if self.rect is not None:
            self.rect = pygame.draw.rect(screen, (0, 0, 128), self.rect)

    def is_colliding_with(self, obj):
        return self.rect.colliderect(obj)

    def get_rect(self):
        return self.rect


    '''
    def draw(self, surface):
        pygame.draw.rect(screen, (0, 0, 128), (screen.get_width()/2, screen.get_height()/2, 16, 16))
    '''

pygame.init()

screen.fill((0, 0, 0))
game = Game()
#clock = pygame.time.Clock()
pygame.display.update()

while True:

    for e in pygame.event.get():
        if e.type == QUIT:
            pygame.quit()
            exit()
            break

    game.loop()
