import requests as rq
import simplejson
import datetime

def INIT():
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

def buscarPublicaciones(entidad, cantidad):
    # if(type(entidad) not String or largo not Int):  ### hay que chequear caso borde por entrada de mal tipo de variable
    global init

    if(not  init):     #para no enviar el auth todas las veces que se busca
       INIT()
       init = True

    headers = {'User-Agent': 'MyAPI/0.0.1'}
    headers['Authorization'] = f'bearer {TOKEN}'

    url = 'https://oauth.reddit.com/r/politics/search'

    params = {
        'q': entidad,           # Término de búsqueda
        'sort': 'new',          # Ordenar por fecha
        'limit': cantidad       # Limitar la cantidad de resultados
    }

    redUS = rq.get(url, headers=headers, params = params)
    redUSjson = redUS.json()

    for post in redUSjson['data']['children']:
        print(f"Titulo: {post['data']['title']}")

        print(f"Publicación: {post['data']['selftext']}")
        
        fecha = datetime.datetime.fromtimestamp(post['data']['created_utc']).strftime('%d-%m-%Y %H:%M')
        print(f"Hora de publicación: {fecha}")

        print(f"Subreddit: {post['data']['subreddit']}")
        print("-" * 80)

    # json = simplejson.dumps(redUY.json(), indent=4, sort_keys=True)  ## para formatear el json en la consola y que se entienda mas

init = False
TOKEN = 0

buscarPublicaciones("Biden", 3)