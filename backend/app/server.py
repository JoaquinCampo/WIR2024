from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from elasticsearch import Elasticsearch
import simplejson
from datetime import datetime, timedelta
import json
import numpy as np
import random
import redditAPI
import huggingface

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
    "subreddit": "r/politics",
    "cant_comments": 3,
    "date": "20240613",
    "id": "1df6tue",
    "name": "t3_1df6tue",
    "related_entity": "Trump",
    "score": 0.8776760101318359,
    "sentiment": "Negative",
    "text": "No text available",
    "thumbsup": 5,
    "title": "This Top Democrat Isn\u2019t Afraid to Call Trump a Felon and a Grifter. Most of the party\u2019s leaders want to avoid too much focus on Donald Trump\u2019s felonies. JB Pritzker, the governor of Illinois, feels differently.",
    "Donald Trump": 0.88,
    "Kevin McCarthy": 0.75,
    "Mitch McConnell": 0.64,
    "Ted Cruz": 0.53,
    "Joe Biden": 0.42,
    "Kamala Harris": 0.31,
    "Nancy Pelosi": 0.25,
    "Chuck Schumer": 0.17,
    "Alexandria Ocasio-Cortez": 0.02,
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

def group_by_date(results, days=8):
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
        },
        "size": 10000
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
    avarage = total / 8

    for i in range(8):
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
        },
        "size": 10000
    }

    response = es.search(index=index_name, body=query)
    # print(simplejson.dumps(response.json(), indent=4, sort_keys=True))
    hits = response['hits']['hits']
    results = [hit['_source'] for hit in hits]

    post_min = post_neutral = post_max = None
    min_score = neutral_score = max_score = float('-inf')

    for item in results:
        if item['sentiment'] == 'Negative' and (post_min is None or item['score'] > min_score):
            post_min = item
            min_score = item['score']
        elif item['sentiment'] == 'Neutral' and (post_neutral is None or item['score'] > neutral_score):
            post_neutral = item
            neutral_score = item['score']
        elif item['sentiment'] == 'Positive' and (post_max is None or item['score'] > max_score):
            post_max = item
            max_score = item['score']

    return post_min, post_neutral, post_max


def smooth_data(data):
    average_reputation = np.mean([entry["Reputation"] for entry in data])

    for entry in data:
        noise = random.uniform(-0.25 * average_reputation, 0.25 * average_reputation) 
        
        if entry["Reputation"] + noise > 0:
            entry["Reputation"] = entry["Reputation"] + noise
        else:
            entry["Reputation"] = entry["Reputation"] - noise

    return data

@app.get("/politician/{name}")
def read_politician_stats(name: str):
    post_min, post_neutral, post_max = three_posts(name)

    res = {
        "Politician": name,
        "stats": smooth_data(get_statistics(name)),
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max
    }

    return res
 
@app.get("/politician_NOW/{name}")
def get_politician_stats(name: str):

    unscored_data = redditAPI.get_politician_data_amount(name, 500)

    data = huggingface.analyse_sentiment(name, unscored_data)


    grouped_data = group_by_date(data)

    today = datetime.now().date()
    res = []

    total = 0
    for item in grouped_data:
        total += get_score(item)
    avarage = total / 8

    for i in range(8):
        day = today - timedelta(days=i)
        if grouped_data[i]:
            reputation_score = get_score(grouped_data[i])
            res.append({"Date": day.strftime('%Y%m%d'), "Reputation": reputation_score})
        else:
            res.append({"Date": day.strftime('%Y%m%d'), "Reputation": avarage})

    post_min = post_neutral = post_max = None
    min_score = neutral_score = max_score = float('-inf')

    for item in data:
        if item['sentiment'] == 'Negative' and (post_min is None or item['score'] > min_score):
            post_min = item
            min_score = item['score']
        elif item['sentiment'] == 'Neutral' and (post_neutral is None or item['score'] > neutral_score):
            post_neutral = item
            neutral_score = item['score']
        elif item['sentiment'] == 'Positive' and (post_max is None or item['score'] > max_score):
            post_max = item
            max_score = item['score']

    ret = {
        "Politician": name,
        "stats": smooth_data(res),
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max
    }

    return ret

