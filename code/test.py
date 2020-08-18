#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import cv2
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
from selenium import webdriver
sys.path.append('../')
from help.config import config_data
from help.tools import get_proxy_ip, wirteLog, get_mobileconfig_url


if __name__ == '__main__':

    st = 'position: fixed;width: 359px;height: 359px;top: 227px;left: 6px;border: 1px solid rgb(229, 229, 229);border-radius: 3px;'

    result = re.compile(r'(?<=: )(\d+)(?=px;)').findall(st)
    print(result)

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

    # url = 'https://iosvipsign.site/install/798-75?appenddata=%7B%22ChannelInfo%22%3A%22%7C%7C798%7Chttps%3A%2F%2F369vk.com%2F%7C1597717571446%7Cf5705def7c6ada08c3f521c625971617%22%2C%22test%22%3A%22hello%22%7D'
    # par = urllib.parse.urlparse(url)
    # query = urllib.parse.parse_qs(par.query)
    # print(query)

    # mobileconfig_url = get_mobileconfig_url('./111.mobileconfig')
    # print(mobileconfig_url)
