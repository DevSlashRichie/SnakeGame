#!/usr/bin/env python3

import pygame
import random
import sys
from pygame.locals import *

class Game(object):
    
    def __init__(self):
        self.screen = pygame.display.set_mode((600, 600))

        self.fruit = Fruit(self.screen)
        self.snake = Snake(self.screen)

        self.points = 0
        self.text_pointer = PointsDisplay(self.screen)
        
    def execute(self):
        pygame.display.set_caption("The Snake Game")
        pygame.display.update()

        while True:
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                    break
                
                if e.type == KEYDOWN:
                    key = e.key
                    if key == K_LEFT:
                        self.snake.change_direction((-1, 0))
                    if key == K_RIGHT:
                        self.snake.change_direction((1, 0))
                    if key == K_UP:
                        self.snake.change_direction((0, -1))
                    if key == K_DOWN:
                        self.snake.change_direction((0, 1))

            if self.snake.is_collisioning(self.fruit.get_square()):
                self.fruit.reset()
                self.snake.append_body()

            # RESET SCREEN
            self.screen.fill((0, 0, 0))

            # ADD ELEMENTS
            self.fruit.draw()
            self.snake.update_move()
            self.snake.draw()

            self.text_pointer.set_counter(len(self.snake.body) - 1)
            self.text_pointer.draw()

            pygame.display.update()
        
class PointsDisplay(object):

    def __init__(self, screen):
        self.screen = screen
        self.counter = 0
        pygame.font.init()

        self.font = pygame.font.SysFont('Comic Sans MS', 30)
        self.text_surface = None

    def set_counter(self, amount):
        self.counter = amount

    def draw(self):
        self.text_surface = self.font.render(f'Points: {self.counter}', True, (255, 255, 255))
        self.screen.blit(self.text_surface, (30, 30))
        

class Fruit(object):
    
    def __init__(self, screen):
        self.screen = screen
        self.element = self.gen_element()
    
    def gen_element(self):
        return Square(random.randrange(0, self.screen.get_width() - 1), random.randrange(0, self.screen.get_height() - 1), self.screen)

    def draw(self):
        return self.element.draw()

    def get_square(self):
        return self.element

    def reset(self):
        self.element = self.gen_element()

class Snake(object):
    
    def __init__(self, screen):
        self.body = [Square(screen.get_width() // 2, screen.get_height() // 2, screen)]
        dirs = self.get_random_move_init()
        self.direction = (dirs[0], dirs[1])
        self.screen = screen

    def get_random_move_init(self):
        opts = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        return opts[random.randint(0, len(opts) - 1)]
    
    def change_direction(self, direction):
        self.direction = direction

    def draw(self):
        for part in self.body:
            part.draw()

    def update_move(self):
        save_list = self.body[:]
        for part in range(0, len(self.body)):
            sq_cr = self.body[part]
            sq_cr.move(self.direction[0] * 16, self.direction[1] * 16)
        
    
    def is_collisioning(self, square) -> bool:
        return self.body[0].is_collisioning(square.x, square.y)

    def append_body(self):
        last_element = self.body[len(self.body) - 1]
        xpos, ypos = (
            last_element.get_x() + (16 * self.direction[0] * -1),
            last_element.get_y() + (16 * self.direction[1] * -1)
        )

        sq = Square(xpos, ypos, self.screen)
        sq.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.body.append(sq)

class Square(object):
    
    def __init__(self, x, y, screen):
        self.x = x
        self.y = y
        self.screen = screen
        self.color = (255, 255, 255)

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

    def move(self, x, y):
        self.x = self.x + x
        self.y = self.y + y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self): 
        pygame.draw.rect(self.screen, self.color, (self.get_x(), self.get_y(), 16, 16))


    def is_collisioning(self, x, y):
        sup_e = (self.x - 16, self.y - 16)
        inf_e = (self.x + 16, self.y + 16)

        for xpos in range(sup_e[0], inf_e[0]):
            for ypos in range(sup_e[1], inf_e[1]):
                if xpos == x and ypos == y:
                    return True
        return False


pygame.init()
game = Game()
game.execute()