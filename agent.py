import ollama
from tools import tools, TOOLS
import memory
from display import stream_response, call_args, print_tool_result, print_recall

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
        print_tool_result(call.function.name, result)
        agent.messages.append({'role': 'tool', 'content': result,
                               'tool_name': call.function.name})

def inject_recall(query, agent, hits) -> None:
    lines = ["Scripts already created that can be used and imported freely."]
    
    for score, record, _ in hits:
        lines.append(f"- {record['file_name']}: {record['docstring']}")
        for fn in record['functions']:
            sig = f"{fn['name']}({', '.join(fn['args'])}) -> {fn['returns']}"
            lines.append(f"    {sig} — {fn['doc']}")

    
    agent.messages.append({
        'role': 'assistant',
        'content': '',
        'tool_calls': [{'function': {'name': 'recall_scripts',
                                        'arguments': {'query': query}}}]
    })
    agent.messages.append({
        'role': 'tool',
        'tool_name': 'recall_scripts',
        'content': "\n".join(lines)
    })

MAX_STORED = 400
def compact_messages(agent):
    for msg in agent.messages[:-2]:
        for call in msg.get('tool_calls', []):
            args = call_args(call)
            for key, val in args.items():
                if isinstance(val, str) and len(val) > MAX_STORED:
                    args[key] = f"<{len(val)} chars, omitted>"
        if msg.get('role') == 'tool' and len(msg['content']) > MAX_STORED:
            msg['content'] = msg['content'][:MAX_STORED] + " <truncated>"

def search_script_memory(message: dict, scripts_embeddings: list) -> list:
    script_hits = []
    for s in message["thinking"].split("."):
        if len(s.strip()) > 10:
            results = memory.search(s, scripts_embeddings, k=3)
            script_hits.extend(results)
    script_hits.sort(key=lambda x: x[0], reverse=True)
    seen = set()
    unique = []
    for hit in script_hits:
        if hit[1]['file_name'] not in seen:
            seen.add(hit[1]['file_name'])
            unique.append(hit)
    script_hits = unique[:4]
    for score, record, query in script_hits:
        if record in scripts_embeddings:
            scripts_embeddings.remove(record)
    return script_hits

def new_input(text, agent) -> None:
    agent.messages.append({'role': 'user', 'content': text})
    stop_after_thinking = True
    scripts_embeddings = memory.script_embeddings.copy()

    while True:
        compact_messages(agent)

        stream = ollama.chat(model='gemma4:e4b', messages=agent.messages,
                             think=agent.thinking, stream=True, tools=agent.tools)
        new_message = stream_response(stream, stop_after_thinking)
        if stop_after_thinking and len(scripts_embeddings) > 0:
            script_hits = search_script_memory(new_message, scripts_embeddings)
            print_recall(script_hits)
            inject_recall(script_hits[0][2], agent, script_hits)
            stop_after_thinking = False
            continue
        elif stop_after_thinking and len(scripts_embeddings) <= 0:
            stop_after_thinking = False
            continue

        msg = {'role': 'assistant', 'content': new_message['content'].strip()}
        if new_message['tool_calls']:
            msg['thinking'] = new_message['thinking']
            msg['tool_calls'] = new_message['tool_calls']
        agent.messages.append(msg)

        if not new_message['tool_calls']:
            return new_message['content']

        run_tool_calls(agent, new_message['tool_calls'])
        stop_after_thinking = True

class Agent():
    def __init__(self, agent_role, role_name, thinking=False, tools=[]):
        self.messages = [{'role': 'system', 'content': agent_role}]
        self.thinking = thinking
        self.tools = tools
        self.role_name = role_name
