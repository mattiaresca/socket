import socket
from threading import Thread
from tkinter import SE
import json
from xmlrpc.client import Server

SERVER_ADDRESS='127.0.0.1'
SERVER_PORT=22225
class Server():
    "questa classe rappresenta un server"
    def __init__(self,address,port):
        self.address=address
        self.port=port


    def avvia_server(self):
        """
        Metodo per aprirsi e mettersi in 
        ascolto aspettando richieste 
        di server 
        """
        sock_listen = socket.socket()
        sock_listen.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
        sock_listen.bind((self.address, self.port))
        sock_listen.listen(5)
        print("Server in ascolto su %s."%str((self.address,self.port)))
        return sock_listen
    
    def accetta_connessioni(self,sock_listen):
        while True:
            sock_service, addr_client = sock_listen.accept()
            print("\nConnessione ricevuta da " + str(addr_client))
            print("\nCreo un thread per servire le richieste")
            try:
                Thread(target=self.ricevi_comandi, args=(sock_service, addr_client)).start()
            except:
                print("Il thread non si avvia")
                sock_listen.close()

    def ricevi_comandi(self,sock_service,addr_client):
        print("avviato")
        while True:
            data=sock_service.recv(2048)
            if not data:
                break
            data=data.decode()
            data=json.loads(data)
            primoNumero=data['primoNumero']
            operazione=data['operazione']
            secondoNumero=data['secondoNumero']
            ris=""
            if operazione=="+":
                ris=primoNumero+secondoNumero
            elif operazione=="-":
                ris=primoNumero-secondoNumero
            elif operazione=="*":
                ris=primoNumero*secondoNumero
            elif operazione=="/":
                if secondoNumero==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="Operazione non riconosciuta"
            ris=str(ris)
            sock_service.sendall(ris.encode("UTF-8"))
        sock_service.close()
s1=Server(SERVER_ADDRESS,SERVER_PORT)
sock_lis=s1.avvia_server()
s1.accetta_connessioni(sock_lis)