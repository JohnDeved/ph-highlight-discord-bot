from helper.clips import create_clips
from helper.popular import get_popular_videos
from helper.bot import send_file
from helper.db import get_json, set_json

uploaded_videos = set(get_json())
videos = set(get_popular_videos())
new_videos = videos - uploaded_videos

if len(new_videos) == 0:
    print("No new videos found")
    exit()

for video in new_videos:
    clips = create_clips(video)
    for clip in clips:
        print("uploading", clip)
        send_file(clip, f"[source]({video})")
        
    uploaded_videos.add(video)

set_json(list(uploaded_videos))