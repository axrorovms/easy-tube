import re

def valid_video_url(vid_url: str):
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})"
    return re.match(pattern, vid_url) is not None
