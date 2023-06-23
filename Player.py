# Player class
import pygame as pygame

from constants import WHITE
from main import win


class Player:
    def __init__(self):
        self.lives = 5
        self.gold = 100

        # Load font
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        gold_text = self.font.render(f"Gold: {self.gold}", True, WHITE)
        win.blit(lives_text, (10, 10))
        win.blit(gold_text, (10, 40))