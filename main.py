import os
import logging
from telebot import TeleBot

from src.reels_converter.service import Service

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot_token = os.environ["BOT_TOKEN"]
bot = TeleBot(bot_token)
service = Service(bot)
service.run()


@bot.message_handler(commands=['start'])
def start_command(message):
    answer = """Hello, i was created to download reels from Instagram \nJust send the video link to me"""
    chat_id = message.chat.id
    bot.send_message(chat_id, answer)
    logger.info(f"User with chat_id: {chat_id} is started to use service")

@bot.message_handler(regexp='https:\/\/www.instagram.com\/reel\/')
def proccessing_link(message):
    logger.info(f"Catch message: {message.text}")
    chat_id = message.chat.id
    service.add_to_queue(chat_id, message.text)
    bot.send_message(chat_id, "Added to download queue. Please wait")

bot.polling()