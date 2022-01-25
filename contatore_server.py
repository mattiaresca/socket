import socket
import json

HOST='127.0.0.1'
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    contatore=1 
    s.bind((HOST, PORT))#tupla: array non modificabile
    s.listen()
    print("[*] In ascolto su %s:%d "%(HOST, PORT))
    #conversione del client
    clientsocket, address=s.accept()#accetta la conversione
    with clientsocket as cs:
        print("Connessione da ", address)
        while True:
            data=cs.recv(1024)
            if not data: #se data è un vettore vuoto risulta false; sennò true/if len(data)==0/se è vuoto esce, sennò continua
                break
            data=data.decode()
            data=json.loads(data)
            stringa=data['stringa']
            if stringa != "ko":
                ris="messaggio numero"+ str(contatore)+ ":" +stringa
                contatore+=1
            #risposta al client
            else:
                ris='Ricevuto "ko" dal server'
            cs.sendall(ris.encode("UTF-8"))
            print(ris)
            #Fine parte server