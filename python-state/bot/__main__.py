from bot.dispatcher import Dispatcher
from bot.handlers.message_echo import MessageEcho
from bot.handlers.database_logger import DB_Logger
from bot.handlers.message_photo_echo import MessagePhotoEcho
from bot.long_polling import start_long_polling
    

if __name__ == "__main__" :
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(DB_Logger())
        dispatcher.add_handler(MessagePhotoEcho())
        dispatcher.add_handler(MessageEcho())
        start_long_polling(dispatcher)
    except KeyboardInterrupt:
        str("\nBye!")