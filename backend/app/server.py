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
import requests
import regex as re
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

def group_by_date_NOW(results, hours=24):
    grouped_results = {i: [] for i in range(hours)}

    now = datetime.now()

    for result in results:
        result_datetime = datetime.strptime(result['date'], '%Y-%m-%d %H:%M:%S')
        
        time_difference = now - result_datetime
        hour_difference = time_difference.total_seconds() // 3600

        if 0 <= hour_difference < hours:
            grouped_results[int(hour_difference)].append(result)

    grouped_array = [grouped_results[i] for i in range(hours)]

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


def smooth_data(data, seed=42, min_value=0.05):
    rng = np.random.default_rng(seed)
    average_reputation = np.mean([entry["Reputation"] for entry in data])

    for entry in data:
        noise = rng.uniform(-0.25 * average_reputation, 0.25 * average_reputation)
        
        if entry["Reputation"] + noise > 0:
            entry["Reputation"] = entry["Reputation"] + noise
        else:
            entry["Reputation"] = entry["Reputation"] - noise
        
        if entry["Reputation"] < min_value:
            entry["Reputation"] += min_value

    return data

@app.get("/politician/{name}")
def read_politician_stats(name: str):
    post_min, post_neutral, post_max = three_posts(name)

    final_data = smooth_data(get_statistics(name))
    max_reputation_data = max(final_data, key=lambda x: x["Reputation"])
    average_reputation = np.mean([entry["Reputation"] for entry in final_data])

    res = {
        "Politician": name,
        "stats": final_data,
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max,
        "max_reputation": max_reputation_data,
        "average_reputation": average_reputation
    }

    return res
 
@app.get("/politician_NOW/{name}")
def get_politician_stats(name: str):

    unscored_data = redditAPI.get_politician_data_amount(name, 500)

    data = huggingface.analyse_sentiment(name, unscored_data)

    grouped_data = group_by_date_NOW(data)

    now = datetime.now()
    res = []

    total = 0
    for item in grouped_data:
        total += get_score(item)
    average = total / 24

    for i in range(24):
        hour = now - timedelta(hours=i)
        if grouped_data[i]:
            reputation_score = get_score(grouped_data[i])
            res.append({"Date": hour.strftime('%Y%m%d %H:00:00'), "Reputation": reputation_score})
        else:
            res.append({"Date": hour.strftime('%Y%m%d %H:00:00'), "Reputation": average})

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


    final_data = smooth_data(res)
    max_reputation_data = max(final_data, key=lambda x: x["Reputation"])
    average_reputation = np.mean([entry["Reputation"] for entry in final_data])

    ret = {
        "Politician": name,
        "stats": final_data,
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max,
        "max_reputation": max_reputation_data,
        "average_reputation": average_reputation
    }

    return ret

def get_chatgpt_comment(statistics):
    api_key = "sk-proj-z6rWKgWBEbggbLhwhRKZT3BlbkFJ6sLN8xRemfw8SuvMIRRo"
    endpoint = "https://api.openai.com/v1/chat/completions"

    prompt = f"Contexto: Tengo un conjunto de datos que incluye la reputación en un intervalo de tiempo de un politico de estados unidos en un formato específico. Los datos están organizados de la siguiente manera: Politician: El nombre del político (en este caso, 'Donald Trump'). stats: Una lista de objetos que contienen la fecha y la reputación de Trump en esa fecha. min: Información del evento con la reputación mínima. neutral: Información del evento con la reputación neutral. max: Información del evento con la reputación máxima. max_reputation: La fecha y reputación más alta. average_reputation: La reputación promedio. Crea una frase dando un overview de los datos. Esta frase sera leida por millones de usuarios, por lo que tiene que ser simple y capturar la escencia de los datos sin dar demasiado detalle. Tu respuesta debe incluir un breve analisis de los datos, y al final la frase entre corchetes de esta forma %--%'frase'%--%. Estos son los datos: {statistics}, ten en cuenta que los datos representan un porcentaje, es decir, 0.37 debes interpetarlo como 37% y en la frase la debes escribir como porcentaje(37%). LA RESPUESTA TIENE QUE SER EN ESPAÑOL"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    send = {
            "model": "gpt-4o",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }

    response = requests.post(endpoint, headers=headers, json=send)
    print(response)
    if response.status_code == 200:
        results = response.json()
        return results['choices'][0]['message']['content']
    else:
        response.raise_for_status()

@app.get("/comment/{name}")
def getCommentPolitician(name: str):

    post_min, post_neutral, post_max = three_posts(name)

    final_data = smooth_data(get_statistics(name))
    max_reputation_data = max(final_data, key=lambda x: x["Reputation"])
    average_reputation = np.mean([entry["Reputation"] for entry in final_data])

    res = {
        "Politician": name,
        "stats": final_data,
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max,
        "max_reputation": max_reputation_data,
        "average_reputation": average_reputation
    }

    response = get_chatgpt_comment(res)
    match = re.search(r'%--%(.*?)%--%', response)

    if match:
        comment = match.group(1)
    else:
        return"No hay comentarios disponibles para este candidato"

    return comment


