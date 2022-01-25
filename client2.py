import socket 
import json
HOST="127.0.0.1"
PORT=65432

with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    while True:
        primoNumero= input("inserisci il primo numero. exit() per uscire")
        if primoNumero=="exit()":
            break
        primoNumero=float(primoNumero)
        operazione=input("insersci l'operazione (+,-,*,/,%)")
        secondoNumero=float(input("inserisci il secondo numero"))
        messaggio={'primoNumero':primoNumero, 'operazione': operazione, 'secondoNumero': secondoNumero}
        messaggio=json.dumps(messaggio) 
        #trasforma l'oggetto in stringa
        s.sendall(messaggio.encode("UTF-8"))
        data=s.recv(1024)
        #aspettiamo che il server risponda 
        print("Risultato: ", data.decode())