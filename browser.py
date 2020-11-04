from selenium import webdriver
from bs4 import BeautifulSoup
import requests

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(chrome_options=options)
    return browser

# ---- Funciones utiles para el scrap y bus
def cortar_lista(lista):
  if len(lista)<=5:
    return lista
  else:
    return lista[:5]

# wd = init_driver()

def unique(list1): 
    unique_list = []  
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list


def create_pipe_string(lista):
  cadena=""
  for x in lista:
    cadena=cadena+x+"|"
  cadena=cadena[:-1]
  return cadena

def cambia_sopa_scrap(palabra): #palabra en ingl
  wd = init_driver()
  url = "https://translate.google.com.mx/?hl=es#view=home&op=translate&sl=en&tl=es&text="+palabra 
  wd.get(url)
  soup = BeautifulSoup(wd.page_source,'html.parser')
  return soup 

#consigue otras traducciones y traduccion 
def scrap_transalation(palabra):   
    soup= cambia_sopa_scrap(palabra)
    # soup= cambia_sopa_scrap(palabra)  #truquillo manioso
    dicci={}
    lista_otros_verbos=[]
    try:
        textos=soup.find_all('span', attrs={'class' : 'tlid-translation translation'})
        translation=textos[1].text  #contando con que habra solo femenino,masculino y masculino sera el segundo 
    except:  #si no significa que no tiene genero 
        
        translation=soup.find("span", attrs={'class' : 'tlid-translation translation'}).text


          
    cadena_otros_verbos=""
    try:
        body=soup.find("tbody")  #cambia el body segun la sopa
        contador=0
        for td in body:
          try:
            tipo=td.find("span", attrs={'class' : 'gt-cd-pos'}).text
          except:
            pass
          if tipo=='sustantivo' or 'abjetivo' and contador<10:  #si es verbo que se guarde en una cadena,contador para que sean menos de 10
             try:
                otro_verbo=td.find("span", attrs={'class' : 'gt-baf-cell gt-baf-word-clickable'}).text
                #cadena_otros_verbos=cadena_otros_verbos+ otro_verbo +"|"
                lista_otros_verbos.append(otro_verbo)
                contador=contador+1
             except:
                cadena_otros_verbo=""
        #cadena_otros_verbos=cadena_otros_verbos[:-1] #quitamos el ultimo |
    except:
        print("no se encontro body")
    lista_otros_verbos=unique(lista_otros_verbos)
    cadena_otros_verbos=create_pipe_string(lista_otros_verbos)
    dicci['other_translation']=cadena_otros_verbos
    dicci['translation']=translation
    return dicci

def get_word_from_api(palabra): #palabra en ingl
  url = "https://api.dictionaryapi.dev/api/v2/entries/en/"+palabra
  economia = requests.get(url)
  lista = economia.json()# como ya es la api ya no es necesario hacer la sopa  
  return lista  # regresa una lista de diccionarios


### Necesita una grán refatorización, luego me encargaré de reahaccer el método
def extract_data_from_word(lista):
  dicci={}
  lista_definiciones=[]
  lista_ejemplos=[]
  lista_sinonimos=[]

  element = lista[0]
  try:
    dicci['word'] = element.get('word')
    fonetica=element.get('phonetics')[0]
    audio=fonetica['audio']
    phonetic=fonetica['text']
    dicci['phonetic']=phonetic
    dicci['audio']=audio
  except:
    pass

  try:
    meanings= element.get('meanings')
    for i in meanings:
        partOfSpeech = i.get('partOfSpeech')  #aqui primero encuentra noun y luego reasinga intransitive 
        if not 'verb' in partOfSpeech:
          dicci['partOfSpeech'] = partOfSpeech
          definitions = i.get('definitions')
          for diccionario in definitions:
            if 'definition' in diccionario:
                lista_definiciones.append(diccionario.get('definition'))
            if 'example' in diccionario:
                lista_ejemplos.append(diccionario.get('example'))
            if 'synonyms' in diccionario:
                sinonimos=diccionario.get('synonyms')# solo conseguir 5 de cada lista sinonimos
                lista_sinonimos=lista_sinonimos + cortar_lista(sinonimos)
  except:
    print("no se encontro meanings")

  #recordar las listas
  lista_definiciones = cortar_lista(unique(lista_definiciones))
  lista_ejemplos = cortar_lista(unique(lista_ejemplos))
  lista_sinonimos = unique(lista_sinonimos)
  try: #intentar recordar la lista hasta 15
    lista_sinonimos = lista_sinonimos[:15]
  except: #suponemos que la lista es mas pequenia
    pass
  dicci['definition'] = create_pipe_string(lista_definiciones)
  dicci['example'] = create_pipe_string(lista_ejemplos)
  dicci['synonyms'] = create_pipe_string(lista_sinonimos)
  return dicci