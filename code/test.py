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

    
    # os.system('D:\\python381\\python.exe .\\doupoclub_com.py')
    # os.system('D:\\python381\\python.exe .\\iosvipsign_site.py')
    # os.system('D:\\python381\\python.exe .\\www_86scw_com.py')
    # os.system('D:\\python381\\python.exe .\\ios_tkls365_com.py')
    # headers = {'Cache-Control': 'no-cache'}
    # url = 'http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=53362&port=11&lb=1&pb=45&regions='
    # get_ip = requests.get(url, headers).text.strip()
    # print(get_ip)

    # x = [20, 40, 60, 80, 100, 120, 140]

    # y = [44.50, 75.65, 103.05, 138.35, 168.20, 187.30, 210.85]

    # parameters = np.polyfit(x, y, 1)

    # func = np.poly1d(parameters)
    # print(parameters)
    # plt.scatter(x, y)                      # print the original numbers in dots
    # x = [0] + x + [160]
    # plt.grid(True, color='gray')
    # plt.plot(x, func(x), color='orange', linestyle = '--')
    # plt.xlim(0, 160)
    # plt.ylim(0, 300)
    # plt.xlabel('W (Kg)')
    # plt.ylabel('F (N)')
    # plt.show()



    # st = 'position: fixed;width: 359px;height: 359px;top: 227px;left: 6px;border: 1px solid rgb(229, 229, 229);border-radius: 3px;'

    # result = re.compile(r'(?<=: )(\d+)(?=px;)').findall(st)
    # print(result)

    # split_str = st.split(";")
    # for x in split_str:
    #     print(x.split(":"))
    # print(split_str.split)

    # slideImg = cv2.imread('..\\file\\bg.jpg')
    # bgImg = cv2.imread('..\\file\\front.jpg')

    # result = cv2.matchTemplate(slideImg, bgImg, cv2.TM_CCOEFF_NORMED)
    # y, x = np.unravel_index(result.argmax(), result.shape)
    # print(y,x)
    # xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text
    # print(xml)


    #             udid_dit = re.compile(r'(?<=<key>UDID</key><string>)(.*?)(?=</string>)').findall(config_dit['xml'])

    #         loading_page_url = 'https://down.8iosapp.com/5KZD.app?udid=' + udid_dit[0]
    # print(xml)
    # proxy_ip = get_proxy_ip()

    # post_url = 'https://www.wnphb.com/download/report/azRQ'

    # proxies = {"https": 'https://' + proxy_ip}
    # headers = {'Content-Type': 'application/xml'}
    # response = requests.post(post_url, data=xml, headers=headers, proxies=proxies)
    # print('发送XML响应URL状态', response.status_code)
    # print('发送XML响应URL', response.url)

    # print(xml)

    # url = 'https://iosvipsign.site/install/798-75?appenddata=%7B%22ChannelInfo%22%3A%22%7C%7C798%7Chttps%3A%2F%2F369vk.com%2F%7C1597717571446%7Cf5705def7c6ada08c3f521c625971617%22%2C%22test%22%3A%22hello%22%7D'
    # par = urllib.parse.urlparse(url)
    # query = urllib.parse.parse_qs(par.query)
    # print(query)

    # mobileconfig_url = get_mobileconfig_url('./111.mobileconfig')
    # print(mobileconfig_url)
