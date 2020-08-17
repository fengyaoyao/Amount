#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def doupoclub_com():
    # print(text)
    os.system('python ./doupoclub_com.py')

def iosvipsign_site():
    os.system('python ./iosvipsign_site.py')

def my_job():
    os.system('python  ./test.py')
	
	
# datetime类型（用于精确时间）
# scheduler.add_job(my_job, 'interval', minutes=1,start_date='2020-08-17 09:24:00', end_date='2020-08-17 09:30:00')
# scheduler.add_job(doupoclub_com, 'interval', minutes=4,start_date='2020-08-17 10:15:00', end_date='2020-08-17 12:00:00',max_instances=10)
scheduler.add_job(iosvipsign_site, 'interval', minutes=8,start_date='2020-08-17 15:05:00', end_date='2020-08-17 16:30:00',max_instances=1)
scheduler.start()
