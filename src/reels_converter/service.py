from queue import Queue
from telebot import TeleBot
from threading import Thread, Event
from io import BytesIO
import logging

from .reels_downloader import ReelsDownloader

logger = logging.getLogger(__name__)


class Service:
    def __init__(self, bot:TeleBot) -> None:
        self.download_queue = Queue()
        self.bot = bot
        self.stop_event = Event()
        self.thread_downloader = None
    
    def add_to_queue(self, chat_id, raw_reel_link):
        self.download_queue.put([chat_id, raw_reel_link])
        logger.info(f"Added to queue raw_reel_link: {raw_reel_link}, chat_id: {chat_id}")

    def send_binary_reel(self, chat_id, binary_reel):
        reel = BytesIO(binary_reel)
        self.bot.send_video(chat_id, reel)

    def infinity_downloader(self):
        while True:
            try:
                if self.stop_event.is_set():
                    break
                chat_id, reel_raw_link = self.download_queue.get()
                logger.info(f"Get reel_raw_link: {reel_raw_link}, chat_id: {chat_id}")
                binary_reel = ReelsDownloader.download_reel_raw_link(reel_raw_link)
                self.send_binary_reel(chat_id, binary_reel)
            except Exception as ex:
                logger.error(f"Error: {ex} with: {reel_raw_link}, chat_id: {chat_id}")
                try:
                    error_massage = f"Error: {ex} with: {reel_raw_link}"
                    self.bot.send_message(chat_id, error_massage)
                except:
                    logger.error("Error while send error")
            logger.info(f"Successfuly sended. Reel: {reel_raw_link}, chat_id: {chat_id}")
        logger.info("Thread downloader is stoped")
    
    def run(self):
        logger.info("Starting downloader thread")
        self.thread_downloader = Thread(target=self.infinity_downloader)
        self.thread_downloader.start()
        logger.info("Downloader thread is started")
    
    def __del__(self):
        self.stop_event.set()
        self.thread_downloader.join()

