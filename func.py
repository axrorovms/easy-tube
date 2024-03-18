from youtube_transcript_api import YouTubeTranscriptApi as yta
import g4f
import re


VIDEO_ID_PATTERN = re.compile(r"(?<=v=)[\w-]+")

def get_transcript_from_video(vid_url: str):
    valid = valid_video_url(vid_url)
    if not valid:
        return "please enter youtube video url"
    
    match = VIDEO_ID_PATTERN.search(vid_url)
    vid_id = match.group(0)
    data = yta.get_transcript(vid_id)
    transcript_segments = []
    for value in data:
        for key, val in value.items():
            if key == 'text':
               transcript_segments.append(val)
    result = ' '.join(transcript_segments)
    with open('transcript.txt', 'w') as file:
        file.write(result)
    request = "Summarize the transcript from youtube video,write understable summarizing for the video and nothin more: \n" + result
    return ask_gpt(request)

def ask_gpt(prompt: str) -> str:
    response = g4f.ChatCompletion.create(
        model=g4f.models.gpt_4,
        messages=[{"role": "user", "content": prompt}],
    )
    return response

def valid_video_url(vid_url: str):
    pattern = r"(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([a-zA-Z0-9_-]{11})"
    return re.match(pattern, vid_url) is not None


