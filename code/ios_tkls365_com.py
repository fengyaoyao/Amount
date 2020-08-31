#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import queue
import urllib3
import platform
import requests
import threading
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
sys.path.append('../')
from help.config import config_data
from help.tools import  wirteLog,get_dir,get_system


def runs():


    config_dit = config_data([{'url':'https://ios.tkls365.com/user/install/get_udid?app_id=2711', 'install': '//*[@id="app"]/div/div[1]/div[2]/div[2]/div/div[1]'}])

    if config_dit['proxy_ip'] != False and config_dit['xml'] != False:

        proxy_ip = config_dit['proxy_ip']
        proxies = {"http": 'http://' + proxy_ip,"https": 'https://' + proxy_ip}

        # 发送XML进行签名
        headers = {'Content-Type': 'application/xml'}

        try:
            response = requests.post(config_dit['url'], data=config_dit['xml'] , headers=headers, proxies=proxies)
        except (Exception, requests.exceptions.TooManyRedirects) as e:
            print('错误信息提示：%s' % e)
            return None
           
        loading_page_url =  response.url
        print("响应状态:", response.status_code)
        print('响应地址:', response.url)

        if loading_page_url:

            mobileEmulation = {'deviceName': config_dit['deviceName']}
            chrome_options = webdriver.ChromeOptions()
            # 浏览器不提供可视化页面
            chrome_options.add_argument('--headless')
            # 设置代理
            chrome_options.add_argument('--proxy-server=http://' + proxy_ip)
            # 忽略不信任证书
            chrome_options.add_argument('--ignore-certificate-errors')
            # 禁用GPU加速
            chrome_options.add_argument('--disable-gpu')

            if platform.system() == 'Linux':
                chrome_options.add_argument('--no-sandbox')
                chrome_options.add_argument('--disable-dev-shm-usage')
                
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
            chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)

            try:
                driver.set_page_load_timeout(30)
                driver.get(loading_page_url)
                driver.implicitly_wait(2)
                WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/div[1]/div[2]/div[2]/div')))
                WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="j-install-ipa"]')))
            except (Exception, NameError, NoSuchElementException,TimeoutException, ConnectionRefusedError, urllib3.exceptions.NewConnectionError) as e:
                print('错误信息提示：%s' % e)
                driver.quit()
                return None


            plist =driver.find_element_by_xpath('//*[@id="j-install-ipa"]').get_attribute('href')

            print('plist文件:',plist)

            wirteLog({'xml_response_url':loading_page_url,'plist_file_url':plist})
            driver.quit()


def runThread():

    for i in range(1, 10):
        t = threading.Thread(target=runs)
        t.start()
        sleep(2)
    
if __name__ == '__main__':
    runs()
    # runThread()
    # print('pass')