#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json, config #標準のjsonモジュールとconfig.pyの読み込み
from requests_oauthlib import OAuth1Session
import pandas as pd
import sys
import MeCab

#config.pyにAPIキーを書いておく。
CK = config.CONSUMER_KEY
CS = config.CONSUMER_SECRET
AT = config.ACCESS_TOKEN
ATS = config.ACCESS_TOKEN_SECRET
twitter = OAuth1Session(CK, CS, AT, ATS) #認証処理

url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

#調べる対象
keywords = ["疲", "しんどい", "眠"]

# とくにパラメータは無い
params = {}

# OAuth で GET
twitter = OAuth1Session(CK, CS, AT, ATS)
res = twitter.get(url, params = params)


text_list = []

if res.status_code == 200: #正常通信出来た場合
    timelines = json.loads(res.text) #レスポンスからタイムラインリストを取得
    for line in timelines: #タイムラインリストをループ処理
        text_list.append(line['text'])
else: #正常通信出来なかった場合
    print("Failed: %d" % res.status_code)


print("最近のツイートを表示します。")
for text in text_list:
    print(text)

m = MeCab.Tagger("-Owakati")
keitaiso_list = []
for text in text_list:
    keitaiso_list.extend(m.parse(text).split(" "))

number = 0
for keitaiso in keitaiso_list:
    for key in keywords:
        if key in keitaiso:
            number += 1

print("あなたの疲れ指数は:")
tsukare = number / len(text_list)
print(tsukare)
