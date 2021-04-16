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
		values = []
		for value in q.get_points():
			values.append(value["data"])
		return values
def getPm25(file):
	import pandas as pd
	mesures = pd.read_csv(file, sep=";")
	print(mesures)
	pm25s = mesures['Material Particulado PM 2.5'].values
	print(type(pm25s))
	return pm25s
	#pm25s = np.asanyarray(pm25s)
	#epochs = epochs.reshape((1,-1))
	#pm25s = pm25s.reshape((1,-1))
def main():
	#with canairio use ; and i need , ... is hard level
	from statsmodels.tsa.statespace.sarimax import SARIMAX
	from statsmodels.tsa.arima_model import ARIMA
	import matplotlib.pyplot as plt
	from sklearn.metrics import mean_squared_error
	HOST = "aqa.unloquer.org"
	db = sensors("aqa",HOST)
	#name = "aqa_montesori_nivel_calle"
	name = "jero98772"
	pm25 = db.data(name)
	#file = "test.csv"
	#pm25 = getPm25(file)
	timeser = list(range(len(pm25)))
	timeser2 = timex2(timeser)
	#model = ARIMA(endog = pm25, exog = timeser,order=(1, 2, 1))
	model = SARIMAX(endog = pm25,exog = timeser , order=(1,2,1), seasonal_order=(1,1,1,24))	
	predictions = list(model.fit().predict())
	rmse = (mean_squared_error(timeser2, predictions))**(1/2)
	print("rsm",len(rmse))
	plt.plot(timeser,pm25,"bo")
	plt.plot(timeser2,rmse,"r-")
	plt.show()
	#print(len(timeser*2),len(pm25+predictions),len(timeser*2),len(pm25),len(predictions))
main()