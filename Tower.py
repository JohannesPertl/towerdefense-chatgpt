# Tower class
import pygame

from constants import GREEN
from main import win


class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.range = 150
        self.damage = 1

    def draw(self):
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.height))

    def shoot(self, enemy):
        if self.is_within_range(enemy):
            enemy.health -= self.damage

    def is_within_range(self, enemy):
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range

