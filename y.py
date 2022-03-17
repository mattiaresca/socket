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


# 4.a DOWNLOAD PAGE - SERIAL MODE

#Importo le solite classi
import time
import logging
import requests
import os
 
#Creo la classe "Website" 
class WebsiteDownException(Exception):
    pass
 
 
#creo la classe "conta parole" al quale passo il mio "testo" e l'address
def count_words(content,address):
  #1...
  #stampo il numero di parole contenute in content (home page di address)
  #Eseguo uno split del "messaggio"
  parole=content.split(" ")
  #Visualizzo la lunghezza totale del messaggio contando le lettere di un "x" address
  print(f"Numero di parole del sito: {address}, num.{str(len(parole))}" )
  pass

#Creo la classe "ottieni nome file" al quale passo l'address
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

#Creo la funzione "salva homepage" alla quale passo l'address ed il timeout settato a 20
def save_homepage(address, timeout=20):
    #Faccio il try except
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
         
#Quanto segue è molto simile agli scorsi notebook: si fanno le varie funzioni
#che restituiscono la notifica con messaggi di "logging" e "maneggio" l'homepage
#chiamato una serie di funzioni 
def notify_owner(address):
    """ 
    Simuliamo l'invio di una email di notifica all'admin del sito che non risponde
    """
    logging.info("Notifying the owner of %s website" % address)
    time.sleep(0.5)
     
 
#Creo la funzione "manage_homepage" e gli passo address
def manage_homepage(address):
    """
    Carica l'home page del sito, crea un file, salva il contenuto, 
    ricarica il contenuto dal file, conta le parole, chiude e rimuove il file
    """
    try:
        save_homepage(address)
    except WebsiteDownException:
        notify_owner(address)



#I siti:
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
    #Individuo il tempo iniziale
    start_time = time.time()
    #Inizio un ciclo for
    for address in WEBSITE_LIST:
        #4..
        #chiamo l'opportuna funzione alla quale passo l'indirizzo
        manage_homepage(address)
    #Individuo il tempo finale
    end_time = time.time()        
    #Visualizzo il tempo totale di esecuzione
    print("Tempo di esecuzione seriale : %ssecs" % (end_time - start_time))