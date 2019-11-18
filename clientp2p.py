import os
import socket
import sys
from threading import Thread
import time

H_size = 5

def Chat():
    global name
    global broadcast
    global online
    while True:
        
        recvd = broadcast.recv(1024).decode('utf-8')

        if not len(recvd):
             return False
        username_size = int(recvd[:H_size].strip())
        username = recvd[H_size:H_size + username_size]                   
        
        if username[:1] == 'm' and username[1:] != name:#msg
           
           message_header = recvd[H_size + username_size:H_size + username_size + H_size]
           
           if not len(message_header):
             return False
           message_length = int(message_header.strip())
           message = recvd[H_size + username_size + H_size:H_size + username_size + H_size + message_length]

           print( username[1:] + ">>" + message)
         
        elif username[:1] == 'o':#user entrou
          
           if not(username[1:] in online):
             online.append(username[1:])
             print("***New user: " + username[1:] + "***")
             print('***Total Online User: ' + str(len(online))+ "***")             
             
        elif username[:1] == 's':#user saiu/ há bug
           if (user[1:] in online):
             online.remove(username[1:])
             print("***User disconnected: " + username[1:] + "***")
             print('***Total Online User: ' + str(len(online))+ "***")

def SendMessage():
    global name
    global send
    send.setblocking(False)           
    while True:
        
        data = input(name + ">>")

        
        if data == 'Quit()':
            username =  ('s'+ name).encode('utf-8')
            username_header = f"{len(username):<{H_size}}".encode('utf-8')            
            send.sendto(username_header + username, ('255.255.255.255', 2000)) 
            os._exit(1)            
          
        elif data != '':
            username =  ('m'+ name).encode('utf-8')
            username_header = f"{len(username):<{H_size}}".encode('utf-8')
            message = data.encode('utf-8')
            message_header = f"{len(message):<{H_size}}".encode('utf-8')
            send.sendto(username_header + username + message_header + message,('255.255.255.255', 2000))

def SendUsername():
    global name
    global send
    send.setblocking(False)
    username = ('o' + name).encode('utf-8')
    username_header = f"{len(username):<{H_size}}".encode('utf-8')
    while True:                             
        time.sleep(1)
        send.sendto(username_header + username, ('255.255.255.255', 2000))  


def main():
    global broadcast

    broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)      
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)   
    broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)   
    broadcast.bind(('0.0.0.0', 2000))                                 
    global send
    send = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)           
    send.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)         

    print('Welcome to the Chat!')
    print('Type Quit() to quit')
    
    global name
    name = ''                                                   
    while True:                                                 
        if not name:
            name = input('Username: ')
            if not name:
                print('Enter a valid username')
            else:
                break
    print('*************************************************')  

    global recvThread
    recvThread = Thread(target=Chat) 

    global sendMsgThread
    sendMsgThread = Thread(target=SendMessage)  

    global online
    online = []   

    global sendOnlineThread
    sendOnlineThread = Thread(target=SendUsername) 

    recvThread.start() #inicia thread                                          
    sendMsgThread.start() #inicia envio de  msg                                       
    sendOnlineThread.start() #envia quem está na rede

    recvThread.join()                                           
    sendMsgThread.join()                                        
    sendOnlineThread.join()                                     

if __name__ == '__main__':
    main()
