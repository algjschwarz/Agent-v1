from ollama import chat
from ollama import ChatResponse
from datetime import datetime
from ddgs import DDGS
import subprocess
from dataclasses import dataclass
from time import sleep

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
def new_input(text, agent) -> None:
    agent.messages.append({'role': 'user', 'content': text})

    while True:
        stream = chat(model='gemma4:e4b', messages=agent.messages, think=agent.thinking, stream=True, tools=tools)
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
    def get_messages(self):
        responses = f"{self.role_name} Input: "
        for message in self.messages:
            for role, content in message.values:
                if role == "assistant":
                    responses = responses + content
        return responses
    def reset_messages(self):
        self.messages = self.messages[0]

def main():
    critic_tools = tools[0]
    creator_tools = tools[0:1]
    critic = Agent(f'You are a critic for an agent loop, your primary goal is to analyze thought processes, outcomes, and structure to agents actions and provice critical insight for how to improve', thinking=True, role_name="Critic", tools=critic_tools)
    creator = Agent(f'You are a creator for an agent loop, your primary goal is to create scripts and test them', thinking=True, role_name="Creator", tools=creator_tools)

    user_input = input("Enter Request: ")
    output = ""
    while True:
        output = new_input(f"User Input: {user_input}, Critic Input: {output}", creator)
        output = new_input(f"User Input: {user_input}, Creator Output: {output}", critic)

        

if __name__ == "__main__":
    main()

