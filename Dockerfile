FROM python:3.8.0-slim-buster
COPY . usr/src/app
WORKDIR /usr/src/app

RUN apt-get update 
# && apt-get install chromium-chromedriver
RUN cp /usr/lib/chromium-browser/chromedriver /usr/bin

RUN pip install -r requirements.txt

#ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload
ENTRYPOINT uvicorn --host 0.0.0.0 main:app --port 8080 --reload

#docker build -t gcr.io/d-languages-1/python-app .