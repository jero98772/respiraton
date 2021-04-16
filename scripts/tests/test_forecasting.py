from influxdb import InfluxDBClient
import numpy as np
def timex2(time):
	newTime = []
	numVales = len(time)
	for i in time:
		newTime.append(numVales+i)
	return time + newTime

class sensors:
	def __init__(self,db,host,port=8086):
		#self.port = port
		#self.host = host 
		self.client = InfluxDBClient(host=host, port=port)
		self.db = db
	def names(self):
		names = self.client.query('SHOW MEASUREMENTS ON "'+self.db+'"').raw
		clearNames = eval(str(names)[88:-4])
		return clearNames
	def data(self,name,data = "pm25"):
		q = self.client.query('SELECT mean("'+data+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE time > now() - 24h GROUP BY time(10s) FILL(none)')
		#q = self.client.query('select * from "PM25_Berlin_CanAirIO_v2" WHERE time >= now() - 12h')
		#q = self.client.query('SELECT mean("'+data+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE time > now() - 5h GROUP BY time(10s) FILL(none)')
		#q = self.client.query('SELECT mean("'+dataAQA+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE time > now() - 5h GROUP BY time(10s) FILL(none)')
		values = []
		for value in q.get_points():
			values.append(value["data"])
		return values
def main():
	import pandas as pd
	from statsmodels.tsa.statespace.sarimax import SARIMAX
	import matplotlib.pyplot as plt
	HOST = "aqa.unloquer.org"
	db = sensors("aqa",HOST)
	pm25 = db.data("jero98772")
	timeser = list(range(len(pm25)))
	timeser2 = timex2(timeser)
	#data = {'time': timeser, 'pm25':pm25}
	#df = pd.DataFrame(data=data)
	s_mod = SARIMAX(pm25, order=(1,2,1), seasonal_order=(1,1,1,24))
	#(p,d,q)(P,D,Q)m 
	"""
	https://puneet166.medium.com/time-series-forecasting-how-to-predict-future-data-using-arma-arima-and-sarima-model-8bd20597cc7b
	p = 2 
	m tiempo de un perido , dias de la semana = 7
	"""
	#results=s_mod.fit()
	#results.summary()
	predictions = list(s_mod.fit().predict())
	plt.plot(timeser,pm25,"bo")
	#plt.plot(timeser,predictions,"g-")
	plt.plot(timeser2,pm25+predictions,"r-")
	plt.show()
	#print(timeser*2)
	#print(pm25+predictions)
	print(len(timeser*2),len(pm25+predictions),len(timeser*2),len(pm25),len(predictions))
"""
	print(type(pm25),type(predictions))
	print(pm25+predictions)
	print(Y)
	filtred = np.polyfit(pm25, predictions, 1)
	Y = np.polyval(predictions, timeser)
for x in timeser:
    for y2 in y:

predictions = np.polyval(filtred, timeser)


"""

def test():
	sensorTest = "PM25_Berlin_CanAirIO_v2"
	canairioclass = canairio(sensorTest)
	canairioclass.getData()
	canairioclass.json2datafarame(sensorTest)
main()
