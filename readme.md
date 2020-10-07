### Construir docker 


    docker build -t d-scraper .

Iniciando el contenedor

    docker run -it -p 8000:8080 -v %cd%:/usr/src/app --name scrap d-scraper

Prendiendo y apagando ambiente 

    docker start -a scrap
