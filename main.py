import os, sys
import json
import pygame
import socket
import _thread
from threading import RLock
from pygame.locals import *

#setting up socket
s = socket.socket()
host = '127.0.0.1' 
port = 65431 
s.connect((host, port))

#initializing game screen
pygame.init()
screen = pygame.display.set_mode((500,500))
pygame.display.set_caption("Moving Around")

#create a lock for pygame
lock = RLock()

#player class, created for every client
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.id = -1

        #send player information to server
        jsonDic = {"msg": "PlayerCreated",
                  "posx":str(self.x),
                  "posy":str(self.y)}
        s.sendall(str.encode(json.dumps(jsonDic)))
        self.id = -1
    def processServer(self):
        msg = s.recv(1024).decode()
        #Seperates all messages into a list. Assume all messages are a json
        receivedList = [e + "}" for e in msg.split("}") if e]
        
        #process all msgs one at a time
        for received in receivedList:
           jsonDic = json.loads(received)
           
           #if PlayerID msg, then update the player id
           if jsonDic["msg"] == "PlayerID":
              self.id = jsonDic["playerid"]
           #if PlayerLocation msg, then update the screen
           if jsonDic["msg"] == "PlayerLocation":
               with lock:
                  #draw the other players
                  for playerid in jsonDic:
                     #ignore the msg entry and ignore local player
                     if playerid != "msg" and playerid != self.id:
                        loc = jsonDic[playerid]
                        pygame.draw.rect(screen, (255, 0, 0), (int(loc[0]), int(loc[1]), self.width, self.height))
               
               pygame.display.update()

    def draw(self):
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height))
    def moveY(self, dir):
        self.y += self.speed * dir
        jsonDic = {"msg": "LocationChanged",
                  "id":self.id,
                  "posx":self.x, 
                  "posy":self.y}
        s.sendall(str.encode(json.dumps(jsonDic)))
    def moveX(self, dir):
        self.x += self.speed * dir
        jsonDic = {"msg": "LocationChanged",
                  "id":self.id,
                  "posx":self.x, 
                  "posy":self.y}
        s.sendall(str.encode(json.dumps(jsonDic)))

#creating player 1
player1 = Player(200,200,20,20,10)

#create thread for processing server messages
def processServerMessages():
   while True:
      player1.processServer()

#tracks locations of all other players, received from server
masterloc = {}

_thread.start_new_thread(processServerMessages,())

#game is running
run = True

#main game loop
while run:    
    #Event listener
    for event in pygame.event.get():
        if event.type == QUIT:
            run = False
    
    #stores keys pressed
    keys = pygame.key.get_pressed()
    
    #if left arrow key is pressed
    if keys[pygame.K_LEFT] and player1.x > 0:
        player1.moveX(-1)
    #if right arrrow key is pressed
    if keys[pygame.K_RIGHT] and player1.x < 500 - player1.width:
        player1.moveX(1)
    #if up arrow key is pressed
    if keys[pygame.K_UP] and player1.y > 0:
        player1.moveY(-1)
    #if down arrow key is pressed
    if keys[pygame.K_DOWN] and player1.y < 500 - player1.height:
        player1.moveY(1)

    with lock:   
      #fill the screen with black color
      screen.fill((0,0,0))
    
    #draw the player
    player1.draw()
    
    #update pygame display
    pygame.display.update()

    pygame.time.delay(100)

#close the connection
s.close()