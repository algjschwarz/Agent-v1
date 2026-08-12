from ollama import chat
from ollama import ChatResponse

messages = [
    {
            'role': 'system',
            'content': 'You are a helpful assistant that has access to google'
    }
    ]

def stream_response(stream) -> list:
    is_thinking = False
    new_message = {'thinking':'','content':''}
    for chunk in stream:
        if chunk.message.thinking:
            if not is_thinking:
                print("=== THINKING ===")
                is_thinking = True
            new_message['thinking'] = new_message['thinking'] + chunk.message.thinking
            print(chunk.message.thinking, end='', flush=True)
        if chunk.message.content:
            if is_thinking:
                print("\n\n=== ANSWER ===")
                is_thinking = False
            new_message['content'] = new_message['content'] + chunk.message.content
            print(chunk.message.content, end='', flush=True)
    return new_message

def new_input(text) -> None:
    messages.append({'role': 'user', 'content': text})
    stream : ChatResponse = chat(model='gemma4:e4b', messages=messages, think=True, stream=True)
    new_message = stream_response(stream)
    messages.append({'role': 'assistant', 'content': new_message['content'].strip()})

while True:
    new_input(input())


