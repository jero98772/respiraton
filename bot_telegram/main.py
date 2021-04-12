from telegram import Update
from tools.tools import readtxtline ,timer
from tools.db import dbManage
from telegram.ext import Updater, CommandHandler, CallbackContext
TOKENPATH = "files/token.txt"
CONFIGDB = "files/user_configs"
DBTABLE = "user"
db = dbManage(CONFIGDB)
def helpbot(update: Update, _: CallbackContext) -> None:
    update.message.reply_text('''Comandos\n
		-\t /help \t pide ayuda 
		-\t /test \t comprueba si el bot funciona
		-\t /start\t inicia el bot y recive alertas
		-\t /tiempo \t configura el tiempo de aletas en minutos 
		-\t /activarUbi \t activar ubicacion
		-\t /desactivarUbi  \t desactivar ubicacion
    	''')
def start(update: Update, _: CallbackContext) -> None:
	update.message.reply_text('Hola! Bienvenid@ \nsi nesesitas ayuda usa el comando /help.\nTe estare enviadno alertas y propuestas relacionadas a la calidad de aire.\nme gustaria que activaras tu ubicacion /activarUbi para darte mejor informacion')
	db.connect(DBTABLE,update.message.chat_id)
	db.createUser()
	while True:
		update.message.reply_text(mensaje)
		timer(db.getTimer(),"m")
def test(update: Update, context: CallbackContext) -> None:
	update.message.reply_text(f'Probando 1 2 3...  {update.effective_user.first_name} si me escuchas ,funciona')
def setAlert(update: Update, context) -> None:
	newTime = update.message.text[len("tiempo "):]
	db.connect(DBTABLE,update.message.chat_id)
	db.updateTimer(newTime)
	update.message.reply_text("tiempo actualisado a "+str(newTime)+" minutos", parse_mode='Markdown')
def locationOn(update: Update, context: CallbackContext) -> None:
	message = update.message
	loc = [message.location.latitude,message.location.longitude)]
	db.connect(DBTABLE,update.message.chat_id)    
	db.addLocation(loc)
def locationOff(update: Update, context: CallbackContext) -> None:
	db.connect(DBTABLE,update.message.chat_id)    
	db.disdableLocation()
updater = Updater(readtxtline(TOKENPATH))
updater.dispatcher.add_handler(CommandHandler('test', test))
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CommandHandler('help', helpbot))
updater.dispatcher.add_handler(CommandHandler('tiempo', setAlert ,pass_args=True))
updater.dispatcher.add_handler(CommandHandler('activarUbi', locationOn))
updater.dispatcher.add_handler(CommandHandler('desactivarUbi', locationOff))
updater.start_polling()
updater.idle()