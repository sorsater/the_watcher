
import http.client

from googlesearch import search
from urllib.parse import urlencode
import json
import os

class Pusher():
    def __init__(self, msg):
        self.msg = msg

        self.credentials_file = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'credentials.json')
        self.API_TOKEN = None
        self.USER_TOKEN = None

        self.read_credentials()
        self.push()

    def read_credentials(self):
        print('Reading credentials')
        credentials = json.load(open(self.credentials_file))
        self.API_TOKEN = credentials['API_TOKEN']
        self.USER_TOKEN = credentials['USER_TOKEN']

        if self.API_TOKEN == 'API_TOKEN':
            raise ValueError('You need to setup your own credentials in credentials.json')

    def push(self):
        print('Trying to push!')
        try:
            conn = http.client.HTTPSConnection("api.pushover.net:443")
            conn.request("POST", "/1/messages.json",
                urlencode({
                    "token": self.API_TOKEN,
                    "user": self.USER_TOKEN,
                    "message":  self.msg,
                    "html": 1,
                }), { "Content-type": "application/x-www-form-urlencoded" })
            conn.getresponse()
        except Exception as e:
            print('Failed!', e)
        else:
            print('Success!')


class GoogleWatcher():
    def __init__(self, name, search_string, **kwargs):
        self.ignore_urls_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'ignore_urls.txt')

        self.search_string = search_string
        self.kwargs = kwargs

        self.msg = name + ': '
        self.read_blocked_urls()
        self.search()
    
    def read_blocked_urls(self):
        self.blocked_urls = open(self.ignore_urls_file_path).read().splitlines()

    def search(self):
        matches = ['Matches:']
        print(self.search_string)
        print(self.kwargs)
        cntr = 1
        for url in search(self.search_string, **self.kwargs):
            valid = True
            for blocked in self.blocked_urls:
                if blocked in url:
                    valid = False
                    continue
            if valid:
                print(url)
                matches.append('{}: {}'.format(cntr, url))
                cntr += 1

        self.msg += '\n'.join(matches) if matches else '&#x1f643;'

if __name__ == '__main__':
    apps = [
        GoogleWatcher('cool', '"broder john" "cool" vinyl', stop=10, tbs='qdr:m', lang='sv'),
        #GoogleWatcher('ww3', 'world war 3 sweden', stop=10, tbs='qdr:m', lang='sv'),
    ]

    total_msg = '\n'.join([app.msg for app in apps])

    pusher = Pusher(total_msg)
