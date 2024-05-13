from elasticsearch import Elasticsearch


def create_index():
    elasticsearch_connection = Elasticsearch([{"host": "localhost", "port": 9200}])

    # Check if the connection is successful
    if not elasticsearch_connection.ping():
        raise ValueError("Connection failed")
    else:
        print("Connection successful")

    index_name = "my_index"

    mapping = {
        "mappings": {
            "properties": {
                "field1": {"type": "text"},
                "field2": {"type": "text"},
                "field3": {"type": "text"},
            }
        }
    }

    if not elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.create(index=index_name, body=mapping)
        print(f"Índice {index_name} creado correctamente.")
    else:
        print(f"El índice {index_name} ya existe.")
