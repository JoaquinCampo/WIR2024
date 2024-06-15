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

@app.get("/politician")
def read_items():
    return sample
