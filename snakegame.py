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

        self.clock = pygame.time.Clock()
        
        self.lose = False
        
    def execute(self):
        pygame.display.set_caption("The Snake Game")
        pygame.display.update()

        while True:
            self.clock.tick(16)
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
            
            if self.snake.get_position()[0] > self.screen.get_width() or self.snake.get_position()[0] < 0 or self.snake.get_position()[1] > self.screen.get_height() or self.snake.get_position()[1] < 0:
                self.lose = True

            for i in range(1, len(self.snake.body)):
                if self.snake.is_collisioning(self.snake.body[i]):
                    self.lose = True

            # RESET SCREEN
            self.screen.fill((0, 0, 0))

            # ADD ELEMENTS
            self.fruit.draw()
            self.snake.update_move()
            self.snake.draw()

            self.text_pointer.set_counter(len(self.snake.body) - 3)
            self.text_pointer.draw()

            ded = DeadScreen()

            ded.add_text("¡Haz Perdido!", 40, (0, 0, 0))
            ded.add_text(f"Tu puntaje fue: {self.text_pointer.counter}", 25, (0, 0, 0))

            if self.lose:
                ded.draw_screen(self.screen)

            pygame.display.update()
        
class PointsDisplay(object):

    def __init__(self, screen):
        self.screen = screen
        self.counter = 0

        self.font = pygame.font.SysFont('Helvetica Neue', 30)
        self.text_surface = None

    def set_counter(self, amount):
        self.counter = amount

    def draw(self):
        self.text_surface = self.font.render(f'Points: {self.counter}', True, (255, 180, 255))
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
        f = Square(screen.get_width()//2, screen.get_height()//2, screen)
        f.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        self.body = [f]
        dirs = self.get_random_move_init()
        self.direction = (dirs[0], dirs[1])
        self.screen = screen

        self.append_body()
        self.append_body()

    def get_random_move_init(self):
        opts = [
            (1, 0),
            (-1, 0),
            (0, 1),
            (0, -1)
        ]

        return opts[random.randint(0, len(opts) - 1)]
        #return (1, 0)
    
    def change_direction(self, direction):
        self.direction = direction

    def draw(self):
        for part in self.body:
            part.draw()

    def update_move(self):
        newer = []
        for i in self.body:
            newer.append((i.x, i.y))

        for x in range(0, len(self.body)):
            if x == 0:
                self.body[x].move(self.direction[0] * 16, self.direction[1] * 16)
            else:
                self.body[x].move_to(newer[x-1][0], newer[x-1][1])

        #print(f"{self.get_position()[0], self.get_position()[1]}")
    
    def get_position(self):
        return (self.body[0].x, self.body[0].y)


    def is_collisioning(self, square) -> bool:
        return self.body[0].is_collisioning(square.x, square.y)

    def append_body(self):
        last_element = self.body[len(self.body) - 1]
        xpos, ypos = (
            last_element.get_x() + (16 * self.direction[0] * -1),
            last_element.get_y() + (16 * self.direction[1] * -1)
        )

        sq = Square(xpos, ypos, self.screen)
        #sq.color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        sq.color = (255, 255, 255)
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
        self.x += x
        self.y += y

    def move_to(self, x, y):
        self.x = x
        self.y = y

    def draw(self): 
        pygame.draw.rect(self.screen, self.color, (self.get_x(), self.get_y(), 16, 16))


    def is_collisioning(self, x, y):
        sup_e = (self.x - 15, self.y - 15)
        inf_e = (self.x + 15, self.y + 15)

        for xpos in range(sup_e[0], inf_e[0]):
            for ypos in range(sup_e[1], inf_e[1]):
                if xpos == x and ypos == y:
                    return True
        return False

class DeadScreen(object):

    def __init__(self):
        self.font = pygame.font.SysFont('Helvetica Neue', 30)
        self.texts = []

        self.fakeScreen = pygame.Surface((600, 600))
        self.fakeScreen.fill((255, 255, 255))

    def add_text(self, text, size, color):
        font = pygame.font.SysFont('Helvetica Neue', size)
        ts = font.render(text, True, color)
        self.texts.append(ts)

    def draw_texts(self):
        cx, cy = self.fakeScreen.get_width() / 2, self.fakeScreen.get_height() / 2

        for i, text in enumerate(self.texts):
            offset = 0
            if (i > 0):
                offset = self.texts[i-1].get_height()
            pos = (cx - (text.get_width() / 2), (cy - (text.get_height() / 2)) +offset-20)
            self.fakeScreen.blit(text, pos)


    def draw_screen(self, screen):
        self.draw_texts()
        screen.blit(self.fakeScreen, (0, 0))
        


pygame.init()
pygame.font.init()

game = Game()
game.execute()