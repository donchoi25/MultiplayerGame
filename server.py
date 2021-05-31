import socket  
import time
import json     
import atexit    
import re    
import _thread
from threading import RLock

s = socket.socket()         # Create a socket object
host = '127.0.0.1'    #ip address of machine
port = 65431         
s.bind((host, port))       

#current playerid
playerid = 0
#creating map that tracks player information
playerLocation = {"msg":"PlayerLocation"}

#create a lock for playerLocation and playerid
lock = RLock()

#create function for new client threads
def on_new_client(clientsocket,addr):
   global playerid
   while True:
      msg = clientsocket.recv(1024).decode()
      #Seperates all messages into a list. Assume all messages are a json
      receivedList = [e + "}" for e in msg.split("}") if e]

      for received in receivedList:
         #turns json into dic
         jsonDic = json.loads(received)

         #if a new player is being created, assign a unique player id
         if jsonDic["msg"] == "PlayerCreated":
            newMsg = {"msg":"PlayerID","playerid" : playerid}
            #update the dictionary, and send back unique id
            with lock:
               playerLocation[playerid] = (jsonDic["posx"], jsonDic["posy"])   
               playerid += 1   
            clientsocket.sendall(str.encode(json.dumps(newMsg))) 
            print("Player Created ID: ", playerid)
         #location information on server needs to be updated
         elif jsonDic["msg"] == "LocationChanged":
            #update the dictionary
            with lock:
               playerLocation[jsonDic["id"]] = (jsonDic["posx"], jsonDic["posy"])
               print(playerLocation)

   clientsocket.close()

def sendLocToClient(clients, frames):
   while True:
      #send location info to all clients
      for client in clients:
         client.sendall(str.encode(json.dumps(playerLocation)))
      #sleep until the next frame
      time.sleep(frames)

#closes the port on program exit
def exit_handler():
    print("port successfully closed")
    s.close()       
  
atexit.register(exit_handler)

#5 players possible
s.listen(5)  

#list of connections
clients = []

#30 frames
frames = 1.0/150
#send data to clients every frame
_thread.start_new_thread(sendLocToClient,(clients,frames))

while True:
   #accepts any new connections
   c, addr = s.accept() 
   clients.append(c)
   _thread.start_new_thread(on_new_client,(c,addr))