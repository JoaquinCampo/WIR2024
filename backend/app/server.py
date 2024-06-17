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

    post_min = results[0]
    post_neutral = results[0]
    post_max = results[0]

    pasar = True 
    for item in results:
        if pasar:
            pasar = False
            pass
        if item['sentiment'] == 'Negative' and item['score'] > minn:
            post_min = item
        if item['sentiment'] == 'Positive' and item['score'] > maxx:
            post_max = item
        if item['sentiment'] == 'Neutral' and item['score'] > neutral:
            post_min = item
    return post_min, post_neutral, post_max
        

@app.get("/politician/{name}")
def read_politician_stats(name: str):

    temp = {
    "Politician": "Donald Trump",
    "stats": [
        {
        "Date": "20240616",
        "Reputation": 0
        },
        {
        "Date": "20240615",
        "Reputation": 0
        },
        {
        "Date": "20240614",
        "Reputation": 0.147033890912773
        },
        {
        "Date": "20240613",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240612",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240611",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240610",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240609",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240608",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240607",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240606",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240605",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240604",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240603",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240602",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240601",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240531",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240530",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240529",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240528",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240527",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240526",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240525",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240524",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240523",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240522",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240521",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240520",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240519",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240518",
        "Reputation": 0.00474302873912172
        },
        {
        "Date": "20240517",
        "Reputation": 0.00474302873912172
        }
    ],
    "min": {
        "related_entity": "Donald Trump",
        "id": "1dfrgh2",
        "name": "t3_1dfrgh2",
        "title": "Happy Seventy-eighth Birthday, Mr. Ex-President: If ever there were a case for age-related diminishment of a candidate, Donald Trump is it.",
        "text": "No text available",
        "date": "20240614",
        "cant_comments": 68,
        "thumbsup": 635,
        "link": "reddit.com/r/politics/comments/1dfrgh2/happy_seventyeighth_birthday_mr_expresident_if/",
        "subreddit": "r/politics",
        "sentiment": "Negative",
        "score": 0.625670731067658
    },
    "neutral": {
        "related_entity": "Donald Trump",
        "id": "1dhbwdg",
        "name": "t3_1dhbwdg",
        "title": "Rep. Byron Donalds Wants Supreme Court to ‘Step in’ and Overturn Trump Conviction",
        "text": "No text available",
        "date": "20240616",
        "cant_comments": 113,
        "thumbsup": 153,
        "link": "reddit.com/r/politics/comments/1dhbwdg/rep_byron_donalds_wants_supreme_court_to_step_in/",
        "subreddit": "r/politics",
        "sentiment": "Negative",
        "score": 0.634963810443878
    },
    "max": {
        "related_entity": "Donald Trump",
        "id": "1dhbwdg",
        "name": "t3_1dhbwdg",
        "title": "Rep. Byron Donalds Wants Supreme Court to ‘Step in’ and Overturn Trump Conviction",
        "text": "No text available",
        "date": "20240616",
        "cant_comments": 113,
        "thumbsup": 153,
        "link": "reddit.com/r/politics/comments/1dhbwdg/rep_byron_donalds_wants_supreme_court_to_step_in/",
        "subreddit": "r/politics",
        "sentiment": "Negative",
        "score": 0.634963810443878
    }
    }

    return temp

    statistics = get_statistics(name)

    post_min, post_neutral, post_max = three_posts(name)

    res = {
        "Politician": name,
        "stats": get_statistics(name),
        "min": post_min,
        "neutral": post_neutral,
        "max": post_max
    }

    return res