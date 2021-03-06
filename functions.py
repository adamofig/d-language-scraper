from selenium import webdriver
from bs4 import BeautifulSoup

def init_driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # options.add_argument('window-size=1200x600')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    browser = webdriver.Chrome(chrome_options=options)
    return browser


def cambia_sopa(palabra): #palabra en ingl
  wd = init_driver()
  url = "https://translate.google.com.mx/?hl=es#view=home&op=translate&sl=en&tl=es&text="+palabra 
  wd.get(url)
  soup = BeautifulSoup(wd.page_source,'html.parser')
  wd.quit()
  return soup 

# Recibe un objeto de tipo bs4.element.ResultSet
def get_translation_synonyms_right(nodes): #recibe una lista de cosas asi <span class="gt-baf-back">increase</span....<3  # TODO ! Ponerle nombre de la clase de lista
  synomyns = []
  for element in nodes:
   word = element.get_text()
   synomyns.append(word)
  return synomyns

#cambia a numeros la frecuencia
def frecuencyy(nodo):
  if nodo=="Traducción común":
   return 5
  elif nodo=="Traducción poco común":
   return 3
  elif nodo=="Traducción rara":
   return 1
  else:
    print("algo raro pasa en frecuencia")

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


def examples(nodo):
    list_examples=[]
    for ejem in nodo:
      nodo=ejem.get_text()
      list_examples.append(nodo)
    return list_examples



#@app.get("/translate/{palabra}")
def buscar(palabra):
  dici={}
  soup=cambia_sopa(palabra)
  try:
    spanishTranslation = soup.find('div',attrs={'class':'result-shield-container tlid-copy-target'}).find('span').get_text()
  except:
    mensaje= soup.find('div',attrs={'id':'spelling-correction'})
    print("no se pudo encontrar la palabra")
    print(mensaje)
  dici['spanishTranslation'] = spanishTranslation
  word = soup.find('div',attrs={'class':'text-dummy'}).get_text()
  dici['word'] = word
  other_trans_nodes = soup.find_all('span',attrs={'class':'gt-baf-cell gt-baf-word-clickable'})
  other_translations = get_transalation_optionals(other_trans_nodes)
  dici['otherTranslations'] = other_translations
  try: 
    synonyms_nodes = soup.find('div',attrs={'class':'gt-baf-cell gt-baf-translations gt-baf-translations-mobile'}).find_all('span')
    synonyms = get_translation_synonyms_right(synonyms_nodes)
    dici['synonyms']=synonyms
  except:
    print("no se pudo obtener sinonimos")
    dici['synonyms']=None
  try:
    frecuency = soup.find('div',attrs={'class':'gt-baf-cell gt-baf-entry-score'}).get('title')
    num_frecuency=frecuencyy(frecuency)
    dici['useFrecuency'] = num_frecuency
  except:
    print("no se encuentra frecuencia")
    dici['useFrecuency']=None
  nodes = soup.find("div", attrs={'class' : 'gt-cd gt-cd-mmd'}).find("div", attrs= {'class': 'gt-cd-c'})
  definitions=final_definitions(nodes)
  dici['definitions'] = definitions
  nodo=soup.find_all('div',attrs={'class':'gt-ex-text'})
  example=examples(nodo)
  dici['example'] = example
  return dici
