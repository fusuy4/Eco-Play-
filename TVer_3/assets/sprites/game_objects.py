import pygame
import random

class FallingObjects:
    def __init__(self, image_path, speed, position, num):
        self.recycleable = bool(num)
        self.image = pygame.image.load(image_path)
        self.rect = self.image.get_rect()
        self.top = self.rect.top
        self.speed = speed
        self.position = position

    def randomSpeed(self):
        self.speed = random.uniform(1, 3)

    def randomPosition(self):
        self.position = random.uniform(20, 460)
