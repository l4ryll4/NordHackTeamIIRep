import math
import pygame


class Ball(pygame.sprite.Sprite):

    #стартовая позиция
    x = 350.0
    y = 450.0
    
    #скорость
    speed = 10.0
    direction = 200.0
 
    #размеры мячика
    width = 20
    height = 20

    def __init__(self,Ka):
        # Call the parent class (Sprite) constructor
        super().__init__()

        if Ka ==0:
            self.image = pygame.image.load("res/orb.png")
        if Ka ==1:
            self.image = pygame.image.load("res/ball2.png")

        # Get a rectangle object that shows where our image is
        self.rect = self.image.get_rect()
 
        # Get attributes for the height/width of the screen
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
     

    def bounce(self, diff):
        self.direction = (180 - self.direction) % 360
        self.direction -= diff
 
    def update(self):
        """ Update the position of the ball. """
        # Sine and Cosine work in degrees, so we have to convert them
        direction_radians = math.radians(self.direction)
 
        # Change the position (x and y) according to the speed and direction
        self.x += self.speed * math.sin(direction_radians)
        self.y -= self.speed * math.cos(direction_radians)
 
        # Move the image to where our x and y are
        self.rect.x = self.x
        self.rect.y = self.y
 
        #отскок от верха
        if self.y <= 35:
            self.bounce(0)
            self.y = 36
 
        #левая сторона
        if self.x <= 30:
            self.direction = (360 - self.direction) % 360
            self.x = 31
 
        #правая сторона
        if self.x >= 645:
            self.direction = (360 - self.direction) % 360
            self.x = 644

        #провалился
        if self.y > 680:
            self.x = 350.0
            self.y = 450.0
            return True
        else:
            return False