from ollama import chat
from ollama import ChatResponse
from dataclasses import dataclass
from time import sleep
from tools import tools, TOOLS

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


def new_input(text, agent) -> None:
    agent.messages.append({'role': 'user', 'content': text})

    while True:
        stream = chat(model='gemma4:e4b', messages=agent.messages, think=agent.thinking, stream=True, tools=agent.tools)
        new_message = stream_response(stream)

        msg = {'role': 'assistant', 'content': new_message['content'].strip()}
        if new_message['tool_calls']:
            msg['thinking'] = new_message['thinking']
            msg['tool_calls'] = new_message['tool_calls']
        agent.messages.append(msg)

        if not new_message['tool_calls']:
            return new_message['content']

        for call in new_message['tool_calls']:
            fn = TOOLS.get(call.function.name)
            if fn is None:
                result = f"error: unknown tool {call.function.name}"
            else:
                try:
                    result = fn(**call.function.arguments)
                except Exception as e:
                    result = f"error: {type(e).__name__}: {e}"

            print(f"\n=== TOOL RESULT ===\n{result[:500]}\n")
            agent.messages.append({'role': 'tool', 'content': result,
                                'tool_name': call.function.name})

class Agent():
    def __init__(self, agent_role, role_name, thinking=False, tools=[]):
        self.messages = [{'role': 'system', 'content': agent_role}]
        self.thinking = thinking
        self.tools = tools
        self.role_name = role_name
