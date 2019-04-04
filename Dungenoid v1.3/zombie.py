import pygame

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        
        self.image = pygame.image.load("res/zombie2min.png")
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
    def getType(self):
        return "zomb"