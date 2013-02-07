import time
import requests
import simplejson
headers = {"User-Agent": "Just playing with some stuff, love you guys :) -- /u/semarj"}
interval = 2
base_url = 'http://reddit.com'


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

def traverse_post_listing(posts):
    for post in posts:
        data = post['data']
        try:
            comments = api_call(base_url + data['permalink'] + '.json')
        except:
            import pdb;pdb.set_trace()

        time.sleep(interval)
        comment_list = traverse_comment_listing(comments[1])
        with open('reddit_dump.json' , 'a') as output_file:
            output_file.write(simplejson.dumps(comment_list))
            output_file.write('\n')


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
        traverse_post_listing(posts)


def api_call(url, params={}):
    response = requests.get(url, params=params, headers=headers)
    time.sleep(interval)
    return simplejson.loads(response.content)


