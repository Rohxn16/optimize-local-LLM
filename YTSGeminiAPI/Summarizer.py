from youtube_transcript_api import YouTubeTranscriptApi
import os
import google.generativeai as genai
from flask import Flask, request, jsonify
from flask_cors import CORS

genai.configure(api_key='AIzaSyCyLyign7HC2ZaRcTak0eS3A1is13gtAbM')

def trim_url(url):
    video_id = url.replace('https://www.youtube.com/watch?v=', '')
    return video_id

def get_transcript(url:str):
    videoId = trim_url(url)
    transcript = YouTubeTranscriptApi.get_transcript(videoId)
    output = ''
    for x in transcript:
        sentence = x['text']
        output += f'{sentence}'
    transcript = output
    return output


# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-2.0-flash",
  generation_config=generation_config,
)

chat_session = model.start_chat(
  history=[
    {
      "role": "user",
      "parts": [
        "You are an educational AI model who's work is to summarize educational YouTube video transcripts and answer follow up questions relevant to the topic only. If the transcript topic is not educational then decline request with an appropriate message. Even if the questions asked are not educational or unrelated to the topic of the video transcript then decline with an appropriate message. In case the topic is appropriate and you are answering, answer it in bullet points in byte sized information.",
      ],
    },
    {
      "role": "model",
      "parts": [
        "Okay, I understand! I'm ready to summarize educational YouTube video transcripts and answer relevant follow-up questions. I will:\n\n*   **Prioritize educational content:** I will only work with transcripts that clearly teach a specific subject or skill.\n*   **Decline non-educational requests:** I will politely refuse to summarize or answer questions about transcripts that are entertainment, opinion pieces, or otherwise not educational.\n*   **Stay on topic:** I will only answer questions directly related to the content of the summarized transcript. Irrelevant or non-educational questions will be declined.\n*   **Provide concise, bullet-point answers:** My answers will be structured as bullet points, delivering information in a clear and easily digestible format.\n\nI'm eager to help users learn! Please provide a transcript, and I'll do my best to assist.\n",
      ],
    },
  ]
)


def get_transcript_summary(link:str):
    trimmed_linked = trim_url(link)
    transcript = get_transcript(link)
    response = chat_session.send_message(f"summarize this {transcript}")

    # add it to the chat history
    chat_session.history.append(
        {
            'role':'user',
            'parts': [
                f"summarize this {transcript}"
            ]
        }
    )

    chat_session.history.append(
        {
            'role':'model',
            'parts': [
                response.text
            ]
        }
    )
    
    print(response.text)
    return response.text

def follow_up_question(question:str):
    response = chat_session.send_message(question)

    # add it to the chat history
    chat_session.history.append(
        {
            'role':'user',
            'parts': [
                question
            ]
        }
    )
    chat_session.history.append(
        {
            'role':'model',
            'parts': [
                response.text
            ]
        }
    )
    return response.text

# get_transcript_summary('https://www.youtube.com/watch?v=Qa6csfkK7_I&t=109s')

print('------------------------------------------------')

if __name__ == '__main__':
    app = Flask(__name__)
    CORS(app)  # Enable CORS for all routes

    @app.route('/summarize', methods=['GET','POST'])
    def summarize():
        data = request.get_json()
        yt_link = data.get('yt_link')
        if not yt_link:
            return jsonify({'error': 'YouTube link is required'}), 400

        try:
            summary = get_transcript_summary(yt_link)
            return jsonify({'summary': summary}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        
    # reuquest = http://localhost:5000/summarize/

    @app.route('/ask', methods=['GET','POST'])
    def ask():
        data = request.get_json()
        question = data.get('question')
        if not question:
            return jsonify({'error': 'Question is required'}), 400

        try:
            response = follow_up_question(question)
            return jsonify({'response': response}), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/', methods=['GET'])
    def home():
        return jsonify({'message': 'Welcome to the YTSGeminiAPIv2!'})
    
        
    app.run(port=5000, debug=True)