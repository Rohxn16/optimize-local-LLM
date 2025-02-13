from ollama import chat
from ollama import ChatResponse

payload = {
    "model": "deepseek-r1:7b",  # Specify the model name
    "prompt": "Explain the concept of quantum computing in simple terms.",  # Your input prompt
    "stream": False  # Set to True if you want streaming responses
}

f = open('output.txt', 'r')
text = f.read()
chattext = "summarize the following text which is a YT video transcript within 10 to 20 bullet points without missing out on any vital content: "
prompt = chattext + text
print(prompt)

response = chat(
    model=payload['model'],
    messages=
    [{
        'role':'user',
        'content':(str)(prompt)
    }])
print('------------------------------------------')
print(response['message']['content'])
f = open('response.txt','w')
f.write(response['message']['content'])
f.close()