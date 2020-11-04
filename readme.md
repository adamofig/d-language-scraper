### Construir docker 


    docker build -t d-scraper .

Iniciando el contenedor

    docker run -it -p 8000:8080 -v %cd%:/usr/src/app --name scrap d-scraper

Prendiendo y apagando ambiente 

    docker start -a scrap


### Despliegue 



gcloud builds submit --tag gcr.io/d-languages-1/scraper


gcloud run deploy --image gcr.io/d-languages-1/scraper --platform managed


### Para no volver a configurar clour run 
gcloud config set run/region us-central1