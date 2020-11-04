from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from selenium import webdriver

#import functions

app = FastAPI()

app.add_middleware( CORSMiddleware, allow_origins=["*"],
    allow_credentials=True,allow_methods=["*"], allow_headers=["*"]
)


@app.get("/")
def read_root():
    return {"Scrapper": "Bievenido al scraper, no hay documentación"}




options = webdriver.ChromeOptions()
options.add_argument('--headless')
# options.add_argument('window-size=1200x600')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(chrome_options=options)
#If the chromedriver is not set in the PATH environment variable, specify the chromedriver location with the executable_path option.
#browser = webdriver.Chrome(chrome_options=options, executable_path="/usr/local/bin/chromedriver")

url = "http://google.com"

browser.get(url)
browser.save_screenshot("Website.png")
browser.quit()





