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
from help.tools import get_proxy_ip, wirteLog, get_mobileconfig_url

# 获取签名配置


def get_sign():

    config = config_data([
        # {'url': 'https://doupoclub.com/receive/5ee210d78a135','ischeck': ['5ee210d78a135', 'true']},
        # {'url': 'https://doupoclub.com/receive/5f046d0dbbcab','ischeck': ['5f046d0dbbcab', 'true']},
        # {'url': 'https://doupoclub.com/receive/5ee2126bd1ca6','ischeck': ['5ee2126bd1ca6', 'true']},
        {'url': 'https://doupoclub.com/receive/5efdc065c1bdc',
            'ischeck': ['5efdc065c1bdc', 'true']},
    ])

    try:

        proxy_ip = config['proxy_ip']

        print('代理IP:', proxy_ip)

        # 签名xml
        xml = config['xml']

        # 设置代理请求
        proxies = {"https": 'https://' + proxy_ip}
        # 设置请求头

        headers = {'Content-Type': 'application/xml', 'Connection': 'close'}
        # 发起请求签名
        response = requests.post(
            config['url'], data=xml, headers=headers, proxies=proxies)

        if len(response.url) > 1:
            config['response_url'] = response.url
            print('配置文件', config)
            return config

    except (Exception, requests.exceptions.ProxyError, ConnectionResetError, UnboundLocalError) as e:
        print('错误信息提示：%s' % e)
        return None


# 根据连接获取udid


def get_udid(url):
    par = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(par.query)

    try:
        if len(query['udid'][0]) == 0:
            return False
    except (Exception, KeyError) as e:
        print('错误信息提示：%s' % e)
        return False

    return query['udid'][0]

# 获取下载ID


def get_downloadId(queue_config):

    udid = get_udid(queue_config['response_url'])
    if udid == False:
        return None
    try:

        proxy_ip = queue_config['proxy_ip']
        requests_url = 'https://doupoclub.com/download/' + \
            queue_config['ischeck'][0] + '?udid=' + udid

        proxies = {"https": 'https://' + proxy_ip}

        headers = {
            'Cookie': 'udid=' + udid,
            'referer': queue_config['response_url'],
            'Connection': 'close',
        }

        # 请求获取downloadId
        result = requests.get(requests_url, proxies=proxies, headers=headers)
        print('请求获取downloadId响应:', result.content)

        # 字符串转字典
        content = json.loads(result.content)

        downloadId = content['data']['downloadId']

    except (TypeError, requests.exceptions.ProxyError) as e:
        print('错误信息提示：%s' % e)
        return None

    if len(downloadId) > 0:

        print('下载ID:', downloadId)

        return {'downloadId': downloadId, 'Cookie': 'udid=' + udid, 'referer': queue_config['response_url'], 'proxy_ip': queue_config['proxy_ip']}

    else:
        return None

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
        'https': 'https://' + proxy_ip
    }

    headers = {
        'Cookie': queue2_config['Cookie'],
        'referer': queue2_config['referer'],
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        # 'Connection': 'close'
    }

    for request in range(1, 30):

        download_status_url = 'https://doupoclub.com/progrees/' + \
            queue2_config['downloadId']

        try:
            download_status_data = requests.get(
                download_status_url, proxies=proxies, timeout=(6.05, 27.05))
        except (BaseException, Exception, ConnectionResetError) as e:
            print('错误信息提示：%s' % e)
            continue

        try:
            download_status_json = json.loads(download_status_data.content)
        except Exception as e:
            print('错误信息提示：%s' % e)
            continue

        if download_status_json['data']['complete'] != True:
            continue

        if (download_status_json['data']['complete'] == True and len(download_status_json['data']['downloadUrl'])) > 1:

            downloadUrlDit = re.findall(
                r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', download_status_json['data']['downloadUrl'])

            print('获得下载地址:', downloadUrlDit[0])
            wirteLog(downloadUrlDit[0])
            break

        sleep(0.5)


if __name__ == '__main__':

    strs = 'left: 27.5px;'
    result = re.compile(r'\d+\.?\d*').findall(strs)[0]
    print( float(result) + 1)
    # proxy_ip = get_proxy_ip()
    # print('代理IP',proxy_ip)
    # xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text
    # print('xml',xml)
    # result = re.compile(r'(?<=<key>UDID</key><string>)(.*?)(?=</string>)').findall(xml)
    # print(result)
    # post_url = 'https://down.8iosapp.com/download/report/5KZD'
    # # proxies = {"https": 'https://' + proxy_ip}
    # headers = {'Content-Type': 'application/xml'}
    # response = requests.post(post_url, data=xml, headers=headers)
    # print('发送XML响应URL状态', response.status_code)
    # print('发送XML响应URL', response.url)
    # print('发送XML响应header', response.headers)

    # mobileconfig_url = get_mobileconfig_url('./111.mobileconfig')
    # print(mobileconfig_url)
