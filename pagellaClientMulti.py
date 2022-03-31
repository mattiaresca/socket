#nome del file : pagellaClientMulti.py
import socket
import sys
import random
import os
import time
import threading
import multiprocessing
import json
import pprint

SERVER_ADDRESS = '127.0.0.1'
SERVER_PORT = 22225
NUM_WORKERS=4

#Versione 1 
def genera_richieste1(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    studenti=['studente0','studente1','studente3','studente4']
    materie=['matematica','italiano','inglese','storia e geografia']
    voto=random.randint(1,10)
    assenze=random.randint(1,5)
    materia=materie[random.randint(0,3)]
    studente=studenti[random.randint(0,4)]
    messaggio={
            'studente':studente, 
            'materia':materia, 
            'voto':voto,
            'assenze':assenze}
    print(f"Dati inviato al server {messaggio}")
    messaggio=json.dumps(messaggio)
    s.sendall(messaggio.encode("UTF-8"))
    data=s.recv(1024)
    data=data.decode()
    data=json.loads(data)
    print(f"dati ricevuti dal server {data}")
    #   di uno studente (valori ammessi: 5 cognomi a caso tra cui il tuo cognome)
    #   di una materia (valori ammessi: Matematica, Italiano, inglese, Storia e Geografia)
    #   di un voto (valori ammessi 1 ..10)
    #   delle assenze (valori ammessi 1..5) 
    #2. comporre il messaggio, inviarlo come json
    #   esempio: {'studente': 'Studente4', 'materia': 'Italiano', 'voto': 2, 'assenze': 3}
    #3. ricevere il risultato come json: {'studente':'Studente4','materia':'italiano','valutazione':'Gravemente insufficiente'}

    if not data:
        print(f"{threading.current_thread().name}: Server non risponde. Exit")
    else:
        #4 stampare la valutazione ricevuta esempio: La valutazione di Studente4 in italiano è Gravemente insufficiente
        studente=data['studente']
        materia=data['materia']
        print(f"{threading.current_thread().name}: la valutazione di {data['studente']} in {data['materia']} è {data['valutazione']}")
    s.close()


def genera_richieste2(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}connessione al server: {address}:{port} \n")
    except:
         print(f"\n{threading.current_thread().name} qualcosa è andato storto, sto uscendo... \n")
         sys.exit()
    studenti=['studente0','studente1','studente3','studente4']
    materie=['matematica','italiano','inglese','storia e geografia']
    studente=studenti[random.randint(0,4)]
    pagella=[]
    for m in materie:
        voto=random.randint(1,10)
        assenze=random.randint(1,5)
        pagella.append((m,voto,assenze))
    #compongo il messaggio 
    messaggio={'studente':studente,
    'pagella': pagella}
    print(f"dati inviati al server {messaggio}")
    messaggio=json.dumps(messaggio)
    s.sendall(messaggio.encode("utf-8"))
    data=s.recv(1024)
    data=data.decode()
    data=json.loads(data)
    print(f"dati ricevuti dal server {data}")

    if not data:
        print(f"{threading.current_thread().name}: server non risponde. exit")
    else:
        print(f"{threading.current_thread().name}:lo studente {data['studente']} ha una media di: {data['media']:.2f} e un totale di assenze: {data['assenze']}")
        s.close()
#Versione 3

def genera_richieste3(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}connessione al server: {address}:{port} \n")
    except:
         print(f"\n{threading.current_thread().name} qualcosa è andato storto, sto uscendo... \n")
         sys.exit()
    studenti=['studente0','studente1','studente3','studente4']
    materie=['matematica','italiano','inglese','storia e geografia']
    studente=studenti[random.randint(0,4)]
    pagella=[]
    for m in materie:
        voto=random.randint(1,10)
        assenze=random.randint(1,5)
        pagella.append((m,voto,assenze))
    tabellone[stud]=pagella 
    print("dati inviati al server")
    pp=pprint.PrettyPrinter(indent=4)
    pp.pprint(tabellone)
    tabellone=json.dumps(tabellone)
    s.sendall(tabellone.encode("UTF-8"))
    data=s.recv(1024)
    data=data.decode()
    data=json.loads(data)
    print("dati ricevuti dal server")
    pp.pprint(data)

    if not data:
        print(f"{threading.current_thread().name}: server non risponde. exit")
    else:
        print(f"{threading.current_thread().name}:lo studente {data['studente']} ha una media di: {data['media']:.2f} e un totale di assenze: {data['assenze']}")
        s.close()
 
if __name__ == '__main__':
    start_time=time.time()
    # 3 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste alla quale passo i parametri (num,SERVER_ADDRESS, SERVER_PORT)
    for num in range(0, NUM_WORKERS):
        genera_richieste(num, SERVER_ADDRESS, SERVER_PORT)

    end_time=time.time()
    print("Total SERIAL time=", end_time - start_time)
    start_time=time.time()
    #Creo due liste, tra le quali threads e process
    threads=[]
    
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    #For che crea i mie thread
    for num in range (NUM_WORKERS):
        # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(threading.Thread(target=genera_richieste1, args=(num, SERVER_ADDRESS, SERVER_PORT,)))
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    end_time=time.time()
    print("total threads time=", end_time-start_time)

    start_time=time.time()
    process=[]
    for num in range(0, NUM_WORKERS):
        process.append(multiprocessing.Process(target=genera_richieste1, args=(num, SERVER_ADDRESS, SERVER_PORT)))
    
    [process.start() for process in process]
    [process.join() for process in process]
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)