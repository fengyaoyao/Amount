#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys
import cv2
import requests
import queue
import platform
import threading
import numpy as np
import urllib.parse
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
sys.path.append('../')
from help.config import config_data
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, get_dir, set_flow,get_system


def run():

    # try:

        config_dit = config_data([{'url': 'https://dzc5.cc/','click': '//*[@id="down_btn"]', 'install': '//*[@id="xzzz"]','iframe':'True'}])

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
            # chrome_options.add_argument('--headless')
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
            driver.set_window_size(400,920)

            udid_dit = re.compile(r'(?<=<key>UDID</key><string>)(.*?)(?=</string>)').findall(config_dit['xml'])

            loading_page_url = 'https://down.8iosapp.com/5KZD.app?udid=' + udid_dit[0]

            driver.get(loading_page_url)

            driver.implicitly_wait(2)
            sleep(10)


            iframe = driver.find_element_by_xpath('//*[@id="tcaptcha_iframe"]')
                
            driver.switch_to.frame(iframe)

            # 背景图
            bg_img_src = driver.find_element_by_xpath('//*[@id="slideBg"]').get_attribute('src')

            # 滑块
            front_img_src = driver.find_element_by_xpath('//*[@id="slideBlock"]').get_attribute('src')


            with open("bg.jpg",mode='wb') as f:
                f.write(requests.get(bg_img_src).content)

            with open("front.jpg",mode='wb') as f:
                f.write(requests.get(front_img_src).content)

            import numpy as np

            bg = cv2.imread('bg.jpg')
            front = cv2.imread("front.jpg")


            # 灰度处理
            bg = cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
            front = cv2.cvtColor(front,cv2.COLOR_BGR2GRAY)


            # 处理滑块
            front = front[front.any(1)]

            #匹配  图像匹配算法
            result = cv2.matchTemplate(bg,front,cv2.TM_CCOEFF_NORMED) # 精度最高，速度最慢

            x,y = np.unravel_index(np.argmax(result),result.shape)
            div = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')

            # 获取滑动块的当前位置
            style = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]').get_attribute('style')
            left = re.compile(r'\d+\.?\d*').findall(style)[0] 
            print('滑块位置',left)
            print('移动的位置',y)

            ActionChains(driver).drag_and_drop_by_offset(div,xoffset=y ,yoffset=0).perform()







            # if config_dit['iframe'] == 'True':
            #     iframe = driver.find_element_by_tag_name("iframe")
            #     driver.switch_to.frame(iframe)
            # driver.find_element_by_xpath(config_dit['click']).click()
            # driver.implicitly_wait(1)
            # driver.find_element_by_xpath(config_dit['install']).click()
            # driver.implicitly_wait(1)
            # cookie = driver.get_cookie('udid')
            # post_url = 'https://down.8iosapp.com/download/report/5KZD'

            # print('当前页面URL地址:', driver.current_url)
            # print('Cookie:', cookie)
            # print('配置文件链接:', post_url)



            # proxies = {"https": 'https://' + proxy_ip}
            # headers = {'Content-Type': 'application/xml'}
            # response = requests.post(post_url, data=config_dit[
            #                          'xml'], headers=headers, proxies=proxies)
            # print('发送XML响应URL状态', response.status_code)
            # print('发送XML响应URL', response.url)
            # driver.get(response.url)
            # driver.implicitly_wait(2)
            sleep(30)

            # status = True
            # while status:
            #     text = driver.find_element_by_xpath(
            #         config_dit['install']).text
            #     print(text)
            #     if text == '正在下载中...' or text == '再试一次' or text == '网络错误':
            #         status = False
            #         break
            #     sleep(1)

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

    # except (BaseException, Exception, ConnectionResetError, TypeError) as e:
    #     print('错误信息提示：%s' % e)


if __name__ == '__main__':
    run()