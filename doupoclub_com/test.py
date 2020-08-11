#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import requests
from pathlib import Path
from tools import get_dir,get_system,get_proxy_ip,set_flow,find_file,delete_path,get_mobileconfig_url,wirteLog,get_move_coordinates



def config_data():

    # 配置页面操作信息
    config = random.choice([
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
    ])

    # 配置设备名称
    deviceName = random.choice([
        "iPhone 6/7/8",
        "iPhone 6/7/8 Plus",
        "iPhone 5/SE",
        "iPhone X",
    ])

    config['deviceName'] = deviceName

    try:
        # 获取代理IP
        proxy_ip = get_proxy_ip()

        if proxy_ip:
            config['proxy_ip'] = proxy_ip
    except Exception as e:
        config['proxy_ip'] = None
        
    try:
        
        # 获取XML
        xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text

        if xml:
            config['xml'] = xml
    except Exception as e:
        config['xml'] = None


    autofile = set_flow()

    download_path = '..' + '/download/' + autofile

    if  Path(download_path).exists() == False:
        os.mkdir(download_path)

    config['downloadPath'] = download_path


    return config
