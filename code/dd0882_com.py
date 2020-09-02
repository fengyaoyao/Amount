#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import requests
import queue
import urllib3
import platform
import threading
import urllib.parse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
sys.path.append('../')
from help.config import config_data
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, get_dir, set_flow, get_system, wirteLog


def run():

    try:

        config_dit = config_data([{'url': 'https://dd0882.com/jk-asf-296/','click': '/html/body/div/div[2]/div/a[2]/img', 'install': '/html/body/div[2]/div/div[1]/div[2]/div[2]/div'}])

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

            if platform.system() == 'Linux':
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')

            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)

            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_file}}
            driver.execute("send_command", params)

            driver.get(config_dit['url'])

            WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, config_dit['click']))).click()
            WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="mobileconfig"]')))
            mobileconfig = driver.find_element_by_xpath('//*[@id="mobileconfig"]').get_attribute('value')
            post_url = mobileconfig.replace('getudid','receive').replace('http','https')
            print('配置文件链接:', post_url)

            if post_url is not None:

                proxies = {"https": 'https://' + proxy_ip}
                headers = {'Content-Type': 'application/xml'}
                response = requests.post(post_url, data=config_dit['xml'], headers=headers, proxies=proxies)
                print('发送XML响应URL状态', response.status_code)
                print('发送XML响应URL', response.url)
                driver.get(response.url)

                driver.implicitly_wait(2)
                WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[1]')))

                for x in range(1,100):
                    text = driver.find_element_by_xpath('//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[1]').text
                    print('安装动作:',text)
                    if text == '返回桌面查看':
                        wirteLog({'配置文件的链接:': post_url, '响应地址:': response.url, '安装动作:': text})
                        break
                    if text == '刷新重试!':
                        break
                    sleep(1)

            driver.quit()

    except (BaseException, Exception, ConnectionResetError, TypeError) as e:
        print('错误信息提示2：%s' % e)


def runThread():

    for i in range(1, 4):
        t = threading.Thread(target=run)
        t.start()
        sleep(2)


if __name__ == '__main__':
    runThread()
    # run()
