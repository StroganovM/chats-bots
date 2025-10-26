from bot.handlers.hander import Handler, HandlerStatus
import bot.database_client

class DB_Logger(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        return True
    
    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        bot.database_client.persist_update([update])
        return HandlerStatus.CONTINUE