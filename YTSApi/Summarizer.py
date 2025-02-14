from youtube_transcript_api import YouTubeTranscriptApi
from ollama import chat
import re

class OptimizeServices():

    def __init__(self):
        self.payload = {
        "model": "deepseek-r1:7b",  # Specify the model name
        "stream": False  # Set to True if you want streaming responses
    }
        self.transcript = ''
        self.summary = ''
        self.chat_history = []
    
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
        self.transcript = output
        return output

    def get_transcript_summary(self,link:str):
        transcript = self.get_transcript(link)
        prompt = "summarize the following text which is a YT video transcript within 10 to 20 bullet points without missing out on any vital content: " + transcript
        response = chat(
        model= self.payload['model'],
        messages=
        [
            *self.chat_history,

            {
            'role':'user',
            'content':(str)(prompt)
            }
        ])
        responsetext = response['message']['content']
        cleaned_output = re.sub(r"<think>.*?</think>", "", responsetext, flags=re.DOTALL).strip()
        self.summary = cleaned_output
        
        # Add the prompt and summary to chat history as the first conversation
        self.chat_history.append({"role": "user", "content": prompt})
        self.chat_history.append({"role": "system", "content": cleaned_output})
        
        return cleaned_output

    def ask_question(self, question: str):
        """Answer user questions based on the video summary and maintain chat history."""
        if not self.summary:
            return "Error: No summary available. Please generate a summary first."

        # Add the user's question to chat history
        self.chat_history.append({"role": "user", "content": question})

        # Get the response from the model
        response = chat(
            model=self.payload['model'],
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on the provided YouTube video summary."},
                *self.chat_history  # Include the chat history for context
            ]
        )
        answer = response['message']['content']
        cleaned_answer = re.sub(r"<think>.*?</think>", "", answer, flags=re.DOTALL).strip()

        # Add the model's response to chat history
        self.chat_history.append({"role": "assistant", "content": answer})

        return cleaned_answer
    
    # debug
    def print_chat_history(self):
        for i in self.chat_history:
            print(i)

if __name__ == '__main__':
    context = OptimizeServices()
    op = context.get_transcript_summary('https://www.youtube.com/watch?v=Qa6csfkK7_I&t=109s&ab_channel=NesoAcademy')
    print(op)
    print('--------------------------')
    while True:
        question = input('Enter question: ')
        if question == 'exit':
            break
        print(context.ask_question(question))
        # context.print_chat_history()
        print('--------------------------') 
    