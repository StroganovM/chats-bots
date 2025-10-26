from bot.handler import Handler
import bot.telegram_client

class MessagePhotoEcho(Handler):
    def can_handle(self, update):
        return "message" in update and "photo" in update["message"]
    
    def handle(self, update):
        photos = update["message"]["photo"]
        large_photo = max(photos, key = lambda p: p["file_size"])
        file_id = large_photo['file_id']

        bot.telegram_client.sendPhoto(
            chat_id = update["message"]["chat"]["id"],
            photo = file_id
        )
        return False