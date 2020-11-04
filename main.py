from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver

import browser
import functions

app = FastAPI()
app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_credentials=True,allow_methods=["*"], allow_headers=["*"])

@app.get("/")
def read_root():
    return {"Scrapper": "Bienvenido al scraper, no hay documentación"}

@app.get("/word/{word}")
def get_word(word):
    print("Buscando la palabra", word)
    word_api = browser.get_word_from_api(word)
    word_dict = browser.extract_data_from_word(word_api)
    print(word_dict)
    translations = browser.scrap_transalation(word)
    diccionario = {**word_dict, **translations}
    return diccionario

@app.get("/translate/{palabra}")
def translate(palabra):
 return functions.buscar(palabra)






