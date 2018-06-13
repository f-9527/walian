# -*- coding:utf-8 -*-

import requests
import json


class DingTalk_sendMessage():
    def __init__(self):
        self.url = 'https://oapi.dingtalk.com/robot/send?' \
                      'access_token=15cef87df0d5c4aa60adf70c893840cba2b645855f68a2e6c3aaac48eac87f8f'
        self.HEADERS = {
            'Content-Type': 'application/json ;charset=utf-8'
        }

    def send_text_message(self, content):
        print(content)
        data = {
            'msgtype': 'text',
            'text': {'content': (content + ' \n @17602114603')},
            'at': {'atMobiles': ['17602114603']}

        }

        result = requests.post(url=self.url, data=json.dumps(data), headers=self.HEADERS)
        if result.status_code == 200:
            print('ok')
