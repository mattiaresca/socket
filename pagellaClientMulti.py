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
def genera_richieste(num,address,port):
    try:
        s=socket.socket()
        s.connect((address,port))
        print(f"\n{threading.current_thread().name} {num+1}) Connessione al server: {address}:{port}")
    except:
        print(f"{threading.current_thread().name} Qualcosa è andato storto, sto uscendo... \n")
        sys.exit()

    #1. Generazione casuale:
    studente=""
    student=random.randint(0,5)
    if student==0:
        studente=" rossi"
    elif student==1:
        studente=" rescaldina"
    elif student==2:
        studente= "colomnbo"
    elif student==3:
        studente="nebuloni"
    else:
        studente="piero"

    materia=""
    mat=random.randint(0,5)
    if mat==0:
        materia=" matematica"
    elif mat==1:
        materia=" italiano"
    elif mat==2:
        materia= "inglese"
    elif mat==3:
        materia="storia"
    else:
        studente="geografia"
    voto=random.randint(1,10)
    assenza=random.randint(1,5)

    messaggio={
            'studente':studente, 
            'materia':materia, 
            'voto':voto,
            'assenza':assenza
        }
        
    
    messaggio=json.dumps(messaggio) #trasforma l'oggetto dato in una stringa
    s.sendall(messaggio.encode("UTF-8"))
    data=s.recv(1024)
    print("Risultato: ", data.decode())
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
        print(f"{threading.current_thread().name}")
    s.close()

#Versione 2 
#def genera_richieste2(num,address,port):
  #....
  #   1. Generazione casuale di uno studente(valori ammessi: 5 cognomi a caso scelti da una lista)
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: pagella={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9.5,3), ("Storia",8,2), ("Geografia",8,1)]}
  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json {'studente': 'Cognome1', 'media': 8.0, 'assenze': 8}

#Versione 3
#def genera_richieste3(num,address,port):
  #....
  #   1. Per ognuno degli studenti ammessi: 5 cognomi a caso scelti da una lista
  #   Per ognuna delle materie ammesse: Matematica, Italiano, inglese, Storia e Geografia)
  #   generazione di un voto (valori ammessi 1 ..10)
  #   e delle assenze (valori ammessi 1..5) 
  #   esempio: tabellone={"Cognome1":[("Matematica",8,1), ("Italiano",6,1), ("Inglese",9,3), ("Storia",8,2), ("Geografia",8,1)],
  #                       "Cognome2":[("Matematica",7,2), ("Italiano",5,3), ("Inglese",4,12), ("Storia",5,2), ("Geografia",4,1)],
  #                        .....}
  #2. comporre il messaggio, inviarlo come json
  #3  ricevere il risultato come json e stampare l'output come indicato in CONSOLE CLIENT V.3
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
    process=[]
    # 4 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un thread al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    #For che crea i mie thread
    for num in range (0, NUM_WORKERS):
        # ad ogni iterazione appendo il thread creato alla lista threads
        threads.append(threading.Thread(target=genera_richieste, args=(num, SERVER_ADDRESS, SERVER_PORT,)))
    
    # 5 avvio tutti i thread
    #For che avvia i thread
    for i in range (len(threads)):
        threads[i].start()
    # 6 aspetto la fine di tutti i thread 
    for i in range (len(threads)):
        threads[i].join()
    end_time=time.time()
    print("Total THREADS time= ", end_time - start_time)

    start_time=time.time()
    process=[]
    # 7 ciclo per chiamare NUM_WORKERS volte la funzione genera richieste tramite l'avvio di un processo al quale passo i parametri args=(num,SERVER_ADDRESS, SERVER_PORT,)
    #For che mi crea i processi
    for num in range(0, NUM_WORKERS):
        process.append(multiprocessing.Process(target=genera_richieste, args=(num, SERVER_ADDRESS, SERVER_PORT)))
    # 8 avvio tutti i processi
    #For che mi avvia i processi
    for num in range(0, NUM_WORKERS):
        process[num].start()
    # 9 aspetto la fine di tutti i processi 
    #For che attua i join nei miei processi
    for num in range(0, NUM_WORKERS):
        process[num].join()
    end_time=time.time()
    print("Total PROCESS time= ", end_time - start_time)