import redditAPI
import huggingface
import simplejson
from elasticsearch import Elasticsearch

class Politician:
    """
    Represents a politician with their name, party, opinions, and other information.

    Attributes:
        name (str): The full name of the politician.
        party (str): The political party the politician belongs to.
        first_name (str): The first name of the politician.
        last_name (str): The last name of the politician.
        opinions (list): A list of opinions expressed by the politician.
        after (str): A token used for pagination when retrieving politician data.

    Methods:
        split_name(name): Splits the full name into first and last name.
        display_info(): Returns a string with the politician's information.
        retrieve_info(): Retrieves and analyzes politician data from Reddit and Hugging Face.
    """

    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.first_name, self.last_name = self.split_name(name)
        self.opinions = []
        self.after = None

    def split_name(self, name):
        """
        Splits the full name into first and last name. Assumes the last token as the last name,
        and the rest as the first name.

        Parameters:
           name (str): The full name of the politician.

        Returns:
           tuple: first name, last name
        """
        parts = name.split()
        if len(parts) > 1:
            return (' '.join(parts[:-1]), parts[-1])
        else:
            return (name, "")

    def display_info(self):
        """
        Returns a string with the politician's information.

        Returns:
            str: The politician's information.
        """
        return f"Name: {self.name}, First Name: {self.first_name}, Last Name: {self.last_name}, Party: {self.party}"
    
    def retrieve_info(self):
        """
        Retrieves and analyzes politician data from Reddit and Hugging Face.
        Updates the opinions list with the analyzed posts.

        Returns:
            None
        """
        posts, self.after = redditAPI.get_politician_data(self.name, self.after)
        self.update_last_post(self.after)
        
        print(f" la cantidad de posts es: {len(posts)}")

        scored_posts = huggingface.analyse_sentiment(self.name, posts)
        
        for post in scored_posts:
            self.opinions.append(post)

        self.store_opinions()
    
    def store_opinions(self):
        """
        Stores the opinions in Elasticsearch.

        Returns:
            None
        """
        es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
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
                    "thumbsup": {"type": "integer"},
                    "link": {"type": "text"},
                    "subreddit": {"type": "text"},
                    "sentiment": {"type": "text"},
                    "score": {"type": "integer"},
                    "comment": {"type": "text"}
                }
            }
        }

        for opinion in self.opinions:
            try:
                res = es.index(index=index_name, body=opinion)
            except Exception as e:
                print(f"Error indexing document: {e}")

    def update_last_post(self, post_id):
        """
        Updates the last retrieved post ID in Elasticsearch.

        Parameters:
            post_id (str): The ID of the last retrieved post.

        Returns:
            None
        """
        
        es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])
        index_name = "last_retrieved_post"
        related_entity_value = self.last_name
        
        doc = {
            "related_entity": related_entity_value,
            "post_id": post_id
        }

        query = {
            "query": {
                "match": {
                    "related_entity": related_entity_value
                }
            }
        }

        res = es.search(index=index_name, body=query)

        if res['hits']['total']['value'] > 0:
            doc_id = res['hits']['hits'][0]['_id']
            es.update(index=index_name, id=doc_id, body={"doc": doc})
        else:
            es.index(index=index_name, body=doc)
