from pytube import YouTube

video_url = 'https://www.youtube.com/watch?v=WQJZeL40Ems&t=1s'

import yt_dlp
ydl_opts = {'outtmpl': 'video.mp4'}
# Create a new instance of the downloader
ydl = yt_dlp.YoutubeDL()

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    info = ydl.extract_info(video_url, download=False)

# Get available streams with their resolutions
available_streams = {}
for stream in info['formats']:
    if 'resolution' in stream:
        available_streams[stream['resolution']] = stream

# Present available resolutions to the user
print("Available Resolutions:")
for i, resolution in enumerate(available_streams.keys(), start=1):
    print(f"{i}. {resolution}")

# Let the user choose the resolution
chosen_resolution_index = int(input("Enter the number corresponding to the desired resolution: ")) - 1
chosen_resolution = list(available_streams.keys())[chosen_resolution_index]
chosen_stream = available_streams[chosen_resolution]

# Specify the output filename
output_filename = 'video.mp4'

# Download the chosen stream with the specified output filename
ydl_opts['outtmpl'] = output_filename
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([chosen_stream['url']])
