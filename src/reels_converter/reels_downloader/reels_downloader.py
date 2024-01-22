import requests
import re
import logging
from ..exceptions import *

logger = logging.getLogger(__name__)

class ReelsDownloader:

    @staticmethod
    def get_reel_id(reel_link):
        try:
            reel_id = re.findall(r'reel\/(.*?)\/', reel_link)[0]
            logger.debug(f"Found reel id {reel_id} in url {reel_link}")
        except Exception as ex:
            logger.error(f"Error while parse reel link: {ex}, link: {reel_link}")
            raise CantFindIdInURL(f"No id in link: {reel_link}")
        return reel_id
    
    @staticmethod
    def get_reel_link(reel_id):
        logger.debug(f"Try create link for reel with id: {reel_id}")
        link = "https://www.instagram.com/graphql/query/"
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/86.0.4240.193 Safari/537.36'
        }
        params = {
            'hl': 'en',
            'query_hash': 'b3055c01b4b222b8a47dc12b090e4e64',
            'variables': '{"child_comment_count":3,\
                "fetch_comment_count":40,\
                "has_threaded_comments":true,\
                "parent_comment_count":24,\
                "shortcode":"' + reel_id + '"}'
        }
        try:
            resp = requests.get(link, headers=headers, params=params).json()
            reel_link = resp['data']['shortcode_media']['video_url']
        except Exception as ex:
            logger.error(f"Сant create link because: {ex}, resp: {resp}")
            raise CantCreateReelLink("No connection")
        logger.debug(f"Created reel link: {reel_link} for reel id: {reel_id}")
        return reel_link
    
    @staticmethod
    def download_reel(reel_link):
        logger.debug(f"Downloading reel from {reel_link}")
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                Chrome/86.0.4240.193 Safari/537.36'
        }
        try:
            resp = requests.get(reel_link, headers=headers).content
        except Exception as ex:
            logger.error(f"Failed to download reel from {reel_link}")
            raise CantDownloadReel("Cant download reel")
        logger.debug(f"Successfuly download reel {reel_link}")
        return resp
        
    @staticmethod
    def download_reel_raw_link(raw_link):
        logger.info(f"Try download reel {raw_link}")
        reel_id = ReelsDownloader.get_reel_id(raw_link)
        reel_link = ReelsDownloader.get_reel_link(reel_id)
        binary_reel = ReelsDownloader.download_reel(reel_link)
        logger.debug(f"Successfuly download reel {raw_link}")
        return binary_reel


def test():
    logging.basicConfig(level=logging.DEBUG)
    reel_link = "https://www.instagram.com/reel/CvKqTbLRu9s/?hl=en"
    ReelsDownloader.download_reel_raw_link(reel_link)
    

if __name__ == "__main__":
    test()
