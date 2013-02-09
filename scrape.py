import time
import os
import requests
import simplejson
from classify import categories
csv_delimiter = '\t'
headers = {"User-Agent": "Just playing with some stuff, love you guys :) -- /u/semarj"}
base_url = 'http://reddit.com'
csv_headers = ('id', 'ups', 'downs', 'text')


def traverse_comment_listing(listing):
    ret = []
    def _traverse_listing(listing):
        for child in listing.get('data', {}).get('children', []):
            data = child.get('data',{})
            if 'ups' in data and 'downs' in data:
                ret.append({'id': data['id'],'ups': data['ups'], 'downs': data['downs'], 'body': data['body']})
            replies = data.get('replies', {})
            if replies:
                _traverse_listing(replies)
        return ret
    return _traverse_listing(listing)

def traverse_post_listing(subreddit_name, posts):
    for post in posts:
        data = post['data']
        try:
            comments = api_call(base_url + data['permalink'] + '.json')
        except:
            pass

        comment_list = traverse_comment_listing(comments[1])
        with open('data/%s' % subreddit_name , 'a') as output_file:
            for comment in comment_list:
                output_file.write(dict_to_line(comment))


def traverse_subreddit(name, depth=5):
    current_after = ''
    count = 0
    current_url = '%s/r/%s.json' % (base_url, name)
    params = {}
    for i in range(depth):
        if current_after and count:
           params['after'] = current_after
           params['count'] = count
        page = api_call(current_url, params=params)
        posts = page.get('data', {}).get('children', [])
        count += len(posts)
        current_after = page.get('data', {}).get('after', '')
        traverse_post_listing(name, posts)

def api_call(url, params={}, interval=2):
    response = requests.get(url, params=params, headers=headers)
    time.sleep(interval)
    return simplejson.loads(response.content)


def explode_dump(filename):
    subreddit = filename.split('.')[0]
    for category in categories:
        category_name = category[-1]
        path = os.path.join('labled_data', subreddit, category_name)
        if not os.path.exists(path):
            os.makedirs(path)
    with open(os.path.join('data', filename), 'rb') as input_file:
        for document in input_file.readlines():
            document = document_to_dict(document)
            category = label(document)
            with open(os.path.join(category, 'id_' + str(document['id'])), 'w') as doc_file:
                doc_file.write(document['body'].encode('utf-8'))

def label(document):
    for category in categories:
        if int(document['ups']) - int(document['downs']) > category[0]:
            return category[-1]



def document_to_dict(document):
    ret = {}
    for index, value in enumerate(document.split(csv_delimiter)):
        ret[csv_headers[index]] = value
    return ret

def dict_to_line(dict):
    return '%(id)s\t%(ups)s\t%(downs)s\t%(text)s\n' % {'id': dict['id'].encode('utf-8'),
                                                        'ups': dict['ups'], 'downs': dict['downs'],
                                                        'text': dict['body'].encode('utf-8')}

