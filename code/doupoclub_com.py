#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
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
from help.config import config_data
from help.tools import get_proxy_ip, wirteLog

# 获取签名配置


def get_sign(q1):

    config = config_data([
        {'url': 'https://doupoclub.com/receive/5ee210d78a135','ischeck': ['5ee210d78a135', 'true']},
        {'url': 'https://doupoclub.com/receive/5f046d0dbbcab','ischeck': ['5f046d0dbbcab', 'true']},
        {'url': 'https://doupoclub.com/receive/5ee2126bd1ca6','ischeck': ['5ee2126bd1ca6', 'true']},
        {'url': 'https://doupoclub.com/receive/5efdc065c1bdc','ischeck': ['5efdc065c1bdc', 'true']},
        {'url': 'https://doupoclub.com/receive/5ee36de675aa3','ischeck': ['5ee36de675aa3', 'true']},
        {'url': 'https://doupoclub.com/receive/5efb502309ffd','ischeck': ['5efb502309ffd', 'true']},
        {'url': 'https://doupoclub.com/receive/5ee4a69545a95','ischeck': ['5ee4a69545a95', 'true']},
        {'url': 'https://doupoclub.com/receive/5efcc0cedd73b','ischeck': ['5efcc0cedd73b', 'true']},

    ])

    if config['proxy_ip'] == False or config['xml'] == False:
        q1.put('pass')
        return None

    proxy_ip = config['proxy_ip'] 

    # 代理
    # 签名xml
    xml = config['xml']

    # 设置代理请求
    proxies = {"http": 'http://' + proxy_ip}
    # 设置请求头

    headers = {'Content-Type': 'application/xml', 'Connection': 'close'}
    # 发起请求签名
    try:

        response = requests.post(
            config['url'], data=xml, headers=headers, proxies=proxies)

        if len(response.url) > 1:
            config['response_url'] = response.url
            print('配置文件', config)
            # 写入队列1
            q1.put(config)

    except (requests.exceptions.ProxyError, ConnectionResetError, UnboundLocalError) as e:
        print('发起xml请求签名错误信息提示：%s' % e)
        q1.put('pass')


# 根据连接获取udid


def get_udid(url):
    par = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(par.query)

    try:
        if len(query['udid'][0]) == 0:
            return False
    except KeyError as e:
        print('获取udid错误信息提示：%s' % e)
        return False

    return query['udid'][0]

# 获取下载ID


def get_downloadId(q1, q2):

    queue_config = q1.get()
    q1.task_done()
    if queue_config == 'pass':
        q2.put('pass')
        return

    udid = get_udid(queue_config['response_url'])

    if udid == False:
        q2.put('pass')
        return

    proxy_ip = queue_config['proxy_ip']
    requests_url = 'https://doupoclub.com/download/' + \
        queue_config['ischeck'][0] + '?udid=' + udid

    proxies = {"http": 'http://' + proxy_ip}

    headers = {
        # 设置cookie
        'Cookie': 'udid=' + udid,
        'referer': queue_config['response_url'],
        'Connection': 'close',
    }
    # print(headers)
    try:

        # 请求获取downloadId
        result = requests.get(requests_url, proxies=proxies, headers=headers)
        print('下载ID响应:',result.content)
        # 字符串转字典
        content = json.loads(result.content)
        downloadId = content['data']['downloadId']
    except (Exception, requests.exceptions.ProxyError, TypeError) as e:
        print('获取downloadId错误信息提示：%s' % e)
        q2.put('pass')
        return

    if len(downloadId) > 0:

        data = {'downloadId': downloadId, 'Cookie': 'udid=' + udid,
                'referer': queue_config['response_url'], 'proxy_ip': queue_config['proxy_ip']}

        print('下载ID配置:', data)
        # 写入队列2
        q2.put(data)
    else:
        q2.put('pass')

# 获取manifest.plist 文件下载链接


def get_download_manifest_plist_url(q2):

    queue2_config = q2.get()
    q2.task_done()

    if queue2_config == 'pass':
        return

    proxy_ip = queue2_config['proxy_ip']

    if queue2_config['proxy_ip'] == False:
        proxy_ip = get_proxy_ip()
        if proxy_ip == False:
            return

    proxies = {
        'http': 'http://' + proxy_ip
    }

    headers = {
        'Cookie': queue2_config['Cookie'],
        'referer': queue2_config['referer'],
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'Connection': 'close'
    }

    for request in range(1, 120):

        download_status_url = 'https://doupoclub.com/progrees/' + queue2_config['downloadId']

        try:
            #  timeout=(6.05, 27.05)
            download_status_data = requests.get(
                download_status_url, proxies=proxies)
        except (BaseException, Exception, ConnectionResetError) as e:
            print('获取manifest.plist链接错误信息提示：%s' % e)
            continue

        try:
            download_status_json = json.loads(download_status_data.content)
        except Exception as e:
            print('解析manifest.plist错误信息提示：%s' % e)
            continue

        if download_status_json['data']['complete'] != True:
            continue

        if (download_status_json['data']['complete'] == True and len(download_status_json['data']['downloadUrl'])) > 1:

            downloadUrlDit = re.findall(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', download_status_json['data']['downloadUrl'])

            print('获得下载地址:', downloadUrlDit[0])
            wirteLog(downloadUrlDit[0])
            break

        sleep(1)

if __name__ == '__main__':

    q1 = queue.Queue()
    q2 = queue.Queue()

    for y in range(1, 10):
        t1 = threading.Thread(target=get_sign, args=(q1,))
        t1.start()
        t1.join()
        sleep(1)

    for y in range(1, 10):
        t2 = threading.Thread(target=get_downloadId, args=(q1, q2,))
        t2.start()
        t2.join()
        sleep(0.5)

    for z in range(1, 10):
        t3 = threading.Thread(
            target=get_download_manifest_plist_url, args=(q2,))
        t3.start()

    print('主程序结束')
