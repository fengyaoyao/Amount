#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import queue
import random
import requests
import platform
import threading
from time import sleep
import urllib.parse
from selenium import webdriver
sys.path.append('../')
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, set_flow, wirteLog


def runs():

    proxy_ip = get_proxy_ip()

    print('代理地址:', proxy_ip)

    if proxy_ip == False:
        exit()

    xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text

    proxies = {"http": 'http://' + proxy_ip, "https": 'https://' + proxy_ip}

    config = random.choice([
        {'url':'https://doupoclub.com/receive/5ee210d78a135','ischeck':['5ee210d78a135','true']},
        {'url':'https://doupoclub.com/receive/5f046d0dbbcab','ischeck':['5f046d0dbbcab','true']},
        {'url':'https://doupoclub.com/receive/5ee2126bd1ca6','ischeck':['5ee2126bd1ca6','true']},
        {'url':'https://doupoclub.com/receive/5efdc065c1bdc','ischeck':['5efdc065c1bdc','true']},
        {'url':'https://doupoclub.com/receive/5ef5bbccb0ce6','ischeck':['5ef5bbccb0ce6','true']},
    ])

    try:

        # 发送XML进行签名
        headers = {'Content-Type': 'application/xml'}
        response = requests.post(config['url'], data=xml, headers=headers, proxies=proxies)
        print("响应状态:", response.status_code)
        print('响应地址:', response.url)

        par = urllib.parse.urlparse(response.url)
        query = urllib.parse.parse_qs(par.query)
        requests_url = 'https://doupoclub.com/download/'+ config['ischeck'][0] +'?udid=' + query['udid'][0]

        headers = {
            'Content-Type': 'application/xml',
            'Cookie':'udid=' + query['udid'][0]
        }

        print('请求下载ID地址',requests_url)

        result = requests.get(requests_url,proxies=proxies,headers=headers)

        content = json.loads(result.content)

        status = True

        while status:

         download_status_url  'https://doupoclub.com/progrees/' + content['data']['downloadId']


            

        print('downloadId:',content['data']['downloadId'])

    except (BaseException, UnboundLocalError, Exception, ConnectionRefusedError) as e:
        print('错误信息提示：%s'%e)
runs()
# for i in range(1, 2):
#     t = threading.Thread(target=runs)
#     t.start()
#     sleep(2)
# url = 'https://doupoclub.com/app/5ef5bbccb0ce6?udid=4682ys262tu4p4m34794g22o3311d59248vm3843&t=1597223291&device=iPhone8,2&version=17D50&sign=bed101a34959096d1cfb0646330bea4c'
# par = urllib.parse.urlparse(url)

# query = urllib.parse.parse_qs(par.query)

# print(par)
# print(query['udid'][0])



