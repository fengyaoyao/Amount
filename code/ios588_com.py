#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import json
import queue
import urllib3
import platform
import requests
import threading
import urllib.parse
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


    config_dit = config_data([{'url':'http://fff.xingshuo2005.com/v/awgda7'}])

    if config_dit['proxy_ip'] != False and config_dit['xml'] != False:

        proxy_ip = config_dit['proxy_ip']
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
        chrome_options.add_argument('--safebrowsing-disable-download-protection')
        chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
        chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        driver = webdriver.Chrome(options=chrome_options)

        try:
            driver.get(config_dit['url'])
            WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="download"]')))

        except (Exception, NameError, NoSuchElementException,TimeoutException, ConnectionRefusedError, urllib3.exceptions.NewConnectionError) as e:
            print('错误信息提示1：%s' % e)
            driver.quit()
            return None

        try:
            # 发送XML进行签名
            proxies = {"http": 'http://' + proxy_ip,"https": 'https://' + proxy_ip}
            response = requests.post('https://ios588.com/source/index/receive.php/awgda7', data=config_dit['xml'] , headers={'Content-Type': 'application/xml'}, proxies=proxies)
        except (Exception, requests.exceptions.TooManyRedirects) as e:

            print('错误信息提示2：%s' % e)
            driver.quit()
            return None
           
        print('xml响应地址',response.url)

        cookie = {
            'PHPSESSID':driver.get_cookie('PHPSESSID')['value'],
            'Hm_lpvt_7b09e6c5f34e073b4d5e074abff16797':driver.get_cookie('Hm_lpvt_7b09e6c5f34e073b4d5e074abff16797')['value'],
            'Hm_lvt_7b09e6c5f34e073b4d5e074abff16797':driver.get_cookie('Hm_lvt_7b09e6c5f34e073b4d5e074abff16797')['value'],
        }

        headers = {
            'Accept': 'text/plain, */*; q=0.01',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'Referer': response.url,
            'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
            'X-Requested-With': 'XMLHttpRequest',
        }

        par = urllib.parse.urlparse(response.url)
        query = urllib.parse.parse_qs(par.query)
        proxies = {"http": 'http://' + proxy_ip,"https": 'https://' + proxy_ip}
        url = 'http://rpxfxhr2nz83fe2s92xfj39lob9mhaq5mvb5o2o8qzoux018q6.url.ios588.com/source/index/ajax_vipsign.php?in_id=MDAwMDAwMDAwMIKqyJY&udid='+ query['UDID'][0] +'&ac=signvip&knameid='

        result = requests.get(url, headers=headers, proxies=proxies, cookies=cookie)
        print(result.content)
        signvip_result = eval(result.content)
        if eval(result.content)['status'] != '1':
            driver.quit()
            exit()

        for x in range(1,40):

            url = 'http://rpxfxhr2nz83fe2s92xfj39lob9mhaq5mvb5o2o8qzoux018q6.url.ios588.com/source/index/ajax_vipsign.php?in_id=MDAwMDAwMDAwMIKqyJY&udid='+ query['UDID'][0] +'&ac=checkvipsign&knameid='
            result2 = requests.get(url, headers=headers, proxies=proxies, cookies=cookie)
            data = eval(result2.content)
            print(data)
            if data['status'] =='-13':
                break

            if data['status'] =='2' and data['step'] == 'success':

                header = {
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9',
                    'Connection': 'keep-alive',
                    'Cookie': 'Hm_lvt_7b09e6c5f34e073b4d5e074abff16797=' + cookie['Hm_lvt_7b09e6c5f34e073b4d5e074abff16797'] + '; ' + 'PHPSESSID=' + cookie['PHPSESSID'] + '; ' + 'Hm_lpvt_7b09e6c5f34e073b4d5e074abff16797=' + cookie['Hm_lpvt_7b09e6c5f34e073b4d5e074abff16797'],
                    'Referer': response.url,
                    'Upgrade-Insecure-Requests': '1',
                    'User-Agent':'Mozilla/5.0 (iPhone; CPU iPhone OS 6_0 like Mac OS X) AppleWebKit/536.26 (KHTML, like Gecko) Version/6.0 Mobile/10A5376e Safari/8536.25',
                }
                print(header)
                url2 = 'http://r9e3mowwxkvtn9kkb2fuvcck7oq852tee75hw2efj96f7os6x9.url.ios588.com/source/pack/upload/install/installSign.php?id=MDAwMDAwMDAwMIKqyJY&udid='+ query['UDID'][0]
                result3 = requests.get(url2, headers=header, proxies=proxies)
                print(result3.status_code)
                print(result3.text)
                print(result3.url)
                print(result3.history)

                break
            sleep(1)

        driver.quit()


def runThread():

    for i in range(1, 10):
        t = threading.Thread(target=runs)
        t.start()
        sleep(2)
    
if __name__ == '__main__':
    runs()
    # runThread()