# Enemy class
import pygame

from constants import HEIGHT, RED, WIDTH
from main import win


class Enemy:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT // 2
        self.width = 20
        self.height = 20
        self.vel = 2

    def move(self):
        self.x += self.vel

    def draw(self):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))

    def reached_end(self):
        return self.x >= WIDTH

