# WIR2024

Deben instalar docker en su pc -> https://www.docker.com/products/docker-desktop/

Para levantar el servicio de docker
docker-compose up

Cada vez que se realice un cambio hay que ejecutar
docker-compose up --build


Agregar documento a elasticsearch
http://localhost:9200/my_index/_doc/nro_doc

Consultar mediante campos que usa indices invertidos
http://localhost:9200/my_index/_search
luego le tenes que mandar la query de la siguiente forma
{
  "query": {
    "multi_match": {
      "query": "data science",
      "fields": ["selftext"]
    }
  }
}