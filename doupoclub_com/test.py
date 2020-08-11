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
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, set_flow, wirteLog


def runs():

    proxy_ip = get_proxy_ip()
    print('代理地址:', proxy_ip)

    autofile = set_flow()

    download_path = '..' + '/download/' + autofile

    mobileEmulation = {'deviceName': 'iPhone X'}
    prefs = {'download.default_directory': download_path,
             'download.prompt_for_download': False}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument("--proxy-server=http://" + proxy_ip)
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        '--safebrowsing-disable-download-protection')
    chrome_options.add_argument(
        '--safebrowsing-disable-extension-blacklist')
    chrome_options.add_experimental_option(
        'mobileEmulation', mobileEmulation)
    chrome_options.add_experimental_option('prefs', prefs)
    chrome_options.add_experimental_option(
        'excludeSwitches', ['enable-logging', 'enable-automation'])

    driver = webdriver.Chrome(options=chrome_options)

    driver.command_executor._commands["send_command"] = (
        "POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {
        'behavior': 'allow', 'downloadPath': download_path}}
    driver.execute("send_command", params)

    driver.get('https://www.86scw.com/s/fUdM')
    driver.implicitly_wait(1)
    url = driver.find_element_by_xpath(
        '//*[@id="mobileconfig"]').get_attribute('value')

    proxies = {"http": 'http://' + proxy_ip}

    mobileconfig = requests.get(url, proxies=proxies)

    mobileconfig_file = '../file/' + set_flow() + ".mobileconfig"

    with open(mobileconfig_file, "wb") as code:
        code.write(mobileconfig.content)

    post_url = get_mobileconfig_url(mobileconfig_file)[0]

    # 获取XML
    xml = requests.get('http://104.243.25.81/web/user/getUdidXml').text
    print('配置文件的链接：', post_url)
    print('获取XML:' + xml)

    if os.path.exists(mobileconfig_file):
        os.remove(mobileconfig_file)

    headers = {'Content-Type': 'application/xml'}

    try:
        # 发送XML进行签名
        response = requests.post(
            post_url, data=xml, headers=headers, proxies=proxies)
        print("响应状态:", response.status_code)
        print('响应地址:', response.url)

        driver.get(response.url)

        driver.implicitly_wait(5)
        text = driver.find_element_by_xpath(
            '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[1]').text
        print('安装动作:', text)

        wirteLog({'配置文件的链接:': post_url, '响应地址:': response.url, '安装动作:': text})
        driver.close()
        driver.quit()

    except Exception as e:
        print(e)
        driver.close()
        driver.quit()

xx = 0
while xx < 11:

    for i in range(1, 10):
        t = threading.Thread(target=runs)
        t.start()
        sleep(3)

    xx = xx + 1
