#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import queue
import platform
import threading
import urllib.parse
from time import sleep
from selenium import webdriver
sys.path.append('../')
from help.config import config_data
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, get_dir, set_flow


def run():

    try:

        config_dit = config_data([{'url': 'https://798-1.com/79l-won-cfk/',
                                   'click': '/html/body/div[1]/div[1]/div[1]/a[2]', 'install': '//*[@id="install-btn"]'}])

        if config_dit['proxy_ip'] != False and config_dit['xml'] != False:

            download_file = get_dir() + '/download/' + set_flow()

            proxy_ip = config_dit['proxy_ip']
            print('代理IP', proxy_ip)

            mobileEmulation = {'deviceName': config_dit['deviceName']}
            prefs = {'download.default_directory': download_file,
                     'download.prompt_for_download': False}

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--proxy-server=http://" + proxy_ip)
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument(
                '--safebrowsing-disable-download-protection')
            chrome_options.add_argument(
                "--safebrowsing-disable-extension-blacklist")
            chrome_options.add_experimental_option(
                'mobileEmulation', mobileEmulation)
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_experimental_option(
                'excludeSwitches', ['enable-logging', 'enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)

            driver.command_executor._commands["send_command"] = (
                "POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {
                'behavior': 'allow', 'downloadPath': download_file}}
            driver.execute("send_command", params)

            driver.get(config_dit['url'])
            driver.implicitly_wait(1)
            driver.find_element_by_xpath(config_dit['click']).click()
            driver.implicitly_wait(1)
            driver.find_element_by_xpath(config_dit['install']).click()
            driver.implicitly_wait(1)

            cookie = driver.get_cookie('ios_vip_sign_session')

            for x in range(1, 8):
                download_file_name = find_file(download_file)
                if download_file_name:
                    break
                sleep(1)

            post_url = None
            if download_file_name:
                path_mobileconfig = download_file + '/' + download_file_name
                mobileconfig_url = get_mobileconfig_url(path_mobileconfig)
                post_url = mobileconfig_url[0]

            print('当前页面URL地址:', driver.current_url)
            print('Cookie:', cookie)
            print('配置文件链接:', post_url)
            delete_path(download_file)

            if post_url is not None:

                proxies = {"https": 'https://' + proxy_ip}
                headers = {'Content-Type': 'application/xml'}
                response = requests.post(post_url, data=config_dit[
                                         'xml'], headers=headers, proxies=proxies)
                print('发送XML响应URL状态', response.status_code)
                print('发送XML响应URL', response.url)
                driver.get(response.url)
                driver.implicitly_wait(2)

                status = True
                while status:
                    text = driver.find_element_by_xpath(
                        config_dit['install']).text
                    print(text)
                    if text == '正在下载中...' or text == '再试一次' or text == '网络错误':
                        status = False
                        break
                    sleep(1)

        # par = urllib.parse.urlparse(driver.current_url)
        # data = urllib.parse.parse_qs(par.query)

        # post_data = {
        #     'appenddata': data['appenddata'][0],
        #     'UDID': '',
        #     'device_name': '',
        #     'device_product': '',
        #     'device_version': ''
        # }

        # headers = {
        #     'Content-Type': 'application/json;charset=UTF-8',
        #     'Cookie': 'ios_vip_sign_session=' + cookie['value'],
        #     'Referer': driver.current_url,
        #     'Sec-Fetch-Dest': 'empty',
        #     'Sec-Fetch-Mode': 'cors',
        #     'Sec-Fetch-Site': 'same-origin',
        # }

        # proxies = {"https": 'https://' + config_dit['proxy_ip']}

        # response = requests.post('https://iosvipsign.site/build/798-75.ipa',
        # data=post_data, headers=headers, proxies=proxies)

        # print('响应内容:', response.content)
        # print('响应URL:', response.url)

        # r = requests.get(response.content)
        # with open('./test.mobileconfig', 'wb') as f:
        #     f.write(r.content)

        # mobileconfig_url = get_mobileconfig_url('./test.mobileconfig')
        # print('文件URL:', mobileconfig_url)

        driver.close()
        driver.quit()

    except (BaseException, Exception, ConnectionResetError, TypeError) as e:
        driver.close()
        driver.quit()
        print('错误信息提示：%s' % e)


if __name__ == '__main__':
    run()
    exit()
    for x in range(1, 20):

        config_dit = config_data(
            [{'url': 'https://iosvipsign.site/install/798-75'}])

        post_url = 'https://verify.iosvipsign.site/accept.php?app=NzV8JTdCJTIyQ2hhbm5lbEluZm8lMjIlM0ElMjIlN0MlN0M3OTglN0NodHRwcyUzQSUyRiUyRjc5OC0xLmNvbSUyRjc5bC13b24tY2ZrJTJGJTdDMTU5NzQ5OTQxNTYxNiU3Q2Q5MzdhMjE0ODllZTJjMzc1NjdmYzQxMTc1MzI0YmUyJTIyJTJDJTIydGVzdCUyMiUzQSUyMmhlbGxvJTIyJTdE'
        proxies = {"https": 'https://' + config_dit['proxy_ip']}

        response = requests.post(post_url, data=config_dit['xml'], headers={
                                 'Content-Type': 'application/xml'}, proxies=proxies)

        print('发送XML响应URL状态', response.status_code)
        print('发送XML响应URL', response.url)
        sleep(1)

    exit()

    mobileEmulation = {'deviceName': config_dit['deviceName']}
    prefs = {'download.default_directory': config_dit[
        'downloadPath'], 'download.prompt_for_download': False}

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(
        "--proxy-server=http://" + config_dit['proxy_ip'])
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
        'behavior': 'allow', 'downloadPath': config_dit['downloadPath']}}
    driver.execute("send_command", params)
    driver.get(response.url)

    for x in range(1, 7):

        text = driver.find_element_by_xpath('//*[@id="install-btn"]').text
        print(text)
        if len(text) == 8:
            break
        if text == '再试一次':
            break
        sleep(20)

    driver.close()
    driver.quit()
    exit()

    par = urllib.parse.urlparse(response.url)
    query = urllib.parse.parse_qs(par.query)
    post_data = {
        "UDID": "",
        "appenddata": "",
        "device_name": "",
        "device_product": "",
        "device_version": ""
    }
    post_data['UDID'] = query['UDID'][0]
    post_data[
        'appenddata'] = ''
    post_data['device_product'] = query['DEVICE_PRODUCT'][0]
    post_data['device_version'] = query['DEVICE_VERSION'][0]

    headers = {'Content-Type': 'application/json;charset=UTF-8', 'Cookie': 'os_vip_sign_session=eyJpdiI6IjZIVHM3MzhtUjNub2REQmNMRXNHMUE9PSIsInZhbHVlIjoiQWN2QVJkcERiRFcwaTBTYVVXcUR5TzdYakdiTlB5dlp5OFJEUjRrUTlza1lMcHNkR1EzVGltMWx3SDlleEk1WCIsIm1hYyI6IjdjNTFmNzNhZDYzNTYwZTdhZWY4MGZmMTYwZWJkNjk4NjE1OGUyNDc0NWUyZGE0ZjQ5MDBjYWZiOGVhYzIzMDEifQ%3D%3D'}

    headers['Connection'] = 'keep-alive'
    headers['Sec-Fetch-Dest'] = 'empty'
    headers['Sec-Fetch-Mode'] = 'cors'
    headers['Sec-Fetch-Site'] = 'same-origin'

    response_sign = requests.post(
        'https://iosvipsign.site/build/798-75.ipa', data=post_data, headers=headers, proxies=proxies)

    print("请求签名响应:", response_sign.content)
