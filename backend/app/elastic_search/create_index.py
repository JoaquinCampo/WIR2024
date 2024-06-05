from elasticsearch import Elasticsearch

def create_index():
    elasticsearch_connection = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

    # Check if the connection is successful
    if not elasticsearch_connection.ping():
        raise ValueError("Connection failed")
    else:
        print("Connection successful")

    index_name = "posts_index"
    

    mapping = {
        "mappings": {
            "properties": {
                "related_entity": {"type": "text"},
                "id": {"type": "keyword"},
                "name": {"type": "text"},
                "title": {"type": "text"},
                "text": {"type": "text"},
                "date": {"type": "date", "format": "yyyyMMdd"},
                "cant_comments": {"type": "integer"},
                "thumbsup": {"type": "integer"},
                "sentiment": {"type": "text"},
                "score":{"type": "integer"}
            }
        }
    }

    if not elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.create(index=index_name, body=mapping)
        print(f"Índice {index_name} creado correctamente.")
    else:
        print(f"El índice {index_name} ya existe.")


    index_name = "last_retrieved_post"

    mapping = {
        "mappings": {
            "properties": {
                "related_entity": {"type": "text"},
                "post_id": {"type": "keyword"}
            }
        }
    }

    if not elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.create(index=index_name, body=mapping)
        print(f"Índice {index_name} creado correctamente.")
    else:
        print(f"El índice {index_name} ya existe.")