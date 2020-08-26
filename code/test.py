#!/usr/bin/env python
import os
import re
import sys
import json
import queue
import random
import requests
import platform
import threading
import numpy as np
from time import sleep
import urllib.parse
import matplotlib.pyplot as plt
import cv2
from selenium import webdriver

sys.path.append('..\\')

from help.config import config_data
from help.tools import get_proxy_ip, wirteLog, get_mobileconfig_url


if __name__ == '__main__':


    xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text
    print(xml)


    # proxy_ip = get_proxy_ip()
    # print(proxy_ip)

    # post_url = 'https://www.xbai.app/oCsmuH/getudid/'

    # proxies = {"https": 'https://' + proxy_ip}
    # headers = {'Content-Type': 'application/xml'}
    # response = requests.post(post_url, data=xml, headers=headers, proxies=proxies)
    # print('发送XML响应URL状态', response.status_code)
    # print('发送XML响应URL', response.url)

    # print(xml)
    # par = urllib.parse.urlparse(response.url)
    # query = urllib.parse.parse_qs(par.query)
    # print(query)

    # data = {
    #     'query': query['query'][0],
    #     'hash': ''
    # }

    # headers1 = {
    #     'accept': 'application/json, text/javascript, */*; q=0.01',
    #     'accept-encoding': 'gzip, deflate, br',
    #     'accept-language': 'zh-CN,zh;q=0.9',
    #     'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    #     'origin': 'https://www.syt0351.com',
    #     'referer': response.url,
    #     'sec-fetch-dest': 'empty',
    #     'sec-fetch-mode': 'cors',
    #     'sec-fetch-site': 'same-origin',
    #     'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
    #     'x-requested-with': 'XMLHttpRequest',
    # }



    # response1 = requests.post('https://www.syt0351.com/oCsmuH/goapp', data=data, headers=headers1, proxies=proxies)

    # print('响应URL状态', response1.status_code)
    # print('响应URL', response1.url)

    # content = json.loads(response1.content)
    # print('响应内容', response1.content)
    # print(json)

    # wirteLog(response1.content)
    # mobileconfig_url = get_mobileconfig_url('./111.mobileconfig')
    # print(mobileconfig_url)
