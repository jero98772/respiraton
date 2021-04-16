from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from .logic import timex2
class pred():
	def __init__(self,data):
		self.data = data
	def predData(self):
		self.timeser = list(range(len(self.data)))
		self.timeser2 = timex2(self.timeser) # time use for prediction
		#model = SARIMAX(endog = self.data,exog = self.timeser , order=(1,2,1), seasonal_order=(1,1,1,24))	
		model = SARIMAX(self.data, order=(0,0,0),seasonal_order=(1,1,1,24))
		self.predictions = list(model.fit().predict())
		return self.predictions
	def saveImg(self,pathName):	
		plt.xlabel("time (as amout of data)")
		plt.ylabel("pm25")
		plt.title("prediction")
		plt.plot(self.timeser,self.data,"bo",label="data")
		plt.plot(self.timeser2,self.data+self.predictions,"g-",label="prediction")
		plt.savefig(pathName+'.png')
		plt.clf() 
