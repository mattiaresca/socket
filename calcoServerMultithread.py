
   
#Importo le solite classi: socket, json e threading.
import socket
import json
from threading import Thread

SERVER_ADDRESS='127.0.0.1'
SERVER_PORT=20019

def ricevi_comandi(sock_service, addr_client):
    print("avviato")
    while True:
            data=sock_service.recv(1024)
            if not data: #se data è un vettore vuoto risulta false; sennò true/if len(data)==0/se è vuoto esce, sennò continua
                break
            #Istruzione data a cui passo i dati, e dopo faccio la stessa cosa
            #creando tre variabili a cui passo rispettivamente solo "primoNumero", "operazione" e, infine, secondoNumero
            data=data.decode()
            data=json.loads(data)
            primoNumero=data['primoNumero']
            operazione=data['operazione']
            secondoNumero=data['secondoNumero']
            #Sequenza di if ed elif per cui scelgo nel "ris" la tipologia di operazione e,
            #infine, eseguo l'operazione stessa, per poi alla fine visualizzare il tutto.
            ris=""
            if operazione=="+":
                ris=primoNumero+secondoNumero
            elif operazione=="-":
                ris=primoNumero-secondoNumero
            elif operazione=="*":
                ris=primoNumero*secondoNumero
            elif operazione=="/":
                #Questo è un controllo per cui indico, ad esempio, che non si può dividere per 0.
                if secondoNumero==0:
                    ris="Non puoi dividere per 0"
                else:
                    ris=primoNumero/secondoNumero
            elif operazione=="%":
                ris=primoNumero%secondoNumero
            else:
                ris="Operazione non riuscita"
            ris=str(ris)#Casting a stringa
            #risposta al client
            sock_service.sendall(ris.encode("UTF-8"))
            #Fine parte server
    sock_service.close()

#Funzione "ricevi_connessione" a cui passo la "sock_listen"
def ricevi_connessioni(sock_listen):
    #Ciclo While che continua a girare sino a che il valore continua a rimanere True
    while True:

        sock_service, addr_client=sock_listen.accept()
        #Visualizzo due print, in cui creo dei thread per eseguire le mie operazioni
        print("\nConnessione ricevuta da "+str(addr_client))
        print("\nCreo un thread per servire le richieste ")
        #Funzioni try e except, con successivo controllo degli errori
        try:
            Thread(target=ricevi_comandi, args=(sock_service, addr_client)).start()
        except:
            print("il thread non si avvia ")
            sock_listen.close()

#Funzione avvia server che si avvia una volta che la funzione successiva è terminata
def avvia_server(indirizzo, porta):
    sock_listen=socket.socket()
    sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock_listen.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock_listen.bind((SERVER_ADDRESS, SERVER_PORT))
    #Sequnze di istruzioni che indicano l'avvio dell'ascolto
    sock_listen.listen(5)
    print("Server in ascolto su %s." % str((SERVER_ADDRESS, SERVER_PORT)))
    ricevi_connessioni(sock_listen)

#Ulteriore if, che indica che il programma è funzionante e che perciò può avviarsi la connessione
if __name__=='__main__':
    avvia_server(SERVER_ADDRESS, SERVER_PORT)