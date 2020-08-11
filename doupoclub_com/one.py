#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import queue
import platform
import threading
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


# 获取配置文件写入队列
def make_config():
    for i in range(1, 3):
        r = config_data(config)
        q.put(r)
        sleep(0.1)


def run(n):

    config_dit = q.get()

    if config_dit['proxy_ip'] != None && config_dit['xml'] != None:
        
        proxy_ip = config_dit['deviceName']
        mobileEmulation = {'deviceName': config_dit['deviceName']}
        prefs = {'download.default_directory': config_dit['downloadPath'],'download.prompt_for_download': False}

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument("--proxy-server=http://" + proxy_ip)
        chrome_options.add_argument('--ignore-certificate-errors')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--safebrowsing-disable-download-protection')
        chrome_options.add_argument("--safebrowsing-disable-extension-blacklist")
        chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
        chrome_options.add_experimental_option('prefs', prefs)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])

        driver = webdriver.Chrome(options=chrome_options)

        driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
        params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': config_dit['downloadPath']}}
        driver.execute("send_command", params)

        try:
            driver.get(config_dit['url'])
            driver.implicitly_wait(1)

            if config_dit['frist_is_iframe'] == 'True':
                iframe = driver.find_element_by_tag_name("iframe")
                driver.switch_to.frame(iframe)

            driver.find_element_by_xpath(config_dit['click']).click()
            driver.implicitly_wait(1)

            if len(config_dit['localStorage']) == 2:
                JS = "window.localStorage.setItem('" + config_dit['localStorage'][0] + "','" + config_dit['localStorage'][1] + "');"
                driver.execute_script(JS)
                driver.refresh()

            driver.find_element_by_xpath(config_dit['installation']).click()
            driver.implicitly_wait(1)

        except Exception as e:
            print(e)
            driver.close()
            driver.quit()

        for x in range(1, 10):
            download_file_name = find_file(config_dit['downloadPath'])
            if download_file_name:
                break
            sleep(1)

        post_url = ''
        if download_file_name:
            path_mobileconfig = config_dit['downloadPath'] + '/' + download_file_name
            mobileconfig_url = get_mobileconfig_url(path_mobileconfig)
            post_url = mobileconfig_url[0]

        # 配置代理ip
        proxies = {
            "http": 'http://' + proxy_ip,
            "https": 'https://' + proxy_ip,
        }

        headers = {'Content-Type': 'application/xml'}

        try:
            # 发送XML进行签名
            response = requests.post(post_url, data=config_dit['xml'], headers=headers, proxies=proxies)
            print("响应状态:", response.status_code)
            print('响应地址:', response.url)

            # 加载签名后返回的地址
            install_response = driver.get(response.url)

        except Exception as e:
            print(e)
            driver.close()
            driver.quit()
            continue








if __name__ == '__main__':
    q = queue.Queue()
    t2 = threading.Thread(target=make_config)
    t2.start()
    for i in range(1, 3):
        t = threading.Thread(target=run, args=(i,))
        t.start()