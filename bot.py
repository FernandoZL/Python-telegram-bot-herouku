import logging
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackContext)   
import os


from mail import *
import requests

PORT = int(os.environ.get('PORT', '8443'))

# Habilitar registro
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)
TOKEN = '5530425914:AAEUWQHLPVtM2ksZ6KQS3V8NmGKX_N7-6Sk'

# Definir algunos controladores de comandos. Estos suelen tomar los dos argumentos update y
# contexto. Los controladores de errores también reciben el objeto 
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('''Hola ! Soy su bot de seguimiento de envíos, encuentre los siguientes comandos para interactuar conmigo.
 /start_tracking: iniciar el proceso de seguimiento''')

# Location Tracking
LOC, DN, PHOTO = range(3)

def start_tracking(update: Update, context: CallbackContext):
    user = update.message.from_user
    logger.info("Driver: %s", user.first_name)  
    update.message.reply_text(
        'Please share your current GPS location.',
        reply_markup = ReplyKeyboardRemove(),
    )

    return LOC

def photo(update: Update, context: CallbackContext):
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    # photo_file.download('user_photo.jpg')

  # Get link to get file_path
    link1 = "https://api.telegram.org/bot{}/getfile?file_id={}".format(TOKEN, photo_file.file_id)
    r = requests.get(link1)
    file_path = r.json()["result"]["file_path"]




def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')

def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Cree el actualizador y pásele el token de su bot.
     # Asegúrese de configurar use_context=True para usar las nuevas devoluciones de llamada basadas en contexto
     # Publicar la versión 12 esto ya no será necesario
    updater = Updater(TOKEN, use_context=True)

 # Hacer que el despachador registre a los manejadores
    dp = updater.dispatcher

    # en diferentes comandos - respuesta en Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # en mensaje sin comando, es decir, repetir el mensaje en Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

  # registrar todos los errores
    dp.add_error_handler(error)

  # Iniciar el robot
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url='https://sergesa-bot.herokuapp.com/' + TOKEN
    )

    # Ejecute el bot hasta que presione Ctrl-C o el proceso reciba SIGINT,
     # SIGTERM o SIGABRT. Esto debe usarse la mayor parte del tiempo, ya que
     # start_polling() no bloquea y detendrá el bot con gracia.
    updater.idle()

if __name__ == '__main__':
    main()