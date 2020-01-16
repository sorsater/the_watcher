
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
        self.blocked_urls = ['seriousrelatedream']
        self.search_string = search_string
        self.kwargs = kwargs

        self.msg = name + ': '
        self.search()

    def search(self):
        matches = []
        print(self.search_string)
        print(self.kwargs)
        cntr = 1
        for url in search(self.search_string, **self.kwargs):
            for blocked in self.blocked_urls:
                if blocked not in url:
                    print(url)
                    matches.append(f'{cntr}: {url}')
                    cntr += 1

        self.msg += '\n'.join(matches) if matches else '&#x1f643;'

if __name__ == '__main__':
    apps = [
        GoogleWatcher('cool', '"broder john" "cool" vinyl lp', stop=10, tbs='qdr:m', lang='sv'),
        #GoogleWatcher('ww3', 'world war 3 sweden', stop=10, tbs='qdr:m', lang='sv'),
    ]

    total_msg = '\n'.join([app.msg for app in apps])

    pusher = Pusher(total_msg)
