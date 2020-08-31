#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import requests
import os
import logging
from datetime import datetime
from pathlib import Path
import numpy as np
import cv2
import json
import platform
import shutil
import random
from time import sleep


# 判断字符串是否是json
def is_json(str):

    try:
        json_object = json.loads(str)
    except ValueError:
        return False
    return True


# 获取操作系统
def get_system():

    return platform.system()

# 获取当前目录


def get_dir():

    return os.getcwd()

# 获取代理IP


def get_proxy_ip():

    headers = {'Cache-Control': 'no-cache'}
    url = 'http://http.tiqu.qingjuhe.cn/getip?num=1&type=1&pack=53730&port=1&lb=1&pb=4&regions='
    get_ip = requests.get(url, headers).text.strip()

    if is_json(get_ip):

        result_str = json.loads(get_ip)

        if result_str['code'] == '121':
            
            print(result_str['msg'])
            exit()

        elif result_str['msg'] == '请2秒后再试':
            sleep(1.5)
            get_ip = requests.get(url, headers).text.strip()

        elif result_str['code'] == '113' and len(result_str['msg']) > 1:
            myip = re.findall(r'[0-9]+(?:\.[0-9]+){3}', result_str['msg'])[0]
            white_proxy_url = 'http://ty-http-d.upupfile.com/index/white/add?neek=tyhttp487901&appkey=3e096aec1eecdba33d44249454053a07&white='
            response = requests.get(white_proxy_url + myip, headers).text
            get_ip = requests.get(url, headers).text.strip()

    match_list = re.findall(r'[0-9]+(?:\.[0-9]+){3}', get_ip)

    if len(match_list) == 1:
        return get_ip
    else:
        return False

# 生成字符串


def set_flow():

    return datetime.now().strftime('%Y%m%d%H%M%S%f') +'_'+ str(random.randint(10000,99999))


# 查找指定文件


def find_file(path):

    my_file = Path(path)
    find_arr = ''

    if my_file.exists():
        dirs = os.listdir(path)

        for file in dirs:

            if re.match('.+\\.(mobileconfig)$', file):

                find_arr = file
                break

        return find_arr

# 删除文件夹


def delete_path(path):

    try:
        my_file = Path(path)

        if my_file.exists():

            shutil.rmtree(path)
    except Exception as e:
        print(e)

# 获取mobileconfig文件url地址


def get_mobileconfig_url(path):

    file = open(path, 'rb')
    content = file.readlines()
    data = []

    for i in range(0, len(content)):
        # 匹配模式
        pattern = re.compile(
            r'<string>http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
        # bytes 转string
        string = "".join(map(chr, content[i]))
        # 匹配
        url = re.findall(pattern, string.strip())

        if url:
            data += re.compile(
                r'(?<=<string>)(.*?)(?=</string>)').findall(url[0])

    file.close()

    return data

# 记录日志


def wirteLog(msg):

    logging.basicConfig(level=logging.INFO,
                        filename="../log/{}.log".format(
                            datetime.now().strftime('%Y-%m-%d')),
                        filemode='a',
                        format='%(asctime)s-%(filename)s-%(levelname)s: %(message)s')
    logging.info(msg)

# 获取移动坐标


def get_move_coordinates(bg_path, front_path):

    bg = cv2.imread(bg_path)
    front = cv2.imread(front_path)
    # 灰度处理
    bg = cv2.cvtColor(bg, cv2.COLOR_BGR2GRAY)
    front = cv2.cvtColor(front, cv2.COLOR_BGR2GRAY)

    # 处理滑块
    front = front[front.any(1)]

    # 匹配  图像匹配算法
    result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)  # 精度最高，速度最慢
    x, y = np.unravel_index(result.argmax(), result.shape)
    return y

def print_exception(e):
    
    print("Error '%s' happened on line %d" % (e[0], e[1][1]))