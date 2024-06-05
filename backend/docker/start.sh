#!/bin/bash
# Esperar a que Elasticsearch esté listo
python ./elastic_search/iniciation.py
python ./elastic_search/create_index.py

# Iniciar la aplicación Python
python main.py
