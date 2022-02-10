import socket
import json

HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        stringa=input('Inserire la stringa, "KO" per uscire: ')
        messaggio={
            'stringa': stringa
        }
        messaggio=json.dumps(messaggio) #trasforma l'oggetto indicato  in una stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        if (stringa.find('#list') != -1):
            deserialized_voti = json.loads(data)
        elif (stringa.find('#get') != -1):
            deserialized_voti = json.loads(data)
        else:
            deserialized_voti = data.decode()
        print("\n")
        print(deserialized_voti,"\n")