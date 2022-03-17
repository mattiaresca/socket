# 4.2 DOWNLOAD PAGE - THREAD MODE
"""
url=get_file_name(address)
file = open (url, "wr")
file.write(r.text)
file.close()
file = open (url, "r")
count_words(file.read(), address)
file.close()
os.remove(url)
"""
#Importo le solite librerie
import time
import logging
import requests
from queue import Queue
from threading import Thread
import os
 
#Creo una classe, chiamata WebsiteDownException, a cui passo l'Exception, che
#mi permette di gestire le eccezioni, quindi è un metido chiaro e semplice che
#mi consente di gestire gli errori: a questa passo per l'appunto la Exception,
#il quale è il parametro base per ogni classe eccezione. 
class WebsiteDownException(Exception):
    """
    Eventuale gestione dell'errore dovuto al sito che non risponde     
    """
    #"pass" in python significa è un costrutto "null", che significa che noi lo utilizziamo
    #come se fosse una sorta di segnaposto, di conseguenza lo utilizziamo per costruira
    #sorta di corpo che non fa nulla; infatti, tradotto in italiano, significa "passa".
    #Di fatti risulta molto utile nei cicli con un possibile loop infinito; nelle funzioni
    #o addirittira nelle classi, come in questo caso.
    pass
          
#Funzione "notify_owner", nel quale passo l'ip address.  
#E' necessario per mandare una serie di notifica quando io inserisco gli url. 
def notify_owner(address):
  """ 
  Simuliamo l'invio di una email di notifica all'admin del sito che non risponde
  """
  #4.gestisco una lista in cui memorizzo tutti gli url a cui mandare una notifica
  #memorizzo tutti gli url a cui mandare successivamente una notifica
  logging.info("Notifying the owner of %s website" % address)
   #tempo in cui indico quanto deve "dormire" la funzione
  time.sleep(0.5)


def count_words(content,address):
  #1...
  #stampo il numero di parole contenute in content (home page di address)
  #Eseguo uno split del "messaggio"
  parole=content.split(" ")
  #Visualizzo la lunghezza totale del messaggio contando le lettere di un "x" address
  print(f"Numero di parole del sito: {address}, num.{str(len(parole))}" )
  pass

def get_file_name(address):
  #2...
  #ricavo il nome del file .txt da creare dall'indirizzo ricevuto come parametro
  #es.da http://amazon.com ottengo amazon.txt
  #Faccio un primo split per dividere http dal nome del sito (es. http://amazon.com
  #verra diviso in "http" e "amazon.com")
  sito=address.split("://")
  #creo un secondo split che divida il "secondo elemento" (quindi amazon. come diventa
  #"amazon" e "com")
  sito2=sito[1].split(".")
  #Aggiungo al nome del mio sito il ".txt" (amazon diventa amazon.txt)
  return sito2[0] + ".txt"
  pass

def save_homepage(address, timeout=20):
    """
    Carica l'home page del sito, crea un file, salva il contenuto, 
    lo ricarica dal file, conta le parole, chiude e rimuove il file
    """
    #Faccio il try except
    #3...
    try:
        #carico il contenuto dell'home page di address
        request=requests.head(address, timeout=timeout)
        #lo scrivo in un file il cui nome lo ottengo chiamando la funzione get_file_name
        if (request.status_code>=400):
          raise WebsiteDownException()
        url=get_file_name(address)
        file=open(url, "w")
        r=requests.get(address)
        file.write(r.text)
        #chiudo il file
        file.close()
        #riapro il file 
        file=open(url, "r")
        #leggo il contenuto
        leggo=file.read()
        #conto le parole chiamando la funzione count_words
        count_words(leggo, address)
        #cancello il file
        os.remove(url)
        pass
    except requests.exceptions.RequestException:
        logging.warning("Problem to get website %s" % address)
        raise WebsiteDownException()
            

#Faccio la funzione "manage_homepage"
def manage_homepage(address):
    try:
        save_homepage(address)
    except WebsiteDownException:
        notify_owner(address)
#definisco la funzione "worker"
def worker():
#Eseguo un ciclo while
    # commenta ...
    while True:
        address = task_queue.get()
        manage_homepage(address)
        # commenta ...
        task_queue.task_done()

#Siti:
if _name_ == "_main_":
    WEBSITE_LIST = [
    'https://envato.com',
    'http://amazon.com',
    'http://facebook.com',
    'http://google.com',
    'http://google.fr',
    'http://google.es',
    'http://internet.org',
    'http://gmail.com',
    'http://stackoverflow.com',
    'http://github.com',
    'http://heroku.com',
    'http://really-cool-available-domain.com',
    'http://djangoproject.com',
    'http://rubyonrails.org',
    'http://basecamp.com',
    'http://trello.com',
    'http://yiiframework.com',
    'http://shopify.com',
    'http://another-really-interesting-domain.co',
    'http://airbnb.com',
    'http://instagram.com',
    'http://snapchat.com',
    'http://youtube.com',
    'http://baidu.com',
    'http://yahoo.com',
    'http://live.com',
    'http://linkedin.com',
    'http://yandex.ru',
    'http://netflix.com',
    'http://wordpress.com',
    'http://bing.com',
]

#Indico il "numero" di "lavoratori", che è uguala 4.
NUM_WORKERS = 4

#Creo una "coda"
task_queue = Queue()

#Individuo il tempo iniziale di esecuzione
start_time = time.time()

# commenta ...
#Creo una lista ed aggiungo una serie di numeri
lista1=[1,2,3,4,5,6,7]
#Creo una seconda lista i cui valori sono ottenuti dai valori della prima lista moltiplicando ogni elemento per 2
lista2 = [elemento*2 for elemento in lista1 ]
#Visualizzo la seconda lista, appena ottenuta.
print(lista2) 

# commenta ...
#Nella seguente istruzione io creo i vari thread,
#usufruendo anche di un for in cui non indico l'elemento
#perché sarebbe superfluo, cioè è una cosa trascurabile
#in quanto è già palesato nel codice come l'istruzione
#influerà sul numero dei "workers"
threads = [Thread(target=worker) for _ in range(NUM_WORKERS)]
 
# commenta ...
[task_queue.put(item) for item in WEBSITE_LIST]
 
# commenta ...
#Avvio tutti i thread
[thread.start() for thread in threads]
 
# commenta ...
#Uso la funzione "join" sulla coda
task_queue.join()

#Individuo il tempo finale di esecuzione         
end_time = time.time()        

#Visualizzo il tempo totale di esecuzione 
print("Time for ThreadedSquirrel: %ssecs" % (end_time - start_time))