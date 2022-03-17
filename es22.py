# 4.a DOWNLOAD PAGE - SERIAL MODE

import time
import logging
import requests
import os
 
 
class WebsiteDownException(Exception):
    pass
 
 

def count_words(content,address): #funzione che permette di contate le lettere in un messqggio 
  #1...
  #stampo il numero di parole contenute in content (home page di address)
  parole=content.split(" ") #fa lo spleet del messaggio  
  print(f"num parole:{address}, num.{str(len(parole))}")#si ottiene in output la lungheza del messaggio
  pass

def get_file_name(address):
  #2...
  #ricavo il nome del file .txt da creare dall'indirizzo ricevuto come parametro
  #es.da http://amazon.com ottengo amazon.txt
  sito=address.split("://") #con questo split dividiamo il l'http dal nome del sito 
  sito2=sito[1].split(".") #con quest'altro split il resto dal dominio 
  return sito2[0]+".txt"
  pass

def save_homepage(address, timeout=20):
    """
    
    """
    try:
        #3...
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
        logging.warning("Timeout expired for website %s" % address)
        raise WebsiteDownException()
         
 
def notify_owner(address):#gestisce una serie di notifiche quando vengono inseriti gli url 
    """ 
    Simuliamo l'invio di una email di notifica all'admin del sito che non risponde
    """
    logging.info("Notifying the owner of %s website" % address)#qua si memorizzano tutti gli url da mandare una notifica 
    time.sleep(0.5)#tempo della funzione 
     
 

def manage_homepage(address):
    """
    Carica l'home page del sito, crea un file, salva il contenuto, 
    ricarica il contenuto dal file, conta le parole, chiude e rimuove il file
    """
    try:
        save_homepage(address)
    except WebsiteDownException:
        notify_owner(address)



if __name__ == "__main__":
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
    start_time = time.time() #tempo di inizio del programma 
 
    for address in WEBSITE_LIST:
        #4..
        #chiamo l'opportuna funzione alla quale passo l'indirizzo
        manage_homepage(address)    
    end_time = time.time() #restituirà in qunto tempo viene eseguita la funzione   
    
    print("Tempo di esecuzione seriale : %ssecs" % (end_time - start_time))
    #viene visualizzato il tempo di eseguzione del programma 