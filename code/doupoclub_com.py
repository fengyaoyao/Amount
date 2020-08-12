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
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, set_flow, wirteLog

# 获取签名配置


def get_sign(q1):

    config = config_data([
        {'url': 'https://doupoclub.com/receive/5ee210d78a135',
            'ischeck': ['5ee210d78a135', 'true']},
        {'url': 'https://doupoclub.com/receive/5f046d0dbbcab',
            'ischeck': ['5f046d0dbbcab', 'true']},
        {'url': 'https://doupoclub.com/receive/5ee2126bd1ca6',
            'ischeck': ['5ee2126bd1ca6', 'true']},
        {'url': 'https://doupoclub.com/receive/5efdc065c1bdc',
            'ischeck': ['5efdc065c1bdc', 'true']},
    ])

    # 代理
    proxy_ip = config['proxy_ip']
    # 签名xml
    xml = config['xml']

    # 设置代理请求
    proxies = {"http": 'http://' + proxy_ip}
    # 设置请求头
    headers = {'Content-Type': 'application/xml'}
    # 发起请求签名
    response = requests.post(
        config['url'], data=xml, headers=headers, proxies=proxies)

    config['response_url'] = response.url

    print('配置文件:', config)
    # 写入队列1
    q1.put(config)


# 根据连接获取udid


def get_udid(url):
    par = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(par.query)
    if len(query['udid'][0]) == 0:
        return False
    return query['udid'][0]

# 获取下载ID


def get_downloadId(q1, q2):

    queue_config = q1.get()
    udid = get_udid(queue_config['response_url'])
    proxy_ip = queue_config['proxy_ip']
    requests_url = 'https://doupoclub.com/download/' + \
        queue_config['ischeck'][0] + '?udid=' + udid

    proxies = {"http": 'http://' + proxy_ip}

    headers = {
        # 设置cookie
        'Cookie': 'udid=' + udid
    }

    # 请求获取downloadId
    result = requests.get(requests_url, proxies=proxies, headers=headers)
    # 字符串转字典
    content = json.loads(result.content)

    downloadId = content['data']['downloadId']

    if len(downloadId) > 0:
        print('下载ID:', downloadId)
        # 写入队列2
        q2.put({'downloadId': downloadId, 'Cookie': 'udid=' +
                udid, 'proxy_ip': queue_config['proxy_ip']})


# 获取manifest.plist 文件下载链接


def get_download_manifest_plist_url(q2, manifest_plist_urls):

    queue2_config = q2.get()
    manifest_plist_urls.append(queue2_config)

    # proxy_ip = queue2_config['proxy_ip']
    # Cookie = queue2_config['Cookie']
    # downloadId = queue2_config['downloadId']

    # proxies = {"http": 'http://' + proxy_ip}

    # headers = {'Cookie': Cookie}

    # status = True

    # downloadUrl = None

    # while status:

    #     download_status_url = 'https://doupoclub.com/progrees/' + downloadId

    #     download_status_data = requests.get(
    #         download_status_url, proxies=proxies, headers=headers)

    #     download_status_json = json.loads(download_status_data.content)

    #     if len(download_status_json['data']['downloadUrl']) > 1:

    #         downloadUrlDit = re.findall(
    # r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    # download_status_json['data']['downloadUrl'])

    #         downloadUrl = downloadUrlDit[0]

    #         status = False

    # manifest_plist_urls.append(downloadUrl)

if __name__ == '__main__':

    manifest_plist_urls = []
    thread_list = []
    q1 = queue.Queue()
    q2 = queue.Queue()

    for x in range(1, 3):
        t1 = threading.Thread(target=get_sign, args=(q1,))
        t1.start()
        sleep(2)
        thread_list.append(t1)

    for y in range(1, 3):
        t2 = threading.Thread(target=get_downloadId, args=(q1, q2,))
        t2.start()
        sleep(0.5)
        thread_list.append(t2)

    for z in range(1, 3):
        t3 = threading.Thread(
            target=get_download_manifest_plist_url, args=(q2, manifest_plist_urls,))
        t3.start()
        thread_list.append(t3)

    for Thread in thread_list:
        Thread.join()

    print('文件下载地址:', manifest_plist_urls)
