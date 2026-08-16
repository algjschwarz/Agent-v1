import ollama
from dataclasses import dataclass
from time import sleep
from tools import tools, TOOLS
import rich.rule
import rich.panel
from rich.console import Console

console = Console()

def stream_response(stream) -> list:
    is_thinking = False
    new_message = {'thinking':'', 'content':'', 'tool_calls':[]}
    for chunk in stream:
        if chunk.message.thinking:
            if not is_thinking:
                console.print(rich.rule.Rule("[dim]thinking[/dim]", style="dim"))
                is_thinking = True
            new_message['thinking'] = new_message['thinking'] + chunk.message.thinking
            console.print(chunk.message.thinking, end='', style="dim", highlight=False, soft_wrap=True)
        if chunk.message.content:
            if is_thinking:
                console.print(rich.rule.Rule("[bold]answer[/bold]"))
                is_thinking = False
            new_message['content'] = new_message['content'] + chunk.message.content
            console.print(chunk.message.content, end='', highlight=False, soft_wrap=True)
        if chunk.message.tool_calls:
            new_message['tool_calls'].extend(chunk.message.tool_calls)
    if new_message['tool_calls']:
        console.print(rich.rule.Rule("[cyan]tool calls[/cyan]", style="cyan"))
        console.print(new_message['tool_calls'])
    return new_message

def run_tool_calls(agent, tool_calls):
    for call in tool_calls:
        fn = TOOLS.get(call.function.name)
        if fn is None:
            result = f"error: unknown tool {call.function.name}"
        else:
            try:
                result = fn(**call.function.arguments)
            except Exception as e:
                 result = f"error: {type(e).__name__}: {e}"
    
        console.print(rich.panel.Panel(result[:500], title=call.function.name, border_style="green"))
        agent.messages.append({'role': 'tool', 'content': result,
                            'tool_name': call.function.name})

def new_input(text, agent) -> None:
    agent.messages.append({'role': 'user', 'content': text})

    while True:
        stream = ollama.chat(model='gemma4:e4b', messages=agent.messages, think=agent.thinking, stream=True, tools=agent.tools)
        new_message = stream_response(stream)

        msg = {'role': 'assistant', 'content': new_message['content'].strip()}
        if new_message['tool_calls']:
            msg['thinking'] = new_message['thinking']
            msg['tool_calls'] = new_message['tool_calls']
        agent.messages.append(msg)

        if not new_message['tool_calls']:
            return new_message['content']

        run_tool_calls(agent, new_message['tool_calls'])
        

class Agent():
    def __init__(self, agent_role, role_name, thinking=False, tools=[]):
        self.messages = [{'role': 'system', 'content': agent_role}]
        self.thinking = thinking
        self.tools = tools
        self.role_name = role_name
