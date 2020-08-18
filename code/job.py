#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler

scheduler = BlockingScheduler()


def doupoclub_com():
    os.system('python ./doupoclub_com.py')


def iosvipsign_site():
    os.system('python ./iosvipsign_site.py')


def www_86scw_com():
    os.system('python ./www_86scw_com.py')


scheduler.add_job(doupoclub_com, 'interval', minutes=4,
                  start_date='2020-08-18 10:45:00', end_date='2020-08-18 13:00:00', max_instances=3)
scheduler.add_job(iosvipsign_site, 'interval', minutes=8,
                  start_date='2020-08-18 10:46:00', end_date='2020-08-18 13:00:00', max_instances=3)
scheduler.add_job(www_86scw_com, 'interval', minutes=6,
                  start_date='2020-08-18 10:47:00', end_date='2020-08-18 13:00:00', max_instances=3)
scheduler.start()
