from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

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

@app.get("/politician")
def read_items():
    return sample
