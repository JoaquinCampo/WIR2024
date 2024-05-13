import requests as rq
import simplejson
import datetime

def login():
    global TOKEN

    CLIENT_ID = '35RqOQuPf7sH7XMxtMJ_Og'
    CLIENT_SECRET = 'BzGAvv9krxswP6K80H5ZW0wyrIGobQ'

    auth = rq.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)

    data = {
        'grant_type': 'password',
        'username': 'jomavacadadu',
        'password': 'F@TeK2rBuW*xhdT'
    }

    headers = {'User-Agent': 'MyAPI/0.0.1'}

    res = rq.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    TOKEN = res.json()['access_token']

def buscarPublicaciones(entidad, largo):
    # if(type(entidad) not String or largo not Int):  ### hay que chequear caso borde por entrada de mal tipo de variable

    headers = {'User-Agent': 'MyAPI/0.0.1'}
    headers['Authorization'] = f'bearer {TOKEN}'

    url = 'https://oauth.reddit.com/r/politics/search'

    params = {
        'q': entidad,        # Término de búsqueda
        'sort': 'new',       # Ordenar por relevancia
        'limit': largo       # Limitar a los primeros 10 resultados
    }

    redUY = rq.get(url, headers=headers, params = params)
    redUYjson = redUY.json()

    for post in redUYjson['data']['children']:
        print(f"Titulo: {post['data']['title']}")

        print(f"Publicación: {post['data']['selftext']}")
        
        fecha = datetime.datetime.fromtimestamp(post['data']['created_utc']).strftime('%d-%m-%Y %H:%M')
        print(f"Hora de publicación: {fecha}")

        print(f"Subreddit: {post['data']['subreddit']}")
        print("-" * 80)

    # json = simplejson.dumps(redUY.json(), indent=4, sort_keys=True)  ## para formatear el json en la consola y que se entienda mas

global logged
logged = False
login()
logged = True


buscarPublicaciones("Trump", 3)