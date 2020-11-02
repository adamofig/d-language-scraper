FROM python:3.8.6-buster
COPY . usr/src/app
WORKDIR /usr/src/app

#install chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# RUN cp /usr/lib/chromium-browser/chromedriver /usr/bin

RUN pip install -r requirements.txt

#ENTRYPOINT uvicorn --host 0.0.0.0 main:app --reload
ENTRYPOINT uvicorn --host 0.0.0.0 main:app --port 8080 --reload

#docker build -t gcr.io/d-languages-1/python-app .