import requests as rq
import simplejson
import time
from datetime import datetime, timezone

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

def extract_subreddit(url):
    parts = url.split('/')
    if len(parts) > 2:
        return f"{parts[1]}/{parts[2]}"
    return None

def buscarPublicaciones(entidad, next_post_id, _time, sorting):
    """
    Fetches posts from the Reddit API based on the given entity.

    Args:
        entidad (str): The entity to search for in the posts.
        next_post_id (str): The ID of the last fetched post. Used for pagination.

    Returns:
        tuple: A tuple containing a list of posts and the ID of the next post.

    """

    headers = {
        'User-Agent': 'MyAPI/0.0.1',
        'Authorization': f'Bearer {TOKEN}'
    }

    url = 'https://oauth.reddit.com/r/politics/search.json'
    params = {
        'q': entidad,
        'sort': sorting,
        'limit': 100,
        'restrict_sr': True,
        't': _time
    }

    if next_post_id is not None:
        params['after'] = next_post_id

    response = rq.get(url, headers=headers, params=params)
    response_json = response.json()

    if response.status_code == 200:
        # formatted_json = simplejson.dumps(response_json, indent=4, sort_keys=True)
        # print(formatted_json)

        posts = []
        for data in response_json['data']['children']:
            if _time == 'day':
                created_utc = data['data']['created_utc']
                created_datetime = datetime.utcfromtimestamp(created_utc)
                formatted_date = created_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
                post = {
                    'related_entity': entidad,
                    'id': data['data']['id'],
                    'name': data['data']['name'],
                    'title': data['data']['title'],
                    'text': data['data']['selftext'] or 'No text available',
                    'date': formatted_date,
                    'cant_comments': data['data']['num_comments'],
                    'thumbsup': data['data']['score'],
                    "link": "reddit.com" + data['data']['permalink'],
                    "subreddit": extract_subreddit(data['data']['permalink'])
                }
            else:
                post = {
                    'related_entity': entidad,
                    'id': data['data']['id'],
                    'name': data['data']['name'],
                    'title': data['data']['title'],
                    'text': data['data']['selftext'] or 'No text available',
                    'date': time.strftime("%Y%m%d", time.gmtime(data['data']['created_utc'])),
                    'cant_comments': data['data']['num_comments'],
                    'thumbsup': data['data']['score'],
                    "link": "reddit.com" + data['data']['permalink'],
                    "subreddit": extract_subreddit(data['data']['permalink'])
                }
            posts.append(post)

        next_id = response_json['data']['after']
        if next_id is None:
            print(response_json['data']['after'])

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
    """
    Retrieves data for a politician from Reddit API.

    Args:
        Entity (str): The name of the politician.
        next_id (str): The ID of the next post to retrieve.

    Returns:
        tuple: A tuple containing a list of all posts and the ID of the next post.
    """

    global logged
    logged = False
    login()
    logged = True

    all_posts = []
    

    count = 1
    posts, next_id = buscarPublicaciones(Entity, next_id, 'week', 'relevance')
    print("=====================================================================================")
    print("=====================================================================================")
    print("===============================LA CANTIDAD DE POSTS ES===============================")
    print(f"========================================{len(posts)}=========================================")
    print("=====================================================================================")
    print(len(posts))
    for post in posts:
        all_posts.append(post)

    while next_id is not None and count < 10:
        posts, next_id = buscarPublicaciones(Entity, next_id, 'week', 'relevance')
        for post in posts:
          all_posts.append(post)
        count += 1

    if next_id is None:
        print("=====================================================================================")
        print("=====================================================================================")
        print("===================================NEXT ID IS NONE===================================")
        print("=====================================================================================")
        print("=====================================================================================")

    # Esta todo comentado pq no estamos utilizando los comentarios aun, en otra version tal vez se utilicen
    final_data = []
    response_count = 0
    posts_count = 0
    for post in all_posts:
        print(f"comentarios procesados: {response_count}")
        if response_count == 10000:
            break
        posts_count += 1
        print(f'Count = {posts_count} _------------_ obteniendo comentarios')
        data = fetch_comments(post['id'])

        print('Comentarios obtenidos')

        post_data = data[0]['data']['children'][0]['data']
        post_author = post_data['author']
        
        if post_author != 'AutoModerator':  # Avoid posts from 'AutoModerator'
            comments = data[1]['data']['children']
            cant_comments = 0
            for comment in comments:
                if cant_comments == 75:
                    break
                if comment['kind'] != 't1':
                    continue 
                response = {
                    'related_entity': Entity,
                    'id': post['id'],
                    'name': post['id'],
                    'title': post['title'],
                    'text': post['text'] or ' ',
                    'date': time.strftime("%Y%m%d", time.gmtime(comment['data']['created_utc'])),
                    'thumbsup': comment['data']['score'],
                    "link": "reddit.com" + comment['data']['permalink'],
                    "subreddit": extract_subreddit(comment['data']['permalink']),
                    "comment": comment['data']["body"]
                }
                final_data.append(response)
                response_count += 1
                cant_comments += 1

    print(f"comentarios procesados: {response_count}")
    return final_data, next_id


def get_politician_data_amount(Entity, amount):
    """
    Retrieves data for a politician from Reddit API.

    Args:
        Entity (str): The name of the politician.
        next_id (str): The ID of the next post to retrieve.

    Returns:
        tuple: A tuple containing a list of all posts and the ID of the next post.
    """

    global logged
    logged = False
    login()
    logged = True

    all_posts = []

    posts, _ = buscarPublicaciones(Entity, None, 'day', 'new')
    
    print("=====================================================================================")
    print("=====================================================================================")
    print("===============================LA CANTIDAD DE POSTS ES===============================")
    print(f"========================================{len(posts)}=======================================")
    print("=====================================================================================")

    for post in posts:
        all_posts.append(post)

    final_data = []
    response_count = 0
    posts_count = 0
    for post in all_posts:
        print(f"comentarios procesados: {response_count}")
        posts_count += 1
        print(f'Count = {posts_count} _------------_ obteniendo comentarios')
        data = fetch_comments(post['id'])

        print('Comentarios obtenidos')

        post_data = data[0]['data']['children'][0]['data']
        post_author = post_data['author']
        
        if post_author != 'AutoModerator':  # Avoid posts from 'AutoModerator'
            comments = data[1]['data']['children']
            cant_comments = 0
            for comment in comments:
                if response_count >= amount:
                    print("SE LLEGO A {amount} POSTS")
                    print(f"comentarios procesados: {response_count}")
                    return final_data
                if cant_comments == 150:
                    break
                if comment['kind'] != 't1':
                    continue 
                
                created_utc = comment['data']['created_utc']
                # Convert Unix timestamp to timezone-aware datetime object
                created_datetime = datetime.fromtimestamp(created_utc, tz=timezone.utc)
                # Format datetime object to string if necessary
                formatted_date = created_datetime.strftime('%Y-%m-%d %H:%M:%S')
                
                response = {
                    'related_entity': Entity,
                    'id': post['id'],
                    'name': post['id'],
                    'title': post['title'],
                    'text': post['text'] or ' ',
                    'date': formatted_date,
                    'thumbsup': comment['data']['score'],
                    "link": "reddit.com" + comment['data']['permalink'],
                    "subreddit": extract_subreddit(comment['data']['permalink']),
                    "comment": comment['data']["body"]
                }
                final_data.append(response)
                response_count += 1
                cant_comments += 1

    print(f"comentarios procesados: {response_count}")
    return final_data