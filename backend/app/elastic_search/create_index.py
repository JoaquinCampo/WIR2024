from elasticsearch import Elasticsearch

def create_index():
    elasticsearch_connection = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

    # Check if the connection is successful
    if not elasticsearch_connection.ping():
        raise ValueError("Connection failed")
    else:
        print("Connection successful")

    # Create the posts_index
    index_name = "posts_index"

    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "index.translog.durability": "async"
        },
        "mappings": {
            "properties": {
                "related_entity": {"type": "text"},
                "id": {"type": "keyword"},
                "name": {"type": "text"},
                "title": {"type": "text"},
                "text": {"type": "text"},
                "date": {"type": "date", "format": "yyyyMMdd"},
                "thumbsup": {"type": "integer"},
                "link": {"type": "text"},
                "subreddit": {"type": "text"},
                "sentiment": {"type": "text"},
                "score": {"type": "integer"},
                "comment": {"type": "text"}
            }
        }
    }

    if not elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.create(index=index_name, body=settings)
        print(f"Index {index_name} created successfully.")
    else:
        print(f"The index {index_name} already exists.")

    # Create the last_retrieved_post index
    index_name = "last_retrieved_post"

    settings = {
        "settings": {
            "number_of_shards": 1,
            "number_of_replicas": 0,
            "refresh_interval": "30s",
            "index.translog.durability": "async"
        },
        "mappings": {
            "properties": {
                "related_entity": {"type": "text"},
                "post_id": {"type": "keyword"}
            }
        }
    }

    if not elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.create(index=index_name, body=settings)
        print(f"Index {index_name} created successfully.")
    else:
        print(f"The index {index_name} already exists.")

def delete_index(index_name):
    elasticsearch_connection = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

    # Check if the connection is successful
    if not elasticsearch_connection.ping():
        raise ValueError("Connection failed")
    else:
        print("Connection successful")

    # Delete the index if it exists
    if elasticsearch_connection.indices.exists(index=index_name):
        elasticsearch_connection.indices.delete(index=index_name)
        print(f"Index {index_name} deleted successfully.")
    else:
        print(f"The index {index_name} does not exist.")
