import pygame
import sys
import os
import tkinter
import time
from pygame.locals import *

from block import *
from ball import Ball
from chest import Chest
from LV import laval
from player import Player
from coin import Coin
from Imp import *
from zombie import Zombie

pygame.init()

VV=1
SS = 0
KK = 0
life = 3
score = 0
white = (255, 255, 255)
block_width = 30
block_height = 30
XX = 0

#зарезервировано под всякие картинки, шрифты, звуки и прочую графическую фигню.
bg = pygame.image.load("res/bg11.jpg")
font = pygame.font.Font("res/font.ttf", 26)

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
monsters1 = pygame.sprite.Group()
atacks = pygame.sprite.Group()
bonuses = pygame.sprite.Group()

 
#зомби-зомби-зомби-зомби
student = Zombie(100, 315,)
allsprites.add(student)
monsters1.add(student)

student2 = Zombie(400, 315)
allsprites.add(student2)
monsters1.add(student2)

bon = Coin (350, 60, 10)
shard = Fireball(350, 60)
clown = Imp(350, 70)
allsprites.add(clown)
monsters.add(clown)
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
            screen.blit(bg, (0, 0))
            mp = pygame.mouse.get_pos()
            for i in self.punkts:
                if mp[0]>i[0] and mp[0]<i[0]+155 and mp[1]>i[1] and mp[1]<i[1]+50:
                    punkt =i[5]
            self.render(screen, font_menu, punkt)
            for e in pygame.event.get():
                if e.type == pygame.QUIT:
                    sys.exit()
                if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                    pygame.mixer.music.load("res/Dungeon of Agony.mp3")
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_volume(0.5)
                    if punkt == 0:
                        done = False
                    elif punkt == 1:
                        exit()

            pygame.display.flip()
punkts = [(350, 300, u'PLAY', (11, 0, 77), (250,250,30), 0),
          (350, 340, u'EXIT', (11, 0, 77), (250,250,30), 1)]
game = Menu(punkts)
game.menu()
#Распознаватор объектов 3000!
##А чего не 4000? :')
for row in laval:
    for column in row:
        if column == "#":
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
game_win = False
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
    text = font.render("Score: "+str(score),True,(0, 0, 0))
    screen.blit(text, [700,100])
    text1 = font.render("Life: "+str(life),True,(0, 0, 0))
    screen.blit(text1, [700,135])
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit_program = True
            
    if not game_over or game_win:
        SS+=1
        monsters.update()
        monsters1.update()
        player.update()
        clown.update()
        shard.update()
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
    if game_win:
        text = font.render("You win!", True, white)
        textpos = text.get_rect(centerx=background.get_width()/2)
        textpos.top = 300
        screen.blit(text, textpos)
        exit_program = True
    if pygame.sprite.spritecollide(player, balls, False):
        diff = (player.rect.x + player.width/2) - (ball.rect.x+ball.width/2)
        ball.rect.y = screen.get_height() - player.rect.height - ball.rect.height - 1
        ball.bounce(diff)
    deadblocks = pygame.sprite.spritecollide(ball, blocks, True)
    deadmonsters = pygame.sprite.spritecollide(ball, monsters, True)
    deadimp = pygame.sprite.spritecollide(ball, monsters1, True)
    destroychest = pygame.sprite.spritecollide(ball, chests, True)
    takecoin = pygame.sprite.spritecollide(player, bonuses, True)
    hit = pygame.sprite.spritecollide(player, atacks, True)
    hit2 = pygame.sprite.spritecollide(player, monsters, True)
    if len(deadblocks) > 0:
        ball.bounce(0)
        score +=10
    if len(deadmonsters)> 0:
        score +=500
        if len(monsters) == 0 and len(deadimp) == 0:
            game_win = True

    if len(takecoin) > 0:
        KK+=1
        Ball.width = 30
        Ball.height = 30
        Ball.speed = 7.5
        ball.__init__(KK)
    if len(destroychest) > 0:
        bon.kill()
        ball.bounce(0)
        x, y = ball.x, ball.y - 30
        bon = Coin (x, y, 15)
        allsprites.add(bon)
        bonuses.add(bon)
        score +=20
    if len(hit) > 0:
        player.x = 450
        life -=1
    if len(hit2) > 0:
        player.x = 450
        life -=1
    if len(deadimp) >0:
        score +=500
        VV=0
    if VV==1:
        if (SS//150)==1:
            shard.kill()
            x, y = clown.rect.x, clown.rect.y
            shard = Fireball(x, y)
            allsprites.add(shard)
            atacks.add(shard)
            SS=0

    allsprites.draw(screen)
 
    pygame.display.flip()
 
pygame.quit()