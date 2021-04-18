#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
import sqlite3
class dbManage():
	def __init__(self,dbName):
		self.dbName = str(dbName)
		self.dbItems = "(user,timealert,lat,lng)"
	def connect(self,tableName,user):
		self.tableName = str(tableName)
		self.user = user
		self.connecting = sqlite3.connect(self.dbName)
		self.cursor = self.connecting.cursor()
		return self.cursor
	def createUser(self):
		data = (self.user,120,"","")
		dbcomand = str("INSERT INTO {0} {1}  VALUES {2};".format(self.tableName,self.dbItems,data))
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def getTimer(self):
		dbcomand = " SELECT timealert FROM {0} WHERE user = {0};".format(self.tableName,self.user)
		self.cursor.execute(dbcomand)
		timealert = self.cursor.fetchall()
		return timealert
	def updateTimer(self,time):
		dbcomand = " UPDATE {0} SET timealert={1} WHERE user = {2};".format(self.tableName,time,self.user)
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def addLocation(self,loc):
		"""loc as list [lat, long] """
		dbcomand = " UPDATE {0} SET lat={1},lng={2} WHERE user = {3};".format(self.tableName,loc[0],loc[1],self.user)
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def disdableLocation(self):
		dbcomand = " UPDATE {0} SET lat={1},lng={2} WHERE user = {3};".format(self.tableName,"0","0",self.user)
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def addSensor(self,name):
		dbcomand = " UPDATE {0} SET sensorP={1} WHERE user = {2};".format(self.tableName,name,self.user)
		self.cursor.execute(dbcomand)
		self.cursor.connection.commit()
	def getSensorName(self):
		dbcomand = " SELECT sensorP FROM {0} WHERE user = {1};".format(self.tableName,self.user)
		self.cursor.execute(dbcomand)
		name = self.cursor.fetchall()
		return name

	