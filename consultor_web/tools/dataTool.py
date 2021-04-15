from influxdb import InfluxDBClient
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
		#q = self.client.query('SELECT mean("'+data+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE (time > now() - 5h GROUP BY time(10s) FILL(none))')
		q = self.client.query('select * from "'+name+'" WHERE time >= now() - 12h')
		#q = self.client.query('SELECT mean("'+data+'") AS "data" FROM "'+self.db+'"."autogen".'+name+' WHERE time > now() - 5h GROUP BY time(10s) FILL(none)')
		print(q)
		values = []
		for value in q.get_points():
				values.append(value[data])
		return values
