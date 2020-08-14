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
from help.tools import find_file, delete_path, get_mobileconfig_url,get_proxy_ip


# config = [
#     {'url': 'https://iosvipsign.site/install/798-75'},
# ]


def run():

    try:

        config_dit = config_data([{'url': 'https://798-1.com/79l-won-cfk/','click':'/html/body/div[1]/div[1]/div[1]/a[2]'}])

        if config_dit['proxy_ip'] != None and config_dit['xml'] != None :

            proxy_ip = config_dit['proxy_ip']
            mobileEmulation = {'deviceName': config_dit['deviceName']}
            prefs = {'download.default_directory': config_dit['downloadPath'], 'download.prompt_for_download': False}

            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument("--proxy-server=http://" + proxy_ip)
            chrome_options.add_argument('--ignore-certificate-errors')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--safebrowsing-disable-download-protection')
            chrome_options.add_argument('--safebrowsing-disable-extension-blacklist')
            chrome_options.add_experimental_option('mobileEmulation', mobileEmulation)
            chrome_options.add_experimental_option('prefs', prefs)
            chrome_options.add_experimental_option( 'excludeSwitches', ['enable-logging', 'enable-automation'])
            driver = webdriver.Chrome(options=chrome_options)
            driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': config_dit['downloadPath']}}
            driver.execute("send_command", params)
            driver.get(config_dit['url'])
            driver.implicitly_wait(1)

            driver.find_element_by_xpath(config_dit['click']).click()

            sleep(10)
            print(driver.current_url)
            cookies = driver.get_cookies()
            print(driver.get_cookies())
            driver.close()
            driver.quit()
            exit()

            ios_vip_sign_session = driver.get_cookie('ios_vip_sign_session')


            if len(ios_vip_sign_session['value']) <= 0:

                driver.close()
                driver.quit()

                return None

            config_dit['ios_vip_sign_session'] = 'ios_vip_sign_session='+ios_vip_sign_session['value']

            print('config',config_dit)
            proxy_ip = config_dit['proxy_ip']
            url = 'https://iosvipsign.site/build/798-75.ipa'
            xml = config_dit['xml']
            post_data = {
                "UDID": "",
                "appenddata": "",
                "device_name": "",
                "device_product": "",
                "device_version": ""
            }

            # 设置代理请求
            proxies = {"https": 'https://' + config_dit['proxy_ip']}
            # 设置请求头

            headers = {'Content-Type': 'application/json;charset=UTF-8','Cookie':config_dit['ios_vip_sign_session']}
            # 发起请求签名
            response = requests.post(url, data=post_data, headers=headers, proxies=proxies)

            print('mobileconfigUrl:',response.content)

            r = requests.get(response.content)
            with open('test.mobileconfig', 'wb') as f:
                f.write(r.content)

            # 读取mobileconfig文件的请求地址
            post_url = get_mobileconfig_url('test.mobileconfig')[0];
            print('配置文件的链接：',post_url)


            response = requests.post(post_url, data=xml, headers={'Content-Type': 'application/xml'}, proxies=proxies)

            print('发送XML响应URL',response.url)

            par = urllib.parse.urlparse(response.url)
            query = urllib.parse.parse_qs(par.query)

            post_data['UDID'] = query['UDID'][0]
            post_data['appenddata'] = '%7B%22ChannelInfo%22%3A%22%7C%7C798%7Chttps%3A%2F%2F798-1.com%2F79l-won-cfk%2F%7C1597372246636%7C2df93ad47a7451cdabfb5f4db9d1f6c8%22%2C%22test%22%3A%22hello%22%7D'
            post_data['device_product'] = query['DEVICE_PRODUCT'][0]
            post_data['device_version'] = query['DEVICE_VERSION'][0]

            headers['Connection'] = 'keep-alive'
            headers['Sec-Fetch-Dest'] = 'empty'
            headers['Sec-Fetch-Mode'] = 'cors'
            headers['Sec-Fetch-Site'] = 'same-origin'

            response_sign = requests.post(url, data=post_data, headers=headers, proxies=proxies)


            print("请求签名响应:", response_sign.content)


            driver.close()
            driver.quit()

            # return config_dit

    except (BaseException, Exception, ConnectionResetError, TypeError) as e:
        print('错误信息提示：%s'%e)


if __name__ == '__main__':
    run()
    exit()


    config_dit = config_data([{'url': 'https://iosvipsign.site/install/798-75'}])

    post_url = 'https://verify.iosvipsign.site/accept.php?app=NzV8JTdCJTIyQ2hhbm5lbEluZm8lMjIlM0ElMjIlN0MlN0M3OTglN0NodHRwcyUzQSUyRiUyRjc5OC0xLmNvbSUyRjc5bC13b24tY2ZrJTJGJTdDMTU5NzM5NjUzODcwMSU3QzRlYmMxYzJiOTg1YTk1ZmU2MGI5MTZhZDJlZGI5N2Y0JTIyJTJDJTIydGVzdCUyMiUzQSUyMmhlbGxvJTIyJTdE'
    proxies = {"https": 'https://' + config_dit['proxy_ip']}

    response = requests.post(post_url, data=config_dit['xml'], headers={'Content-Type': 'application/xml','Cookie':'cookie_udid=eyJpdiI6IlF6QzZrM2dxRUEvUkV3a3RZSHIrU1E9PSIsInZhbHVlIjoiK1crV1p4MW1kS1ZxalMvVFlCZVBwdz09IiwibWFjIjoiZDU4ZDM1MTU1YmJhM2I1NTA2ZTBiYjhmNmQ4YWUxNzY2NTg5MzA1NGM1ZjA5ZjI3MTYzNDQ0YzFhYTMwNzA5YiJ9; ios_vip_sign_session=eyJpdiI6Im1pOVI3UXlTcmNEclBLUFY3ZC9QREE9PSIsInZhbHVlIjoiaDhkVDBZYXBqbWVlTUEvTUNYL1ZQNDB6WWRFeE5OQU9mWlhlZ2xTZEY1eDVSVzZaOXRPN244dnRPRHdZL0NvKyIsIm1hYyI6IjMxMzRmYWUxNDE1YmMxNTAwOGYyOTE5MTMzMzVhOTZlZjZiMDU0NTM1MjJmZTJmMTM2ZjY5ZWUwOTUxYWEzZGEifQ%3D%3D'}, proxies=proxies)

    print('发送XML响应URL状态',response.status_code)
    print('发送XML响应URL',response.url)


    par = urllib.parse.urlparse(response.url)
    query = urllib.parse.parse_qs(par.query)
    post_data = {
        "UDID": "",
        "appenddata": "",
        "device_name": "",
        "device_product": "",
        "device_version": ""
    }
# {"ChannelInfo":"||798|https://798-1.com/79l-won-cfk/|1597396538701|4ebc1c2b985a95fe60b916ad2edb97f4"}

    post_data['UDID'] = query['UDID'][0]
    post_data['appenddata'] = '%7B%22ChannelInfo%22%3A%22%7C%7C798%7Chttps%3A%2F%2F798-1.com%2F79l-won-cfk%2F%7C1597396538701%7C4ebc1c2b985a95fe60b916ad2edb97f4%22%2C%22test%22%3A%22hello%22%7D'
    post_data['device_product'] = query['DEVICE_PRODUCT'][0]
    post_data['device_version'] = query['DEVICE_VERSION'][0]

    headers = {'Content-Type': 'application/json;charset=UTF-8','Cookie':'cookie_udid=eyJpdiI6IlF6QzZrM2dxRUEvUkV3a3RZSHIrU1E9PSIsInZhbHVlIjoiK1crV1p4MW1kS1ZxalMvVFlCZVBwdz09IiwibWFjIjoiZDU4ZDM1MTU1YmJhM2I1NTA2ZTBiYjhmNmQ4YWUxNzY2NTg5MzA1NGM1ZjA5ZjI3MTYzNDQ0YzFhYTMwNzA5YiJ9; ios_vip_sign_session=eyJpdiI6Im1pOVI3UXlTcmNEclBLUFY3ZC9QREE9PSIsInZhbHVlIjoiaDhkVDBZYXBqbWVlTUEvTUNYL1ZQNDB6WWRFeE5OQU9mWlhlZ2xTZEY1eDVSVzZaOXRPN244dnRPRHdZL0NvKyIsIm1hYyI6IjMxMzRmYWUxNDE1YmMxNTAwOGYyOTE5MTMzMzVhOTZlZjZiMDU0NTM1MjJmZTJmMTM2ZjY5ZWUwOTUxYWEzZGEifQ%3D%3D'}

    headers['Connection'] = 'keep-alive'
    headers['Sec-Fetch-Dest'] = 'empty'
    headers['Sec-Fetch-Mode'] = 'cors'
    headers['Sec-Fetch-Site'] = 'same-origin'

    response_sign = requests.post('https://iosvipsign.site/build/798-75.ipa', data=post_data, headers=headers, proxies=proxies)


    print("请求签名响应:", response_sign.content)