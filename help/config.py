#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import random
import requests
from pathlib import Path
from help.tools import get_dir,get_proxy_ip,set_flow


# 配置信息
def config_data(configs):

    # 配置页面操作信息
    config = random.choice(configs)

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
