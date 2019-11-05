import socket

def Main():
    host='127.0.0.1'
    port=2000
    Type="utf-8"
    clientName="CLIENTname"
    
    client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    client.connect((host,port))

    client.send(bytes(clientName,Type))
    from_server=''
    while True:
        
        serverData = client.recv(4096)
        
        if len(serverData)<=0:
            break
            
        from_server+=serverData.decode(Type)
        print(from_server)    
        
    #client.close()
    
if __name__=='__main__':
    Main()
