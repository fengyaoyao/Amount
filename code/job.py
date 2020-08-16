#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def my_job():
    # print(text)
    os.system('/Library/Frameworks/Python.framework/Versions/3.8/bin/python3.8  /Users/mac/www/Amount/code/doupoclub_com.py')

# datetime类型（用于精确时间）
scheduler.add_job(my_job, 'interval', minutes=8,
                  start_date='2020-08-16 17:20:00', end_date='2020-08-16 18:00:00')

scheduler.start()
