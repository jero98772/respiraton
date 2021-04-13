from influxdb import InfluxDBClient
import json
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