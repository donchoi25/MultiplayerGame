import socket  
import json     
import atexit        

s = socket.socket()         # Create a socket object
host = '127.0.0.1'    #ip address of machine
port = 65431         
s.bind((host, port))       

#current playerid
playerid = 0
#creating map that tracks player information
playerLocation = {}

#closes the port on program exit
def exit_handler():
    print("port successfully closed")
    s.close()       
  
atexit.register(exit_handler)

#5 players possible
s.listen(5)  
#accepts any new connections
c, addr = s.accept()                    

while True:
   received = c.recv(1024).decode()
   #if a new player is being created, assign a unique player id
   if received == "Player Created":
      c.sendall(str(playerid).encode())
      print("Player Created ID: ", playerid)
      playerid += 1
   #location information on server needs to be updated
   elif received != None:
      #turn json into dic
      print(received)
      jsonDic = json.loads(received)
      #update the dictionary
      playerLocation[jsonDic["id"]] = (jsonDic["posx"], jsonDic["posy"])
   else:
      print(playerLocation)