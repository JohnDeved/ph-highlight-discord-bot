from bs4 import BeautifulSoup
import requests
from enum import Enum
from helper.config import PH_ENDPOINT, TIME_PERIOD

class TimePeriod(Enum):
    ALL_TIME = 'a'
    TODAY = 't'
    THIS_WEEK = 'w'
    THIS_MONTH = 'm'
    THIS_YEAR = 'y'

def get_popular_videos(time_period: TimePeriod = TimePeriod[TIME_PERIOD]):
    url = f"{PH_ENDPOINT}/video?p=homemade&o=mv&t={time_period.value}&cc=world"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = soup.select("#videoCategory.videos > .videoBox")
    
    return [
        f'{PH_ENDPOINT}/view_video.php?viewkey={video["data-video-vkey"]}'
        for video in videos 
            if isinstance(video["data-video-vkey"], str)
    ]