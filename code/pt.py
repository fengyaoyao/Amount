#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import cv2
import numpy as np
 
def show(name):
	cv2.imshow('Show', name)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
 
def main():
	otemp = '../file/hycdn2.png'
	oblk = '../file/hycdn.jpg'
	target = cv2.imread(otemp, 0)
	template = cv2.imread(oblk, 0)
	w, h = target.shape[::-1]
	temp = '../file/temp.jpg'
	targ = '../file/targ.jpg'
	cv2.imwrite(temp, template)
	cv2.imwrite(targ, target)
	target = cv2.imread(targ)
	target = cv2.cvtColor(target, cv2.COLOR_BGR2GRAY)
	target = abs(255 - target)
	cv2.imwrite(targ, target)
	target = cv2.imread(targ)
	# print(target)
	# exit()
	template = cv2.imread(temp)
	result = cv2.matchTemplate(target, template, cv2.TM_CCOEFF_NORMED)
	x, y = np.unravel_index(result.argmax(), result.shape)
	# 展示圈出来的区域
	cv2.rectangle(template, (y, x), (y + w, x + h), (7, 249, 151), 2)
	show(template)
 
if __name__ == '__main__':
	main()