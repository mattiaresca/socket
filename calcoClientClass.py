import socket
from threading import Thread
import json
from calcoClientMultithread import SERVER_ADDRESS, SERVER_PORT 
SSERVER_ADDRESS= '127.0,0,1'
SERVER_PORT=22225
class Client():
    """
    questa classe rappresenta una persona 
    che opera con client
    """
    def connessione_server(self,address,port):
        """
        metodo per stabilire la connessione con il server 
        """
        sock_service=socket.socket()
        sock_service.connect((address,port))
        return sock_service

    def invia_comandi(self,sock_service):
        """
        metodo per inviare le richieste
        di servizio e ricevere le risorse
        """
        while True:
            primoNumero=input("Inserisci il primo numero exit() per uscire: ")
            if primoNumero=="exit()":
                break
            primoNumero=float(primoNumero)
            operazione=input("Inserisci l'operazione (+,-,*,/,%): ")
            secondoNumero=float(input("Inserisci il secondo numero: "))
            messaggio={
                'primoNumero':primoNumero, 
                'operazione':operazione, 
                'secondoNumero':secondoNumero
            }
            messaggio=json.dumps(messaggio) #trasforma l'oggetto dato in una stringa
            sock_service.sendall(messaggio.encode("UTF-8"))
            data=sock_service.recv(2048)
            print("Risultato: ", data.decode())
            if not data:
                print("Server non risponde. Exit")
                break
            data=data.decode()
            print("ricevuto dal server")
            print(data+'\n')
c1=Client()
sock_serv=c1.connessione_server(SERVER_ADDRESS,SERVER_PORT)
c1.invia_comandi(sock_serv)