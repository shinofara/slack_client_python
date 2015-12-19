#coding: utf-8

import urllib
import urllib2
import datetime
import json


class Client:
    SLACK_URL = 'https://slack.com/api/'
    SLACK_ARCHIVE_URL_FMT = "https://%s.slack.com/archives/%s"

    token = ''
    account = ''
    botName = 'worker'

    def __init__(self, account, token):
        self.token = token
        self.account = account


    def makeUrl(self, method):
        return self.SLACK_URL + method

    def makeArchiveUrl(self, cName):
        return self.SLACK_ARCHIVE_URL_FMT % (self.account, cName)

    #-----------
    # Message
    #----------
    def post(self, text, channel):
        params = {'channel':channel,
                  'text': text,
                  "username": self.botName,
                  "icon_url": "http://pixenlarge.com/examples/c/173_construction_worker.jpg",
        }
        return self.request(self.makeUrl("chat.postMessage"), params)

    #-----------
    # Channel
    #----------
    def info(self, cid):
        params = {'channel': cid}
        return self.request(self.makeUrl("channels.info"), params) 

    def create(self):
        now = datetime.datetime.now()
        cName = "test_" + "{0:%Y%m%d%H%M}".format(now)
        params = {'name': cName }
        return self.request(self.makeUrl("channels.create"), params)

    def archive(self, channel):
        params = {'channel': channel['id'] }
        self.request(self.makeUrl("channels.archive"), params)
        return self.makeArchiveUrl(channel['name'])

    def invite(self, channel):
        params = {'channel': channel['id'], 'user': uid }
        print self.request(self.makeUrl("channels.invite"), params)

    def request(self, url, params):
        # tokeをここで追加
        params['token'] = self.token

        params = urllib.urlencode(params)

        req = urllib2.Request(url)
        # ヘッダ追加
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')
        # パラメータ追加
        req.add_data(params)

        res = urllib2.urlopen(req)

        # レスポンス取得
        return json.loads(res.read())
