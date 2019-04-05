import pygame
import random

class Imp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        
        self.image = pygame.image.load("res/Imp.png")
        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y
        self.spx = random.randrange(-5, 5)
        self.spy= random.randrange(-5, 5)
        
    def update(self):
        
        self.rect.y += 0
        self.rect.x += self.spx

        #лево
        if self.rect.x <= 120:
            self.spx = -self.spx
            self.x = 120
        #право
        if self.rect.x >= 510:
            self.spx = -self.spx
            self.x = 510
        
class Fireball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.x = x
        self.y = y
        self.image = pygame.image.load("res/fireball.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        self.speedy = 5
        
    def update(self):
        self.rect.y += self.speedy
        
        