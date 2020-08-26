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
from PIL import Image
from time import sleep
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
sys.path.append('../')
from help.config import config_data
from help.tools import find_file, delete_path, get_mobileconfig_url, get_proxy_ip, get_dir, set_flow,get_system



def get_img(driver):

    try:
        WebDriverWait(driver, 60, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdn1"]')))
        WebDriverWait(driver, 60, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="cdn2"]')))
        WebDriverWait(driver, 60, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tcaptcha_drag_button"]')))


        # 获取滑动块的当前初始化位置
        style = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]').get_attribute('style')
        default_px = re.compile(r'\d+\.?\d*').findall(style)[0]

        # 背景图
        bg_img_src = driver.find_element_by_xpath('//*[@id="cdn1"]').get_attribute('src')

        # 滑块
        front_img_src = driver.find_element_by_xpath('//*[@id="cdn2"]').get_attribute('src')

        with open("../file/bg.jpg",mode='wb') as f:
            f.write(requests.get(bg_img_src).content)

        with open("../file/front.jpg",mode='wb') as f:
            f.write(requests.get(front_img_src).content)

        otemp = '../file/front.jpg'
        oblk = '../file/bg.jpg'

        target = cv2.imread(otemp, 0)
        template = cv2.imread(oblk, 0)
        temp = 'temp.jpg'
        targ = 'targ.jpg'
        cv2.imwrite(temp, template)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
        target = abs(255 - target)
        cv2.imwrite(targ, target)
        target = cv2.imread(targ)
        template = cv2.imread(temp)
        result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
        x, y = np.unravel_index(result.argmax(), result.shape)

        print('default_px',default_px)

        xoffset = float(y)/2 - float(default_px)

        return xoffset

    except (Exception, NameError, ConnectionRefusedError) as e:

        print('错误信息提示：%s' % e)
        driver.quit()
        return None

def move_to(driver):

        try:

            xoffset = get_img(driver)
            if xoffset == None:
                driver.quit()
                return None

            print('xoffset',xoffset)

            WebDriverWait(driver, 60, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tcaptcha_drag_button"]')))
            WebDriverWait(driver, 60, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tcaptcha_note"]')))

            div = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')
            ActionChains(driver).drag_and_drop_by_offset(div,xoffset=xoffset ,yoffset=0).perform()
        except (Exception, NameError, ConnectionRefusedError) as e:

            print('错误信息提示：%s' % e)
            driver.quit()
            return None
                
        sleep(4)

        try:

            tcaptcha_note = driver.find_element_by_xpath('//*[@id="tcaptcha_note"]').text
            if tcaptcha_note == '请控制拼图块对齐缺口':
                div = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]')
                ActionChains(driver).drag_and_drop_by_offset(div,xoffset=xoffset ,yoffset=0).perform()
            
        except Exception as e:
            pass



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
            print(config_dit)
            mobileEmulation = {'deviceName': config_dit['deviceName']}
            prefs = {'download.default_directory': download_file,
                     'download.prompt_for_download': False}

            chrome_options = webdriver.ChromeOptions()
            # chrome_options.add_argument('--headless')
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
            params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': download_file}}
            driver.execute("send_command", params)


            udid_dit = re.compile(r'(?<=<key>UDID</key><string>)(.*?)(?=</string>)').findall(config_dit['xml'])

            loading_page_url = 'https://down.8iosapp.com/5KZD.app?udid=' + udid_dit[0]

            print(loading_page_url)
            driver.get(loading_page_url)

            try:
                WebDriverWait(driver, 30, 0.5).until(EC.presence_of_element_located((By.XPATH, '//*[@id="tcaptcha_iframe"]')))
                iframe = driver.find_element_by_id("tcaptcha_iframe")
                driver.switch_to.frame(iframe);
            except (Exception, NameError, ConnectionRefusedError) as e:
                print('错误信息提示：%s' % e)
                driver.quit()
                return None

            sleep(3)
            # driver.execute_script("function startReq(ticket,randStr) {localStorage.setItem('ticket', ticket);localStorage.setItem('randstr', randstr);}")
            move_to(driver)
            # for x in range(1,50):
            # downloadId = driver.execute_script("return window.localStorage.getItem('downloadId');")
            # print('downloadId',downloadId)
            #     sleep(1)
            # try:
            #     for x in range(1,10):
            #         tcaptcha_note = driver.find_element_by_xpath('//*[@id="tcaptcha_note"]').text
            #         if len(tcaptcha_note) > 0:
            #             break
            #         sleep(1)

            #     print('tcaptcha_note',tcaptcha_note)
            #     if tcaptcha_note == '这题有点难呢，已为您更换题目':
            #         move_to(driver)
            # except Exception as e:
            #     print('错误信息提示：%s' % e)


            driver.switch_to.parent_frame()
            for x in range(1,80):
                text = driver.find_element_by_xpath('//*[@id="xzzz"]').text
                print('安装动作：',text)
                if text == '下载异常':
                    break
                if text == '完成':
                    break
                if text == '安装':
                    break
                sleep(1)

            driver.quit()

if __name__ == '__main__':
    run()