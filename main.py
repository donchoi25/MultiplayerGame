import os, sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640,480))
pygame.display.set_caption("Moving Around")
pygame.mouse.set_visible(0)

class Player(pygame.sprite.Sprite):
    def __init__(self, image, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.speed = speed
        self.image = image
        self.pos = image.get_rect().move(0,height)
    def move(self):
        self.pos = self.pos.move(0, self.speed)
        if self.pos.right > 600:
            self.pos.left = 0

#creating player 1
playerimg = pygame.image.load('player.png').convert()
playerimg = pygame.transform.scale(playerimg, (40,40))
player1 = Player(playerimg,0,0)

#creating background
#background = pygame.image.load('bg.jpeg').convert()
#screen.blit(background, (0, 0))

#main game loop
while True:
    screen.blit(player1.image, player1.pos)
    
    #Event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() 
            
    pygame.display.update()
    pygame.time.delay(100)