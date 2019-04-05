import pygame
import random

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("res/zombie2min.png")
        self.rect = self.image.get_rect()

        self.rect.x = x 
        self.rect.y = y
        self.spx = random.randrange(-2, 2)
        self.spy= random.randrange(-2, 2)



    def update(self):
        self.rect.y += self.spy
        self.rect.x += self.spx
        #Верх
        if self.rect.y <= 300:
            self.spy = -self.spy
            self.y = 31
        #Вниз
        if self.rect.y >= 631:
            self.spy = -self.spy
            self.y = 600
        #лево
        if self.rect.x <= 30:
            self.spx = -self.spx
            self.x = 31
        #право
        if self.rect.x >= 601:
            self.spx = -self.spx
            self.x = 600
     