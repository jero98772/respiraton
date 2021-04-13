from flask import Flask, render_template, request
app = Flask(__name__)
class webpage():
	WEBPAGE = ""
	@app.route(WEBPAGE+"")
	def pm25predictUnloquer():
"""
		from core.proyects.pm25Predict.pm25Predict import genpredsunloquer
		hoy = hoyminsArr()
		ahora = minsTotales(hoy)
		ultimoRegistro = "data/pm25Predict/registros/ultimoRegistroUnloquer"#+".txt"
		nombres = "data/pm25Predict/sensors_names/sensors_unloquer"#+".txt"
		horas = 60*2
		host = "aqa.unloquer.org"
		plazo = readtxt(ultimoRegistro)
		plazo = int(plazo[0]) 
		status = "le fatlta " + str( plazo-ahora )+" minutos para una nueva predccion"
		if horas <= (plazo-ahora):
			db = ["aqa","v80","aqamobile"]
			working = genpredsunloquer(db[0],host) +genpredsunloquer(db[1],host) +genpredsunloquer(db[2],host)
			writetxt(ultimoRegistro,ahora+(horas))
			deletefiles(nombres)
			writetxt(nombres,working)
			status += "predicion disponible en 2 horas "
		else:
			status += "proccima predicion disponible en 2 horas "
		working = eval(readtxtstr(nombres))
		return render_template('',names = working,msg = status )
"""	
webpage()

if __name__=='__main__':
	webapp.run(debug=True,host="0.0.0.0",port=9600)