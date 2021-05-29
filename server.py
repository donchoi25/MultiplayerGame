import socket  
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
playerLocation = {}

#create a lock
lock = RLock()

#create function for new client threads
def on_new_client(clientsocket,addr):
   global playerid
   while True:
      msg = clientsocket.recv(1024).decode()
      #Seperates all messages into a list. Assume all messages are enclosed in {}
      receivedList = [e + "}" for e in msg.split("}") if e]

      for received in receivedList:
         #if a new player is being created, assign a unique player id
         if received == "{PlayerCreated}":
            with lock:
               clientsocket.sendall(str(playerid).encode())
               playerid += 1
            print("Player Created ID: ", playerid)
         #location information on server needs to be updated
         elif received != None:
            #turn json into dic
            jsonDic = json.loads(received)
            #update the dictionary
            with lock:
               playerLocation[jsonDic["id"]] = (jsonDic["posx"], jsonDic["posy"])
               print(playerLocation)

   clientsocket.close()


#closes the port on program exit
def exit_handler():
    print("port successfully closed")
    s.close()       
  
atexit.register(exit_handler)

#5 players possible
s.listen(5)  
                   

while True:
   #accepts any new connections
   c, addr = s.accept() 
   _thread.start_new_thread(on_new_client,(c,addr))