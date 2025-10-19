from bot.handler import Handler
import bot.database_client

class DB_Logger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True
    
    def handle(self, update: dict) -> bool:
        bot.database_client.persist_update([update])
        return True