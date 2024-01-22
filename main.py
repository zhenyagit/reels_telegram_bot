import os
import logging
from telebot import TeleBot
from telebot.types import Message
import time

from src.reels_converter.repository.repository import Repository
from src.reels_converter.service import Service

logging.basicConfig(level=logging.DEBUG)
logging.getLogger("urllib3").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)

bot_token = os.environ["BOT_TOKEN"]
bot = TeleBot(bot_token)
service = Service(bot)
service.run()


@bot.message_handler(commands=['start'])
def start_command(message:Message):
    answer = """Hello, i was created to download reels from Instagram \nJust send the video link to me"""
    chat_id = message.chat.id
    service.db_add_person(message)
    bot.send_message(chat_id, answer)
    logger.info(f"User with chat_id: {chat_id} is started to use service")

@bot.message_handler(commands=["status"])
def get_status(message:Message):
    logger.info(f"{message.chat.username} trying to get status")
    chat_id = message.chat.id
    if not message.chat.username == "imjs_man":
        return
    data = {}
    repository = Repository()
    users = repository.get_users()
    for user in users:
        videos = repository.get_videos(user[0])
        data[user[1]] = videos
    bot.send_message(chat_id, f"{data}")
    

@bot.message_handler(regexp='https:\/\/www.instagram.com\/reel\/')
def proccessing_link(message:Message):
    logger.info(f"Catch message: {message.text}")
    chat_id = message.chat.id
    service.db_add_person(message)
    service.add_to_queue(chat_id, message.text)
    bot.send_message(chat_id, "Added to download queue. Please wait")

while True:
    try:
        bot.polling(non_stop=True)
    except Exception as e:
        logger.error(e)
        time.sleep(15)