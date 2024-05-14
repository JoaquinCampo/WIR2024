import requests as rq
import simplejson
import time

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

def buscarPublicaciones(entidad, next_post_id):
    headers = {
        'User-Agent': 'MyAPI/0.0.1',
        'Authorization': f'Bearer {TOKEN}'
    }

    url = 'https://oauth.reddit.com/r/politics/search.json'
    params = {
        'q': entidad,
        'sort': 'new',
        'limit': 9,
        'restrict_sr': True
    }

    if next_post_id is not None:
        params['after'] = next_post_id

    response = rq.get(url, headers=headers, params=params)
    response_json = response.json()

    if response.status_code == 200:
        formatted_json = simplejson.dumps(response_json, indent=4, sort_keys=True)

        posts = []
        for data in response_json['data']['children']:
            
            post = {
                'id': data['data']['id'],
                'title': data['data']['title']
            }
            posts.append(post)

        next_id = response_json['data']['after']
        return posts, next_id
        
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def fetch_comments(post_id):
    headers = {
        'User-Agent': 'MyAPI/0.0.1',
        'Authorization': f'Bearer {TOKEN}'
    }

    url = f'https://oauth.reddit.com/r/politics/comments/{post_id}.json'

    response = rq.get(url, headers=headers)
    response_json = response.json()
    
    if response.status_code == 200:
        return response_json
    else:
        print(f"Failed to fetch comments: {response.status_code}")
        return None

def collect_threads(comments, prefix=''):
    """ Recursively collects threads of conversations from comments. """
    threads = []
    for comment in comments:
        if 'body' in comment['data']:
            # Current comment text
            current_text = f"{comment['data']['author']} : {comment['data']['body']}\n"
            full_text = prefix + current_text

            # If there are replies, recurse and append each reply thread
            if 'replies' in comment['data'] and isinstance(comment['data']['replies'], dict):
                threads.extend(collect_threads(comment['data']['replies']['data']['children'], full_text))
            else:
                # If no replies, this is the end of the thread
                threads.append(full_text.strip())

    return threads

def get_politician_data(Entity, next_id):
    global logged
    logged = False
    login()
    logged = True
    cant_requests = 0

    final_data = []

    all_posts = []

    cant_requests += 1
    posts, next_id = buscarPublicaciones(Entity, next_id)
    for post in posts:
        all_posts.append(post)

    count = 0
    while next_id is not None and count < 10:
        cant_requests += 1
        if cant_requests == 100:
            print('Esperando 60 segundos para mantenerse dentro del limite de requests')
            cant_requests = 0
            time.sleep(55)   
        posts, next_id = buscarPublicaciones(Entity, next_id)
        for post in posts:
          all_posts.append(post)
        count += 1

    posts_count = 0
    for post in all_posts:
        posts_count += 1
        print(f'Count = {posts_count} _------------_ obteniendo comentarios')
        data = fetch_comments(post['id'])
        print('Comentarios obtenidos')

        post_data = data[0]['data']['children'][0]['data']
        post_author = post_data['author']
        post_text = post_data['selftext'] or post_data['title']
        
        if post_author != 'AutoModerator':  # Avoid posts from 'AutoModerator'
            comments = data[1]['data']['children']
            unformatted_threads = collect_threads(comments)
            unformatted_threads.pop(0)
            for thread in unformatted_threads:
                final_data.append(f'{post_author}: {post_text} \n{thread}')

    return final_data, next_id