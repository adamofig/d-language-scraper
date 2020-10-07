from fastapi import FastAPI

app = FastAPI()

import dryscrape
from bs4 import BeautifulSoup

dryscrape.start_xvfb()

sess = dryscrape.Session()
url = "https://translate.google.com.mx/#view=home&op=translate&sl=en&tl=es&text=raise"
sess.visit(url)
source = sess.body()

soup = BeautifulSoup(source,'lxml')

print(soup)

@app.get("/")
def read_root():
    return {"Hello": "World22"}


