from politician import Politician
import simplejson
from elastic_search import iniciation, create_index
from elasticsearch import Elasticsearch

def delete_index(index_name):
    """
    Deletes the specified Elasticsearch index.

    Parameters:
        index_name (str): The name of the Elasticsearch index.

    Returns:
        dict: The response from the delete operation.
    """
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
    response = es.indices.delete(index=index_name, ignore=[400, 404])
    return response

def delete_all_data(index_name):
    """
    Deletes all documents from the specified Elasticsearch index.

    Parameters:
        index_name (str): The name of the Elasticsearch index to delete documents from.

    Returns:
        None
    """
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
    es.delete_by_query(index=index_name, body={"query": {"match_all": {}}})

def get_document_count(index_name):
    """
    Retrieves the count of documents in the specified Elasticsearch index.

    Parameters:
        index_name (str): The name of the Elasticsearch index to count documents from.

    Returns:
        int: The number of documents in the index.
    """
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
    response = es.count(index=index_name, body={"query": {"match_all": {}}})
    return response['count']

def fetch_all_documents(index_name):
    """
    Fetches all documents from the specified Elasticsearch index.

    Parameters:
        index_name (str): The name of the Elasticsearch index to fetch documents from.

    Returns:
        list: A list of documents from the index.
    """
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
    response = es.search(index=index_name, body={"query": {"match_all": {}}}, size=10000)
    documents = response['hits']['hits']
    return documents

politicians_2024 = [
    {
      "name": "Joe Biden",
      "party": "Democratic Party",
    },
    {
      "name": "Donald Trump",
      "party": "Republican Party",
    },
    {
      "name": "Kamala Harris",
      "party": "Democratic Party",
    },
    {
      "name": "Nancy Pelosi",
      "party": "Democratic Party",
    },
    {
      "name": "Kevin McCarthy",
      "party": "Republican Party",
    },
    {
      "name": "Chuck Schumer",
      "party": "Democratic Party",
    },
    {
      "name": "Mitch McConnell",
      "party": "Republican Party",
    },
    {
      "name": "Alexandria Ocasio-Cortez",
      "party": "Democratic Party",
    },
    {
      "name": "Ted Cruz",
      "party": "Republican Party",
    }
]

print("Empezando el main--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

iniciation.check_elasticsearch()
create_index.create_index()

# List to store the politicians.
# politician_instances = []

# for politician_info in politicians_2024:
#     new_politician = Politician(name=politician_info["name"], party=politician_info["party"])
#     politician_instances.append(new_politician)

# for politician in politician_instances:
#     politician.retrieve_info()


# # Delete all data in the "posts_index"
# delete_all_data("posts_index")

# # Delete all data in the "last_retrieved_post"
# delete_all_data("last_retrieved_post")

# Delete an index
# create_index.delete_index("posts_index")

# Trump = Politician(name="Donald Trump", party="Republican")
# Trump.retrieve_info()


# Get the count of documents in the "posts_index"
posts_index_count = get_document_count("posts_index")
print(f"Number of documents in posts_index: {posts_index_count}")

# Get the count of documents in the "last_retrieved_post" index
last_retrieved_post_count = get_document_count("last_retrieved_post")
print(f"Number of documents in last_retrieved_post: {last_retrieved_post_count}")

# # Fetch and print all documents from the "posts_index"
# posts_index_documents = fetch_all_documents("posts_index")
# print("Documents in posts_index:")
# for doc in posts_index_documents:
#     print(doc['_source'])

# # Fetch and print all documents from the "last_retrieved_post" index
# last_retrieved_post_documents = fetch_all_documents("last_retrieved_post")
# print("Documents in last_retrieved_post:")
# for doc in last_retrieved_post_documents:
#     print(doc['_source'])



