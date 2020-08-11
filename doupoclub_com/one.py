#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
from time import sleep
from selenium import webdriver
sys.path.append('../')
from help.config import config_data
from help.tools import find_file,delete_path,get_mobileconfig_url


config = [
    {'url': 'https://yd8.vip/', 'click': '/html/body/div[1]/div/div/a', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'False', 'localStorage': ['5ee205a1f1670ischeck', 'true']},

    {'url': 'https://qp911.cc/', 'click': '//*[@id="bgtype2_download"]/section/img[1]', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'True', 'localStorage': ['5f218a85bbda7ischeck', 'true']},

    {'url': 'https://26x.com/', 'click': '/html/body/section/div[2]/div[1]/img[2]', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'True', 'localStorage': ['5ee210d78a135ischeck', 'true']},

    {'url': 'http://yinniu66.com/', 'click': '//*[@id="download2"]', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'False', 'localStorage': ['5f046d0dbbcabischeck', 'true']},

    {'url': 'https://01606.cc/', 'click': '/html/body/div[1]/div/div/a/img[1]', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'False', 'localStorage': ['5ee2126bd1ca6ischeck', 'true']},

    {'url': 'https://58yh.cc/', 'click': '/html/body/div[1]/a', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'True', 'localStorage': ['5ee210d78a135ischeck', 'true']},

    {'url': 'https://dfl6.cc/', 'click': '//*[@id="bgtype2_download"]/img', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'True', 'localStorage': ['5efdc065c1bdcischeck', 'true']},
    {'url': 'https://wtz01.vip/', 'click': '/html/body/section/div[2]/img', 'installation': '//*[@id="xzzz"]',
        'frist_is_iframe': 'True', 'localStorage': ['5ef5bbccb0ce6ischeck', 'true']},
]


# 创建一个队列
# 加入配置信息到队列

# 创建多个线程
# 每个线程从队列里获取配置信息进行运行
print(config_data(config))