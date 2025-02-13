from youtube_transcript_api import YouTubeTranscriptApi
from ollama import chat
import re

class OptimizeServices():

    def __init__(self):
        self.payload = {
    "model": "deepseek-r1:7b",  # Specify the model name
    "prompt": "Explain the concept of quantum computing in simple terms.",  # Your input prompt
    "stream": False  # Set to True if you want streaming responses
    }
    
    def trim_url(self,url):
        video_id = url.replace('https://www.youtube.com/watch?v=', '')
        return video_id

    def get_transcript(self,url:str):
        videoId = self.trim_url(url)
        transcript = YouTubeTranscriptApi.get_transcript(videoId)
        output = ''
        for x in transcript:
            sentence = x['text']
            output += f'{sentence}'
        return output

    def get_transcript_summary(self,link:str):
        transcript = self.get_transcript(link)
        prompt = "summarize the following text which is a YT video transcript within 10 to 20 bullet points without missing out on any vital content: " + transcript
        response = chat(
        model= self.payload['model'],
        messages=
        [{
            'role':'user',
            'content':(str)(prompt)
        }])
        responsetext = response['message']['content']
        cleaned_output = re.sub(r"<think>.*?</think>", "", responsetext, flags=re.DOTALL).strip()
        return cleaned_output

if __name__ == '__main__':
    context = OptimizeServices()
    op = context.get_transcript_summary('https://www.youtube.com/watch?v=Qa6csfkK7_I&t=109s&ab_channel=NesoAcademy')
    print(op)