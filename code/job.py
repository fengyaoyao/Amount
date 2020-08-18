#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def my_job():
    # print(text)
    os.system('/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8  /Users/mac/www/Amount/code/iosvipsign_site.py')

# datetime类型（用于精确时间）
scheduler.add_job(my_job, 'interval', minutes=3,
                  start_date='2020-08-17 22:35:00', end_date='2020-08-17 23:59:00')

scheduler.start()
