#!/usr/bin/env python 
# -*- coding: utf-8 -*-"
from tools.dataTool import sensors
from telegram import Update
from tools.tools import readtxtline ,timer ,readtxt
from tools.db import dbManage
from telegram.ext import Updater, CommandHandler, CallbackContext ,MessageHandler , filters
TOKENPATH = "files/token.txt"
CONFIGDB = "files/user_configs"
DBTABLE = "user"
db = dbManage(CONFIGDB)
updater = Updater(readtxtline(TOKENPATH))
def sendMsg():
	host = "influxdb.canair.io"
	dbData  = sensors("canairio",host)
	data = dbData.data()
	last = data[-1::]
	if last < 26 : #favorable de acuedo a Association of the combined effects of air pollution and changes in physical activity with cardiovascular disease in young adults
		msg = readtxt("files/inectivos.txt")
		msg = "Hola ,"+{update.effective_user.first_name}+".\n"+msg+"\nla ultima medicion fue {0} .".format(last)
	else:
		msg = readtxt("files/alertas.txt")
		msg = "Hola ,"+{update.effective_user.first_name}+".\n"+msg+"\nla ultima medicion fue {0} .".format(last)
		#update.message.reply_text(msg)
	return msg
def helpbot(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('''Comandos\n
		-\t /help \t pide ayuda 
		-\t /test \t comprueba si el bot funciona
		-\t /start\t inicia el bot y recive alertas
		-\t /tiempo <tiempo>\t configura el tiempo de aletas en minutos 
		-\t /activarUbi <lat/long>\t activar ubicacion \n \t\t\t puedes añadir cordenadas como 6.2433/-75.5763 ,es importante diferenciar latitid/logitud \n
		-\t /desactivarUbi\t desactivar ubicacion \n
    	-\t /añadirSensor <nombre>\t añade el sensor que te enviara notificaciones \n es esencial
    	''')
def start(update: Update, _: CallbackContext) -> None:
	msg1 = '''
	Hola! Bienvenid@ a Aire alParque. 
	te ayudaremos a planear tu dia con el mejor momento de menos comtaminacion  
	hecho por Alianza Piranga
	mas informacion aqui: 
	https://aire-al-parque.web.app/principalParques
	'''
	msg2 = '''
	si nesesitas ayuda usa el comando /help.\nTe estare enviadno alertas y propuestas relacionadas a la calidad de aire del sensor selecionado .\nme gustaria que activaras tu ubicacion /activarUbi para darte mejor informacion'
	'''
	update.message.reply_text(msg1)
	update.message.reply_text(msg2)
	while True:
		update.message.reply_text(sendMsg())
		timer(db.getTimer(),"m")
	db.connect(DBTABLE,update.message.chat_id)
	db.createUser()
def test(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(f'Probando 1 2 3...  {update.effective_user.first_name} si me escuchas ,funciona')
def setAlert(update: Update, context) -> None:
	newTime = update.message.text[len("tiempo "):]
	db.connect(DBTABLE,update.message.chat_id)
	db.updateTimer(newTime)
	update.message.reply_text("tiempo actualisado a "+str(newTime)+" minutos", parse_mode='Markdown')
def locationOn(update: Update, context) -> None:
	loc = [0,0]
	args = update.message.text[len("activarUbi "):]
	if len("activarUbi ") <  len(args):
		loc = [args[:args.find("/")],args[args.find("/")+1:]]
	db.connect(DBTABLE,update.message.chat_id)
	db.addLocation(loc)
	update.message.reply_text("activando ubicacion para las cordenadas"+str(loc), parse_mode='Markdown')
def sensorConfig(update: Update, context) -> None: 
	sensorName = update.message.text[len("addSensor "):]
	db.connect(DBTABLE,update.message.chat_id)
	db.addSensor(sensorName)
	update.message.reply_text("reciviras notificaciones del sensor "+str(sensorName), parse_mode='Markdown')
def locationOff(update: Update, context: CallbackContext) -> None:
	db.connect(DBTABLE,update.message.chat_id)    
	db.disdableLocation()
	update.message.reply_text("desactivando ubicacion", parse_mode='Markdown')

updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helpbot))
updater.dispatcher.add_handler(CommandHandler('desactivarUbi', locationOff))
updater.dispatcher.add_handler(CommandHandler('activarUbi', locationOn,pass_args=True))
updater.dispatcher.add_handler(CommandHandler('tiempo', setAlert ,pass_args=True))
updater.dispatcher.add_handler(CommandHandler('añadirSensor ',sensorConfig,pass_args=True))#  error ValueError: Command is not a valid bot command

updater.start_polling()
updater.idle()
