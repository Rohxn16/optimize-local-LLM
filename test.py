# from  youtube_transcript_api import YouTubeTranscriptApi
# from datetime import datetime as time

# # summarizer = pipeline("summarization", model="stevhliu/my_awesome_billsum_model")

# def get_transcript(video_id):
#     try:
#         transcript = YouTubeTranscriptApi.get_transcript(video_id)
#         text = " ".join([t['text'] for t in transcript])
#         return text
#     except Exception as e:
#         return str(e)



# video_id = "5_6waKTGlqA"  # Replace with the actual video ID
# transcript = get_transcript(video_id)
# print(transcript)
# print
# print('-------------------------------------------------')
# # summary = summarize_text(transcript)
# # print(summary)
# # time1 = time.now()
# # print(response.message.content)
# # print(time.now() - time1)

from youtube_transcript_api import YouTubeTranscriptApi
# from transformers import pipeline

# summarizer = pipeline("summarization", model="stevhliu/my_awesome_billsum_model")

url = 'https://www.youtube.com/watch?v=Qa6csfkK7_I&t=109s&ab_channel=NesoAcademy'
print(url)

video_id = url.replace('https://www.youtube.com/watch?v=', '')
print(video_id)

transcript = YouTubeTranscriptApi.get_transcript(video_id)

print(transcript)

output=''
for x in transcript:
  sentence = x['text']
  output += f' {sentence} '

f = open('output.txt', 'w')
f.write(output)
f.close()

# response = summarizer(output)
print(type(output))