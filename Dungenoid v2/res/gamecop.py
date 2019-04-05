import pygame
import sys
import os
import tkinter
from pygame.locals import *

from block import Block
from ball import Ball
from zombie import Zombie
from chest import Chest
from LV import laval
from player import Player
from coin import Coin

pygame.init()

KK = 0
life = 3
score = 0
white = (255, 255, 255)
block_width = 30
block_height = 30
XX = 0

#зарезервировано под всякие картинки, шрифты, звуки и прочую графическую фигню.
bg = pygame.image.load("res/bg1.jpg")
font = pygame.font.Font("res/font.ttf", 36)
#pygame.mixer.music.load ("res/Dungeon of Agony.mp3") 
#pygame.mixer.music.play (- 1 )

#создаем окно
screen = pygame.display.set_mode([900, 700])
window = pygame.display.set_mode([900, 700])
pygame.display.set_caption('Dungenoid')
pygame.mouse.set_visible(0)
info = pygame.Surface((800, 30))
background = pygame.Surface(screen.get_size())
 
#множества для спрайтов
blocks = pygame.sprite.Group()
chests = pygame.sprite.Group()
balls = pygame.sprite.Group()
allsprites = pygame.sprite.Group()
monsters = pygame.sprite.Group()
bonuses = pygame.sprite.Group()
 
#зомби-зомби-зомби-зомби
student = Zombie()
allsprites.add(student)
monsters.add(student)

bon = Coin (350, 60, 10)

#ракетка
player = Player()
allsprites.add(player)
 
#мячик
ball = Ball(0)
allsprites.add(ball)
balls.add(ball)

#блоки
top = 30
class Menu:
    def __init__(self, punkts = [400, 350, u'Punkt', (250,250,30), (250,30,250)]):
        self.punkts = punkts
    def render(self, poverhnost, font, num_punkt):
        for i in self.punkts:
            if num_punkt == i[5]:
                poverhnost.blit(font.render(i[2], 1, i[4]), (i[0], i[1]-30))
            else:
                poverhnost.blit(font.render(i[2], 1, i[3]), (i[0], i[1]-30))
    def menu(self):
        done = True
        font_menu = pygame.font.Font(None, 50)
        pygame.key.set_repeat(0,0)
        pygame.mouse.set_visible(True)
        punkt = 0
        while done:
            info.fill((0, 100, 200))
            screen.fill((0, 100, 200))
 
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt =i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                       sys.exit()
                    if e.key == pygame.K_UP:
                        if punkt > 0:
                           punkt -= 1
                    if e.key == pygame.K_DOWN:
                        if punkt < len(self.punkts)-1:
                           punkt += 1
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()
            window.blit(info, (0, 0))
            window.blit(screen, (0, 30))
            pygame.display.flip()
punkts = [(350, 300, u'Play', (11, 0, 77), (250,250,30), 0),
          (350, 340, u'Exit', (11, 0, 77), (250,250,30), 1)]
game = Menu(punkts)
game.menu()
#Распознаватор объектов 3000!
##А чего не 4000? :')
for row in laval:
    for column in row:
        if column == "-":
            block=Block(XX,top)
            blocks.add(block)
            allsprites.add(block)
        if column == "+":
            chest=Chest(XX, top)
            chests.add(chest)
            allsprites.add(chest)
        XX+=block_width 
    top += block_height 
    XX=0
    
clock = pygame.time.Clock()

game_over = False
sar = False
exit_program = False

#отрисовка экрана. Заменить/пофиксить
#мигание уже не надо(точки не нужны)
def drawScreen():
    pygame.display.update()
    screen.blit(bg, (0, 0))
    
while not exit_program:
    clock.tick(30)
    for e in pygame.event.get():         
        if e.type == pygame.QUIT:
            done = False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE:
                game.menu()        
 

    drawScreen()
    #ЕТО очки
    text = font.render("Score: "+str(score),True,(200,150,250))
    screen.blit(text, [700,100])
    text1 = font.render("Life: "+str(life),True,(200,150,250))
    screen.blit(text1, [700,200])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
            
    if not game_over:
        student.update()
        player.update()
        bon.update()
        sar = ball.update()
        if sar ==True:
            life -=1
            sar =False
        if life ==0:
            game_over = True
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
    destroychest = pygame.sprite.spritecollide(ball, chests, True)
    takecoin = pygame.sprite.spritecollide(player, bonuses, True)
 
    if len(deadblocks) > 0:
        ball.bounce(0)
        score +=10
    if len(deadmonsters)> 0:
        score +=500
        if len(monsters) == 0:
            game_over = True
    if len(takecoin) > 0:
        KK+=1
        Ball.width = 30
        Ball.height = 30
        Ball.speed = 7.5
        ball.__init__(KK)
    if len(destroychest) > 0:
        ball.bounce(0)
        x, y = ball.x, ball.y - 30
        bon = Coin (x, y, 15)
        allsprites.add(bon)
        bonuses.add(bon)
        score +=20
 
    allsprites.draw(screen)
 
    pygame.display.flip()
 
pygame.quit()