#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
def timer(time,timedata):
	""" timer(time,timedata)
	time integer amount 
	timeUnits hours,minutes,seconds
	like "h","m","s"
	"""	
	from time import sleep 
	if timedata == "h": time *=60*60
	if timedata == "m": time *=60
	else: timeAmount = time 
	sleep(time)
def readtxtline(name):
	with open(name, 'r') as file:
		return str(file.readline())