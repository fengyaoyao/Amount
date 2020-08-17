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
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, get_dir, set_flow,get_system,wirteLog


def run():

    try:

        config_dit = config_data([{'url': 'https://798-1.com/79l-won-cfk/',
                                   'click': '/html/body/div[1]/div[1]/div[1]/a[2]', 'install': '//*[@id="install-btn"]'}])

        if config_dit['proxy_ip'] != False and config_dit['xml'] != False:

            if get_system() == 'Windows':
                
                download_file = get_dir() + '\\download\\' + set_flow()
            else:
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

            for x in range(1, 10):
                download_file_name = find_file(download_file)
                if download_file_name:
                    break
                sleep(1)

            post_url = None
            if download_file_name:

                if get_system() == 'Windows':
                    path_mobileconfig = download_file + '\\' + download_file_name
                else:
                    path_mobileconfig = download_file + '/' + download_file_name

                mobileconfig_url = get_mobileconfig_url(path_mobileconfig)
                post_url = mobileconfig_url[0]

            print('当前页面URL地址:', driver.current_url)
            print('Cookie:', cookie)
            print('配置文件链接:', post_url)

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
                        wirteLog(text)
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


            driver.quit()

    except (BaseException, Exception, ConnectionResetError, TypeError) as e:
        print('错误信息提示：%s' % e)


if __name__ == '__main__':
    run()