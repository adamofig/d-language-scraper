from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=["*"],
    allow_credentials=True,allow_methods=["*"], allow_headers=["*"],
)

import dryscrape
from bs4 import BeautifulSoup

dryscrape.start_xvfb()
"""
sess = dryscrape.Session()
url = "https://translate.google.com.mx/#view=home&op=translate&sl=en&tl=es&text=raise"
sess.visit(url)
source = sess.body()

soup = BeautifulSoup(source,'lxml')

print(soup)"""

@app.get("/")
def read_root():
    return {"Scrapper": "Bievenido al scraper, no hay documentación"}

#cambiar palabra
#la funcion que hace que se pueda hacer el parser de la url dada
def cambia_sopa(palabra): #palabra en ingl
  sess = dryscrape.Session()
  url = "https://translate.google.com.mx/#view=home&op=translate&sl=en&tl=es&text="+palabra

 # print(url)
  sess.visit(url)
  source = sess.body()
  soup = BeautifulSoup(source,'html.parser')
  return soup 

# Recibe un objeto de tipo bs4.element.ResultSet
def get_translation_synonyms_right(nodes): #recibe una lista de cosas asi <span class="gt-baf-back">increase</span....<3  # TODO ! Ponerle nombre de la clase de lista
  synomyns = []
  for element in nodes:
   word = element.get_text()
   synomyns.append(word)
  return synomyns

def get_transalation_optionals(nodes):
  other_translations=[]
  i=0
  for element in nodes:
    i=i+1
    if i==10:
      break
    else:
      other_translations.append(element.get_text())
  return other_translations

def get_definitions(nodes,word_type):
  definitions = []
  for element in nodes:
      definition = {}
      meaning = element.find('div', attrs={'class':'gt-def-row'}).get_text()
      number = element.find('span',attrs={'class':'gt-def-num'}).text
      try:
        example = element.find('div',attrs={'class':'gt-def-example'}).text
      except:
        example=None

      definition['number']=number
      definition['example']=example
      definition['meaning']=meaning
      definition['wordType']=word_type
      definitions.append(definition)

  return definitions

def final_definitions(nodes):
 index = 0
 last_type = ""
 final = []
 for element in nodes:
  #print(i , len(nodes))
  if index % 2 == 0:
    #print("par")
    last_type = element.get_text()
  else:
    #print("impar", type(element))
    #print(last_type)
     definitions = get_definitions(element, last_type)
    #print(definitions)
     final += definitions

  index += 1
 return final



@app.get("/translate/{palabra}")
def buscar(palabra):
  dici={}
  soup=cambia_sopa(palabra)
  spanishTranslation = soup.find('div',attrs={'class':'result-shield-container tlid-copy-target'}).find('span').get_text()
  dici['spanishTranslation'] = spanishTranslation
  word = soup.find('div',attrs={'class':'text-dummy'}).get_text()
  dici['word'] = word
  other_trans_nodes = soup.find_all('span',attrs={'class':'gt-baf-cell gt-baf-word-clickable'})
  other_translations = get_transalation_optionals(other_trans_nodes)
  dici['otherTranslations'] = other_translations
  synonyms_nodes = soup.find('div',attrs={'class':'gt-baf-cell gt-baf-translations gt-baf-translations-mobile'}).find_all('span')
  synonyms = get_translation_synonyms_right(synonyms_nodes)
  dici['synonyms']=synonyms
  frecuency = soup.find('div',attrs={'class':'gt-baf-cell gt-baf-entry-score'}).get('title')
  dici['usefrecuency'] = frecuency
  nodes = soup.find("div", attrs={'class' : 'gt-cd gt-cd-mmd'}).find("div", attrs= {'class': 'gt-cd-c'})
  definitions=final_definitions(nodes)
  dici['definitions'] = definitions
  #return dici
  return dici



