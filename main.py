import os, sys
import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((480,480))
pygame.display.set_caption("Moving Around")
pygame.mouse.set_visible(0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

#game loop, game never runs faster than 60 frames
clock = pygame.time.Clock()
while True:
    clock.tick(60)
    
    #Event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit() 