import pygame
import sys
import os
from pygame.locals import *

from block import Block
from ball import Ball
from zombie import Zombie
from chest import Chest
from LV import laval

pygame.init()

life = 3
score = 0
white = (255, 255, 255)
block_width = 30
block_height = 30
XX = 0
zombie_width = 60
zombie_height = 60


#зарезервированно под вские картинки, шрифты, звуки и прочую графическую фигню.
bg = pygame.image.load("res/bg1.jpg")
font = pygame.font.Font("res/font.ttf", 36)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
 
        self.width = 75
        self.height = 60
        self.image = pygame.image.load("res/pad.png")
 
        self.rect = self.image.get_rect()
        self.screenheight = pygame.display.get_surface().get_height()
        self.screenwidth = pygame.display.get_surface().get_width()
 
        self.rect.x = 0
        self.rect.y = self.screenheight-self.height
 
    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        if self.rect.x > 600:
            self.rect.x = 600
        if self.rect.x < 30:
            self.rect.x = 30
                
#создаем окно
screen = pygame.display.set_mode([900, 700])
pygame.display.set_caption('Dungenoid')
pygame.mouse.set_visible(0)
 
background = pygame.Surface(screen.get_size())
 
#множества для спрайтов
blocks = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
monsters = pygame.sprite.Group()
 
#ракетка
player = Player()
allsprites.add(player)
 
#мячик
ball = Ball()
allsprites.add(ball)
balls.add(ball)

#блоки
top = 30

#Распознаватор объектов 3000!
##А чего не 4000? :')
for row in laval:
    for column in row:
        if column == "-":
            block=Block(XX,top)
            blocks.add(block)
            allsprites.add(block)
        if column == "=":
            zomb = Zombie(XX, top)
            monsters.add(zomb)
            allsprites.add(zomb)
        if column == "+":
            chest = Chest(XX, top)
            blocks.add(chest)
            allsprites.add(chest)
        XX+=block_width 
    top += block_height 
    XX=0
    


clock = pygame.time.Clock()

game_over = False

exit_program = False

#отрисовка экрана. Заменить/пофиксить
#мигание уже не надо(точки не нужны)
def drawScreen():
    global animCount
    pygame.display.update()
    screen.blit(bg, (0, 0))
    
while not exit_program:
    clock.tick(30)

    drawScreen()
    #ЕТО очки
    text = font.render("Score: "+str(score),True,(200,150,250))
    screen.blit(text, [700,100])
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
            
    if not game_over:
        player.update()
        game_over = ball.update()
    if game_over:
        text = font.render("Game Over", True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
    if pygame.sprite.spritecollide(player, balls, False):
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    deadmonsters = pygame.sprite.spritecollide(ball, monsters, True)
 
    if len(deadblocks) > 0:
        ball.bounce(0)
        score +=10
    if len(deadmonsters)> 0:
        score +=500
        if len(monsters) == 0:
            game_over = True
 
    allsprites.draw(screen)
 
    pygame.display.flip()
 
pygame.quit()