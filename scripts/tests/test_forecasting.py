#asin(x)+bcos(x)+c
"""
alpha = a/(a**2+b**2)**(1/2)
beta = b/(a**2+b**2)**(1/2)
 =
nota experiementos
{0,2}, {1,0.5}, {2,0}, {3,1}, {4,1.5}, {5,2}, {6,1.5}, {7,2}, {8,0.5}, {9,0}, {10,0.5}, {11,2}, {12,1}, {13,1.6666666666666667}, {14,1}
-0.52313*sin(x)+0.576513*cos(x)+1.13258
"""
from influxdb import InfluxDBClient
import json
import numpy as np
class aqa:
	host = "aqa.unloquer.org"
	client = InfluxDBClient(host=host, port=8086)
	def __init__(self,db):
		self.db = db
	def namesAQA(self):
		names = self.client.query('SHOW MEASUREMENTS ON "'+self.db+'"').raw
		clearNames = eval(str(names)[88:-4])
		return names
	def data(self,name,dataAQA = "pm25"):
		q = self.client.query('SELECT mean("'+dataAQA+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE time > now() - 5h GROUP BY time(10s) FILL(none)')
		values = []
		for value in q.get_points():
				values.append(value[dataAQA])
		return values
class canairio:
	def __init__(self,sensor):
		self.sensor = sensor 
	def getData(self):
		from subprocess import run
		run("curl -G 'http://influxdb.canair.io:8086/query?db=canairio' --data-urlencode 'q=select * from '"+self.sensor+"' WHERE time >= now() - 12h' > "+self.sensor+".json",shell = True)
	#get and read caniario data with solutions about  influx
	def json2datafarame(self,data):
		with open(self.sensor+".json",) as sensordata:
			data = json.load(sensordata)
			values = data["results"]
			#print(types(values))
			cols = values[0][values.index("series")]
			#print(type(cols))
			#[0]["columns"]
			#print(cols)
			#for i in data["values"]:
    		#print(i)
def main():
	import pandas as pd
	import statsmodels.api as sm
	import matplotlib.pyplot as plt
	HOST = "aqa.unloquer.org"
	db = aqa("aqa",HOST)
	pm25 = db.data("jero98772")
	#df=pd.read_csv('salesdata.csv')
	timeser = list(range(len(pm25)))
	data = {'time': timeser, 'pm25':pm25}
	df = pd.DataFrame(data=data)
	df.index=pd.to_datetime(df['time'])
	df['pm25'].plot()
	fig = plt.figure(figsize=(14.4,9.2))#120*4 =480*2 , 120*6 = 720 *2 =1440   
	ax1 = fig.add_subplot(211)
	fig = sm.graphics.tsa.plot_acf(df['pm25'].diff().dropna(), lags=40, ax=ax1)
	ax2 = fig.add_subplot(212)
	fig = sm.graphics.tsa.plot_pacf(df['pm25'].diff().dropna(), lags=40, ax=ax2)
	plt.show()
	model=sm.tsa.statespace.SARIMAX(endog=df['pm25'],order=(0,1,0),seasonal_order=(0,0,1,6),trend='c',enforce_invertibility=False)
	results=model.fit()
	print(results.summary())
def test():
	sensorTest = "PM25_Berlin_CanAirIO_v2"
	canairioclass = canairio(sensorTest)
	canairioclass.getData()
	canairioclass.json2datafarame(sensorTest)
test()