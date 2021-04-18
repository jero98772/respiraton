from flask import Flask, render_template, request
from tools.dataTool import sensors
from tools.pred import pred
from tools.logic import now , readtxtline ,writetxt 
app = Flask(__name__)
class webpage():
	WEBPAGE = "/"
	@app.route(WEBPAGE+"check.html")
	def webpredictions():
		return render_template()
	@app.route(WEBPAGE+"prediction.html")
	def prediction():
		SALT = "_predict"
		#HOST = "aqa.unloquer.org"
		#dbNames = ["aqa","v80","aqamobile"]
		HOST = "influxdb.canair.io"
		dbNames = ["canairio"]
		"""
		time for rest 
		FILEDATETIME = "data/last.txt"
		nowDateTime =  now()
		time = readtxtline(FILEDATETIME)
		status = " fatlta tiempo para una nueva predccion"# tiempo para hacer la predccion , la idea es que no sea pronostico por cada consulta
		if  
		"""
		status = ""
		sensorsNames = []
		sensorsON = []
		for i in dbNames:
			db = sensors(i,HOST)
			sensorsNames += db.names()
		#can use recursion to be more faster
			for ii in sensorsNames:
				#print(ii)
				name = ii[0]
				path = "img/"+ii[0]
				try:
					print("check error")
					pm25 = db.data(name);pm25[0]
					print("no error for "+name)
					predict = pred(pm25)
					predict.predDataSarimax()
					print("pred")
					predict.saveImg("static/img/"+name+SALT)
					print("save img")
					sensorsON.append(name)
					print("ok for"+name)
				except:
						pass
				"""		
				print("check error")
				pm25 = db.data(name)#;pm25[0]
				print("no error for "+name)
				predict = pred(pm25)
				predict.predDataSarimax()
				print("pred")
				predict.saveImg("static/img/"+name+SALT)
				print("save img")
				sensorsON.append(name)
				print("ok for"+name)
				"""
				"""
				db = sensors("aqa",HOST)
				name = "jero98772"
				pm25 = db.data(name);pm25[0]
				print("ERROR",pm25)
				#predict = pred(pm25)
				#predict.predData()
				#predict.saveImg("static/img/"+name+SALT)
				print("saved/img")
				sensorsON.append(name)
				print("ok for"+str(sensorsON))
				"""
		#print(type(sensorsON))
		#data
		#print(type(sNames))
		#working = genpredsunloquer(db[0],host) +genpredsunloquer(db[1],host) +genpredsunloquer(db[2],host)
		#writetxt(ultimoRegistro,ahora+(horas))
		#deletefiles(nombres)
		#writetxt(nombres,working)
		#status = "predicion disponible en 2 horas "
		return render_template("consultor.html",names = sensorsON,msg = status,salt= SALT)
webpage()
if __name__=='__main__':
	app.run(debug=True,host="0.0.0.0",port=9600)
