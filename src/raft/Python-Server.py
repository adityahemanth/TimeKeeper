import socket
import time
def main():
    
    host = "0.0.0.0"
    port = 5001
    
    mySocket=socket.socket()
    mySocket.bind((host,port))
    
    mySocket.listen(1)
    
    conn,addr=mySocket.accept()
    
    print("Connection fron: " + str(addr))
    
    while True:
        data=conn.recv(1024).decode()
        if not data:
            break
            
        print("from connected user: "+str(data))
        
        data=str(data).upper()
        print("Received from User: "+str(data))
        
        data=input("?")
        conn.send(data.encode())
    
    conn.close()
    
if __name__ == '__main__':
    main()