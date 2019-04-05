import pygame

cyan = (224, 255, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.width = 60
        self.height = 30
        self.image = pygame.image.load("res/pad.png")
 
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 350
        self.rect.y = 670
 
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > 600:
            self.rect.x = 600
        if self.rect.x < 30:
            self.rect.x = 30
                