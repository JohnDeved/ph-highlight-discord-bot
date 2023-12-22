from bs4 import BeautifulSoup
import requests
import json
import re
import subprocess
from urllib.parse import urlparse, parse_qs
import os

# constants
CLIP_TIME = 45
CLIP_PADDING = 5

def get_video_meta(url: str):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    scripts = soup.find_all('script')
    hotspots = []
    video_duration = 0

    for script in scripts:
        if 'hotspots' in script.text:
            hotspots_match = re.search(r'"hotspots":(\[.*?\])', script.text)
            if hotspots_match:
                hotspots: list[int] = json.loads(hotspots_match.group(1))

            video_duration_match = re.search(r'"video_duration":(\d+)', script.text)
            if video_duration_match:
                video_duration = int(video_duration_match.group(1))

    return hotspots, video_duration

def get_popular_parts(hotspots: list[int], video_duration: int) -> list[int]:
    # Create a list of dictionaries, each containing the number of views and the corresponding time in the video
    hotspot_times = [{
        'views': hotspots[i],  # number of views
        'time': round((i / len(hotspots)) * video_duration)  # time in seconds
    } for i in range(len(hotspots))]

    # Calculate the average number of views
    avg_views = sum(hotspot['views'] for hotspot in hotspot_times) / len(hotspot_times)

    # Sort the hotspots by popularity in descending order
    hotspot_times.sort(key=lambda x: x['views'], reverse=True)

    # Count the number of popularity spikes (where the views are higher than the average)
    spike_times: list[int] = []
    for hotspot in hotspot_times:
        if hotspot['views'] <= avg_views:
            continue
        
        # ignore hotspots within the first minute
        if hotspot['time'] < 60:
            continue
        
        # check if is too close to the previous spikes
        if any(abs(hotspot['time'] - spike_time) < CLIP_TIME for spike_time in spike_times):
            continue
        
        spike_times.append(hotspot['time'])

    clip_count = len(spike_times)

    popular_parts: list[int] = []
    for hotspot in hotspot_times:
        # Ignore hotspots within the first minute
        if hotspot['time'] < 60:
            continue
        
        # Check if the current hotspot is too close to any of the popular parts
        if any(abs(hotspot['time'] - popular_part) < CLIP_TIME for popular_part in popular_parts):
            continue

        # If the current hotspot is not too close to any of the popular parts, add it to the list
        popular_parts.append(hotspot['time'])
        if len(popular_parts) == clip_count:
            break

    # Sort the popular parts by time in ascending order
    popular_parts.sort()

    return popular_parts

def create_clip(start_time: int, input_file: str, output_file: str):
    # Create the ffmpeg command
    subprocess.run(["ffmpeg", "-y", "-ss", str(start_time - CLIP_PADDING), "-i", input_file, "-t", str(CLIP_TIME + CLIP_PADDING), "-c", "copy", output_file])

def concatenate_clips(clips: list[str], output_file: str):
    # Create a file with the list of clips
    with open("clips.txt", "w") as f:
        for clip in clips:
            f.write(f"file '{clip}'\n")

    # Create the ffmpeg command
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", "clips.txt", "-c", "copy", output_file])

    # Remove the list of clips
    os.remove("clips.txt")

def create_clips(url: str):
    hotspots, video_duration = get_video_meta(url)
    popular_parts = get_popular_parts(hotspots, video_duration)

    # Parse the URL and extract the video ID
    parsed_url = urlparse(url)
    video_id = parse_qs(parsed_url.query)['viewkey'][0]

    # check if the video is already downloaded
    if os.path.isfile(f"./videos/{video_id}.mp4"):
        print("video already downloaded", video_id, url)
    else:
        print("downloading video with id", video_id, url)
        subprocess.run(["yt-dlp", "-o", f"./videos/{video_id}.mp4", url]).check_returncode()
        
    # Create a clip for each popular part
    clips: list[str] = []
    for i, start_time in enumerate(popular_parts):
        input_file = f"./videos/{video_id}.mp4"
        output_file = f"./videos/{video_id}_clip_{i}.mp4"
        create_clip(start_time, input_file, output_file)
        clips.append(output_file)

    return clips
    # Concatenate the clips into a single video
    # concatenate_clips(clips, f'./videos/{video_id}_final.mp4')
