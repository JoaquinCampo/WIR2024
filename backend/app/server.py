from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
import simplejson
from datetime import datetime, timedelta

app = FastAPI()


origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

sample = {
    "cant_comments": 3,
    "date": "20240613",
    "id": "1df6tue",
    "name": "t3_1df6tue",
    "related_entity": "Trump",
    "score": 0.8776760101318359,
    "sentiment": "Negative",
    "text": "No text available",
    "thumbsup": 5,
    "title": "This Top Democrat Isn\u2019t Afraid to Call Trump a Felon and a Grifter. Most of the party\u2019s leaders want to avoid too much focus on Donald Trump\u2019s felonies. JB Pritzker, the governor of Illinois, feels differently."  
}

@app.get("/")
def homePage():
    welcome = {
        "Title": "Welcome to Reputation Analyzer"
    }

    return welcome

def get_score(data):
    sentiment_values = {'Negative': 0, 'Neutral': 0.5, 'Positive': 1}

    for item in data:
        item['label_value'] = sentiment_values[item['sentiment']]

    weighted_sum = sum(item['label_value'] * item['score'] for item in data)
    total_weight = sum(item['score'] for item in data)
    if total_weight != 0:
        weighted_average = weighted_sum / total_weight
    else:
        return 0

    return weighted_average

def group_by_date(results, days=31):
    grouped_results = {i: [] for i in range(days)}

    today = datetime.now().date()

    for result in results:
        result_date = datetime.strptime(result['date'], '%Y%m%d').date()
        
        day_difference = (today - result_date).days

        if 0 <= day_difference < days:
            grouped_results[day_difference].append(result)

    grouped_array = [grouped_results[i] for i in range(days)]

    return grouped_array


def get_statistics(Politician):
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

    index_name = "posts_index"

    query = {
        "query": {
            "match": {
                "related_entity": Politician
            }
        }
    }
    
    response = es.search(index=index_name, body=query)
    hits = response['hits']['hits']
    results = [hit['_source'] for hit in hits]

    grouped_data = group_by_date(results)

    today = datetime.now().date()
    res = []

    total = 0
    for item in grouped_data:
        total += get_score(item)
    avarage = total / 31

    for i in range(31):
        day = today - timedelta(days=i)
        if grouped_data[i]:
            reputation_score = get_score(grouped_data[i])
            res.append({"Date": day.strftime('%Y%m%d'), "Reputation": reputation_score})
        else:
            res.append({"Date": day.strftime('%Y%m%d'), "Reputation": avarage})
            
    return res


def three_posts(Politician):
    es = Elasticsearch([{"host": "localhost", "port": 9200, "scheme": "http"}])

    index_name = "posts_index"

    query = {
        "query": {
            "match": {
                "related_entity": Politician
            }
        }
    }

    response = es.search(index=index_name, body=query)
    hits = response['hits']['hits']
    results = [hit['_source'] for hit in hits]


    minn = 0
    neutral = 0
    maxx = 0

    post_min = None
    post_neutral = None
    post_max = None


    for item in results:
        if item['sentiment'] == 'Negative' and item['score'] > minn:
            post_min = item
        if item['sentiment'] == 'Positive' and item['score'] > maxx:
            post_max = item
        if item['sentiment'] == 'Neutral' and item['score'] > neutral:
            post_min = item
    return post_min, post_neutral, post_max
        

@app.get("/politician/{name}")
def read_politician_stats(name: str):
    statistics, average_score = get_statistics(name)

    post_min, post_neutral, post_max = three_posts(name)

    res = {
        "Politician": "{name}",
        "stats": get_statistics(name),
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max
    }

    return res