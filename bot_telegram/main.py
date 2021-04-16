from telegram import Update
from tools.tools import readtxtline ,timer
from tools.db import dbManage
from telegram.ext import Updater, CommandHandler, CallbackContext ,MessageHandler , filters
TOKENPATH = "files/token.txt"
CONFIGDB = "files/user_configs"
DBTABLE = "user"
db = dbManage(CONFIGDB)
updater = Updater(readtxtline(TOKENPATH))
def helpbot(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('''Comandos\n
		-\t /help \t pide ayuda 
		-\t /test \t comprueba si el bot funciona
		-\t /start\t inicia el bot y recive alertas
		-\t /tiempo \t configura el tiempo de aletas en minutos 
		-\t /activarUbi \t activar ubicacion \n \t\t\t puedes añadir cordenadas como 6.2433/-75.5763 ,es importante diferenciar latitid/logitud 
		-\t /desactivarUbi  \t desactivar ubicacion
    	''')
def start(update: Update, _: CallbackContext) -> None:
	msg1 = '''
	Hola! Bienvenid@ a Aire alParque. 
	te ayudaremos a planear tu dia con el mejor momento de menos comtaminacion  
	hecho por Alianza Piranga
	'''
	msg2 = '''
	si nesesitas ayuda usa el comando /help.\nTe estare enviadno alertas y propuestas relacionadas a la calidad de aire.\nme gustaria que activaras tu ubicacion /activarUbi para darte mejor informacion'
	'''
	update.message.reply_text(msg1)
	update.message.reply_text(msg2)
	db.connect(DBTABLE,update.message.chat_id)
	db.createUser()
	while True:
		update.message.reply_text("aqui debe ir una alerta ...")
		timer(db.getTimer(),"m")
def test(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(f'Probando 1 2 3...  {update.effective_user.first_name} si me escuchas ,funciona')
def setAlert(update: Update, context) -> None:
	newTime = update.message.text[len("tiempo "):]
	db.connect(DBTABLE,update.message.chat_id)
	db.updateTimer(newTime)
	update.message.reply_text("tiempo actualisado a "+str(newTime)+" minutos", parse_mode='Markdown')
def locationOn(update: Update, context) -> None:
	args = update.message.text[len("activarUbi "):]
	if len("activarUbi ") <  len(args):
		loc = [args[:args.find("/")],args[args.find("/")+1:]]
	db.connect(DBTABLE,update.message.chat_id)
	db.addLocation(loc)
	update.message.reply_text("activando ubicacion para las cordenadas"+str(loc), parse_mode='Markdown')
def locationOff(update: Update, context: CallbackContext) -> None:
	db.connect(DBTABLE,update.message.chat_id)    
	db.disdableLocation()
	update.message.reply_text("desactivando ubicacion", parse_mode='Markdown')

updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helpbot))
updater.dispatcher.add_handler(CommandHandler('tiempo', setAlert ,pass_args=True))
updater.dispatcher.add_handler(CommandHandler('activarUbi', locationOn,pass_args=True))
updater.dispatcher.add_handler(CommandHandler('desactivarUbi', locationOff))
updater.start_polling()
updater.idle()
"""
color pm25,  tiempo de expocion (general, personas con riesgo )
verde todo , todo
amarilo todo , 
naranja
rojo
"""