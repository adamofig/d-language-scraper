from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import functions

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=["*"],
    allow_credentials=True,allow_methods=["*"], allow_headers=["*"],
)

import dryscrape
#from bs4 import BeautifulSoup

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
@app.get("/translate/{palabra}")
def translate(palabra):
 return functions.buscar(palabra)





