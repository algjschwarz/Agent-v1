from ollama import chat
from ollama import ChatResponse

messages = [
    {
            'role': 'system',
            'content': 'You are five years old and are a fish'
    },
    {
        'role': 'user',
        'content': 'how to play fun games?'
    }
    ]

stream : ChatResponse = chat(model='gemma4:e4b', messages=messages, think=True, stream=True)
in_thinking = False
new_message = {'thinking':'','content':''}
for chunk in stream:
    if chunk.message.thinking:
        if not in_thinking:
            print("=== THINKING ===")
            in_thinking = True
        new_message['thinking'] = new_message['thinking'] + chunk.message.thinking
        print(chunk.message.thinking, end='', flush=True)
    if chunk.message.content:
        if in_thinking:
            print("\n\n=== ANSWER ===")
            in_thinking = False
        new_message['content'] = new_message['content'] + chunk.message.content
        print(chunk.message.content, end='', flush=True)
messages.append({'role': 'assistant', 'content': new_message['content'].strip()})

