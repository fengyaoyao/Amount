#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
from apscheduler.schedulers.blocking import BlockingScheduler



def doupoclub_com():
    os.system('D:\\python381\\python.exe .\\doupoclub_com.py')


def iosvipsign_site():
    os.system('D:\\python381\\python.exe .\\iosvipsign_site.py')


def www_86scw_com():

	os.system('D:\\python381\\python.exe .\\www_86scw_com.py')

def ios_tkls365_com():
	os.system('D:\\python381\\python.exe .\\ios_tkls365_com.py')
	

if __name__ == '__main__':


	scheduler = BlockingScheduler()
	scheduler.add_job(doupoclub_com, 'interval', minutes=10,start_date='2020-09-01 09:38:00', end_date='2020-09-01 17:30:00',max_instances=3)
	scheduler.add_job(iosvipsign_site, 'interval', minutes=8,start_date='2020-09-01 09:38:00', end_date='2020-09-01 17:30:00',max_instances=3)
	scheduler.add_job(www_86scw_com, 'interval', minutes=6,start_date='2020-09-01 09:38:00', end_date='2020-09-01 17:30:00',max_instances=3)
	# scheduler.add_job(ios_tkls365_com, 'interval', minutes=5,start_date='2020-08-31 09:15:00', end_date='2020-08-31 17:30:00',max_instances=1)
	scheduler.start()

