import json

import bot.telegram_client
import bot.database_client
from bot.handlers.hander import Handler, HandlerStatus

class DrinkSelectionHander(Handler):
    def can_handle(self, update: dict, state: str, order_json: dict) -> bool:
        if "callback_query" not in update:
            return False
        
        if state != "WAIT_FOR_DRINK":
            return False
        
        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")
    
    def handle(self, update: dict, state: str, order_json: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_sprite": "Sprite",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_none": "No drink"
        }

        pizza_drink = drink_mapping.get(callback_data)
        order_json["pizza_drink"] = pizza_drink

        bot.database_client.update_user_order_json(telegram_id, order_json)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")
        bot.telegram_client.answerCallbackQuery(update["callback_query"]["id"])
        bot.telegram_client.deleteMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )
        pizza_name = order_json.get("pizza_name", "Unknown")
        pizza_size = order_json.get("pizza_size", "Unknown")
        drink = order_json.get("pizza_drink", "Unknown")

        order_summary = f"""🍕 **Your Order Summary:**
        **Pizza:** {pizza_name}
        **Size:** {pizza_size}
        **Drink:** {drink}

        Is everything correct?"""

        bot.telegram_client.sendMessage(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=  order_summary,
            parse_mode = "Markdown",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Approve", "callback_data": "order_approve"},
                        ],
                        [
                            {"text": "Revoke order", "callback_data": "order_revoke"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP