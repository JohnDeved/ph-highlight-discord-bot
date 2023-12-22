from helper.clips import create_clips
from helper.popular import get_popular_videos
from helper.bot import send_file
from helper.db import get_json, set_json

videos = [v
    for v in get_popular_videos() 
        if v not in get_json()
]

for video in videos:
    clips = create_clips(video)
    for clip in clips:
        print("uploading", clip)
        send_file(clip, f"[source]({video})")
        
    set_json(get_json() + [video])