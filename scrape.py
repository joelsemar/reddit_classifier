import time
import os
import re
import requests
import simplejson
import random
csv_delimiter = '\t'
headers = {"User-Agent": "Just playing with some stuff, (see github.com/joelsemar/reddit_classifier)  love you guys :) -- /u/semarj"}
base_url = 'http://reddit.com'
csv_headers = ('id', 'ups', 'downs', 'text')
burst_call_count = 30


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


def traverse_post_listing(subreddit_name, posts, burst=False):
    if burst and burst_call_count <= 0:
        return

    for post in posts:
        data = post['data']
        comments = api_call(base_url + data['permalink'] + '.json', burst=burst)

        comment_list = traverse_comment_listing(comments[1])
        with open('data/%s' % subreddit_name , 'a') as output_file:
            for comment in comment_list:
                output_file.write(dict_to_line(comment))


def traverse_subreddit(name, page_depth=5, burst=False):
    os.system('rm -rf data/%s' % name)
    current_after = ''
    count = 0
    current_url = '%s/r/%s.json' % (base_url, name)
    params = {}
    if burst:
        global burst_call_count
        burst_call_count = 30
        page_depth = 100

    for i in range(page_depth):

        if burst and burst_call_count <= 0:
            return

        if current_after and count:
           params['after'] = current_after
           params['count'] = count

        page = api_call(current_url, params=params, burst=burst)
        posts = page.get('data', {}).get('children', [])
        count += len(posts)
        current_after = page.get('data', {}).get('after', '')
        traverse_post_listing(name, posts, burst=burst)

def api_call(url, params={}, burst=False):
    global burst_call_count
    response = requests.get(url, params=params, headers=headers)
    if not burst:
        time.sleep(2)
    burst_call_count -= 1
    return simplejson.loads(response.content)


def unpack_data(filename):
    from classify import categories
    subreddit = filename.split('.')[0]
    if not os.path.exists(os.path.join('data', subreddit)):
        print "I don't seem to have any data for that subreddit. Try scrape.traverse_subreddit(%s)" % subreddit
        return False
    base_path = os.path.join('labeled_data', subreddit)

    os.system('rm -rf labeled_data/%s' % subreddit)
    for category in categories:
        category_name = category[-1]
        for data_set in ['training', 'test']:
            path = os.path.join(base_path, data_set, category_name)
            if not os.path.exists(path):
                os.makedirs(path)

    with open(os.path.join('data', filename), 'rb') as input_file:
        for document in input_file.readlines():
            document = document_to_dict(document)
            if not document:
                continue
            category = label(document)
            if random.random() > 0.90:
                doc_type = 'test'
            else:
                doc_type = 'training'
            doc_file = os.path.join(base_path, doc_type,  category,  'id_' + str(document['id']))

            with open(doc_file, 'w') as doc_file:
                doc_file.write(document['text'])

    return True

def label(document):
    from classify import categories
    for category in categories:
        if int(document['ups']) - int(document['downs']) > category[0]:
            return category[-1]
    return 'n/a'



def document_to_dict(document):
    ret = {}
    values = document.split(csv_delimiter)
    if len(values) != len(csv_headers):
        return None
    for index, value in enumerate(document.split(csv_delimiter)):
        ret[csv_headers[index]] = value
    return ret

def dict_to_line(dict):
    dict['body'] = re.sub('\n', ' ', dict['body'])
    return '%(id)s\t%(ups)s\t%(downs)s\t%(text)s\n' % {'id': dict['id'].encode('utf-8'),
                                                        'ups': dict['ups'], 'downs': dict['downs'],
                                                        'text': dict['body'].encode('utf-8')}

