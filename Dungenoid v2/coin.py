import pygame

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y, speed):
        super().__init__()
        
        self.speed = speed
        
        self.x = x
        self.y = y
        
        self.image = pygame.image.load("res/coin.png")
        self.rect = self.image.get_rect()
        
        self.rect.x = x
        self.rect.y = y
        
    def update(self):
        self.rect.y += self.speed
            