from ollama import chat
from ollama import ChatResponse
from datetime import date
from ddgs import DDGS

tools = [{
    'type': 'function',
    'function': {
        'name': 'search',
        'description': 'Search the web for information',
        'parameters': {
            'type': 'object',
            'properties': {
                'query': {'type': 'string'}
            },
            'required': ['query']
        }
    }
}]

messages = [
    {
        'role': 'system',
        'content': f'You are a helpful assistant. Today is {date.today()}.'
    }
    ]

def stream_response(stream) -> list:
    is_thinking = False
    new_message = {'thinking':'', 'content':'', 'tool_calls':[]}
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
        if chunk.message.tool_calls:
                new_message['tool_calls'].extend(chunk.message.tool_calls)
    print("\n\n=== TOOL CALLS ===")
    print(new_message['tool_calls'])
    return new_message

def search(query):
     results = DDGS().text(query, max_results=5)
     return "\n\n".join(f"{r['title']}\n{r['body']}" for r in results)

def new_input(text) -> None:
    messages.append({'role': 'user', 'content': text})

    while True:
        stream = chat(model='gemma4:e4b', messages=messages, think=True, stream=True, tools=tools)
        new_message = stream_response(stream)

        msg = {'role': 'assistant', 'content': new_message['content'].strip()}
        if new_message['tool_calls']:
            msg['thinking'] = new_message['thinking']
            msg['tool_calls'] = new_message['tool_calls']
        messages.append(msg)

        if not new_message['tool_calls']:
            return

        for call in new_message['tool_calls']:
            result = search(**call.function.arguments)
            print(f"\n=== TOOL RESULT ===\n{result[:500]}\n")
            messages.append({
                'role': 'tool',
                'content': result,
                'tool_name': call.function.name,
            })

new_input('search who won the 2025 world series?')

