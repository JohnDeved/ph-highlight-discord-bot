from bs4 import BeautifulSoup
import requests

def get_popular_videos():
    response = requests.get("https://www.pornhub.com/video?o=mv&cc=world")
    soup = BeautifulSoup(response.text, 'html.parser')
    videos = soup.select("#videoCategory.videos > .videoBox")
    
    return [
        f'https://www.pornhub.com/view_video.php?viewkey={video["data-video-vkey"]}'
        for video in videos 
            if isinstance(video["data-video-vkey"], str)
    ]