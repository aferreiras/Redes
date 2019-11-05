import socket

def Main():
    host='127.0.0.1'
    port=2000
    Type="utf-8"

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    serv.bind((host, port))
    serv.listen(5)

    while True:
        conn, addr = serv.accept()
        from_client = ''
        print("Connection from {addr} has been established!")

        Data = conn.recv(4096)
            
        if len(Data)<=0:
            break
            
        from_client += Data.decode(Type)
        print(from_client)

        conn.send(bytes("You're connected to SERVER",Type))

        conn.close()
            
        print('client disconnected')
if __name__=='__main__':
    Main()
