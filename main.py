from ollama import chat
from ollama import ChatResponse
from datetime import date
from ddgs import DDGS
import subprocess

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
    },{
        'type': 'function',
        'function': {
            'name': 'execute_python',
            'description': 'Execute Python code and return stdout and stderr',
            'parameters': {
                'type': 'object',
                'properties': {'code': {'type': 'string'}},
                'required': ['code']
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

def execute_python(code):
    result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=30)
    return f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

def search(query):
     results = DDGS().text(query, max_results=5)
     return "\n\n".join(f"{r['title']}\n{r['body']}" for r in results)

TOOLS = {'search': search, 'execute_python': execute_python}
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
            fn = TOOLS[call.function.name]
            result = fn(**call.function.arguments)
            print(f"\n=== TOOL RESULT ===\n{result[:500]}\n")
            messages.append({
                'role': 'tool',
                'content': result,
                'tool_name': call.function.name,
            })

while True:
    new_input(input("Input: "))

