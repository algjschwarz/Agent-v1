import ollama
from tools import tools, TOOLS
import memory
import display

creator_tools = tools[:7]
grader_tools = tools[4:8]
orchastrator_tools = tools[8:9]
MAX_STORED_CONTEXT = 400

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
    
class Agent():
    def __init__(self, system_prompt, role_name, thinking=False, tools=[]):
        self.messages = [{'role': 'system', 'content': system_prompt}]
        self.thinking = thinking
        self.tools = tools
        self.tool_log = []
        self.role_name = role_name

    def get_tool_calls(self, tool_name):
        if tool_name == "write_to_file":
            tools_used = []
            files = set()
            for tool in self.tool_log[::-1]:
                if tool["name"] == tool_name and tool["args"]["file_name"] in files:
                    continue
                elif tool["name"] == tool_name:
                    files.add(tool["args"]["file_name"])
                tools_used.append(tool)
            return tools_used[::-1]
        elif tool_name == "grade":
            tools_used = []
            filter = set()
            for tool in self.tool_log[::-1]:
            # reversed so last grades state is prioritized 
                if tool["name"] == tool_name:
                    if tool["args"]["file_name"] in filter:
                        continue
                    tools_used.append(tool)
                    filter.add(tool["args"]["file_name"])
            return tools_used[::-1]


    def new_input(self, text, recall_enabled) -> None:
        self.messages.append({'role': 'user', 'content': text})
        stop_after_thinking = recall_enabled
        scripts_embeddings = memory.script_embeddings.copy()

        while True:
            self.compact_messages()

            stream = ollama.chat(model='gemma4:e4b', messages=self.messages,
                                think=self.thinking, stream=True, tools=self.tools)
            new_message = display.stream_response(stream, stop_after_thinking)
            if recall_enabled:
                if stop_after_thinking and len(scripts_embeddings) > 0:
                    script_hits = search_script_memory(new_message, scripts_embeddings)
                    stop_after_thinking = False
                    match = script_hits[0][0]
                    if match >= 0.6:
                        display.print_recall(script_hits)
                        self.inject_recall(script_hits[0][2], script_hits)
                    else:
                        print("Recall found nothing useful enough.")
                    continue
                elif stop_after_thinking and len(scripts_embeddings) <= 0:
                    stop_after_thinking = False
                    recall_enabled = False
                    continue

            msg = {'role': 'assistant', 'content': new_message['content'].strip()}
            if new_message['tool_calls']:
                msg['thinking'] = new_message['thinking']
                msg['tool_calls'] = new_message['tool_calls']
            self.messages.append(msg)
            if not new_message['tool_calls']:
                return new_message['content']
            self.run_tool_calls(new_message['tool_calls'])
            stop_after_thinking = recall_enabled

    def compact_messages(self):
        for msg in self.messages[:-2]:
            for call in msg.get('tool_calls', []):
                args = display.call_args(call)
                for key, val in args.items():
                    if isinstance(val, str) and len(val) > MAX_STORED_CONTEXT:
                        args[key] = f"<{len(val)} chars, omitted>"
            if msg.get('role') == 'tool' and len(msg['content']) > MAX_STORED_CONTEXT:
                msg['content'] = msg['content'][:MAX_STORED_CONTEXT] + " <truncated>"

    def inject_recall(self, query, hits) -> None:
        lines = ["Scripts already created that can be used and imported freely."]
        
        for score, record, _ in hits:
            lines.append(f"- {record['file_name']}: {record['docstring']}")
            for fn in record['functions']:
                sig = f"{fn['name']}({', '.join(fn['args'])}) -> {fn['returns']}"
                lines.append(f"    {sig} — {fn['doc']}")
        
        self.messages.append({
            'role': 'assistant',
            'content': '',
            'tool_calls': [{'function': {'name': 'recall_scripts',
                                            'arguments': {'query': query}}}]
        })
        self.messages.append({
            'role': 'tool',
            'tool_name': 'recall_scripts',
            'content': "\n".join(lines)
        })

    def run_tool_calls(self, tool_calls):
        for call in tool_calls:
            fn = TOOLS.get(call.function.name)
            if fn is None:
                result = f"error: unknown tool {call.function.name}"
            else:
                try:
                    result = fn(**call.function.arguments)
                except Exception as e:
                    result = f"error: {type(e).__name__}: {e}"
            self.tool_log.append({
                "name": call.function.name,
                "args": dict(call.function.arguments),
                "result": result,
            })
            display.print_tool_result(call.function.name, result)
            self.messages.append({'role': 'tool', 'content': result,
                                'tool_name': call.function.name})

class Grader(Agent):
    def __init__(self, system_prompt, role_name, thinking=False, tools=[]):
        super().__init__(system_prompt, role_name, thinking, tools)
    
    def grade(self, agent):
        '''All files and observations and inputs must occur linearly, This grades programs wether or not they followed the user instruction'''
        user_first_message = agent.messages[1]['content']
        tools_used = agent.get_tool_calls("write_to_file")
        tools_log = {}

        for tool in tools_used:
            if tool["name"] == "write_to_file":
                if tool["args"]["file_name"] not in tools_log:
                    tools_log[tool["args"]["file_name"]] = {"description": ""}
            if tool["name"] == "write_to_file":
                try:
                    tools_log[tool["args"]["file_name"]]["description"] = tool['args']['description']
                except:
                    raise SyntaxWarning("Agent failed to provide description.")

        prompt = f"The users request was: '{user_first_message}': "

        for tool in tools_log.keys():
            prompt += f"Agent Created function '{tool}', with description '{tools_log[tool]['description']}', "
        print(prompt)
        self.new_input(prompt, recall_enabled=False)
        
def main():
    agent = Agent("Test", "Test",  False, tools=[])
    agent.messages.append({'role': 'user', 'content': "User Text"})                 
    agent.tool_log.extend([
                {"name": "write_to_file", "args": {"file_name": "Test", "description": "Test Description"}, "result": "Nothing"},
                {"name": "execute_file", "args": {"file_name": "Test"}, "result": "Nothing"},
                {"name": "send_input", "args": {"text": "Yes"}, "result": "Nothing"},
                {"name": "observe_program", "args": {"interval": "5"}, "result": "Input Yes: Yes"},

                {"name": "execute_file", "args": {"file_name": "Test_2"}, "result": "Nothing"},
                {"name": "observe_program", "args": {"interval": "3"}, "result": "Input Yes: "},
                {"name": "send_input", "args": {"text": "Yes"}, "result": "Nothing"}])
    grader = Grader("List what was created and done", role_name="grader", thinking=True, tools=[])
    grader.tool_log.extend([
        {"name": "grade", "args": {"file_name": "Test", "grade": "True"}, "result": "Nothing"},
        {"name": "grade", "args": {"file_name": "Test", "grade": "False"}, "result": "Nothing"},
        {"name": "grade", "args": {"file_name": "Test2", "grade": "False"}, "result": "Nothing"},
        {"name": "grade", "args": {"file_name": "Test2", "grade": "True"}, "result": "Nothing"},
        {"name": "grade", "args": {"file_name": "Test3", "grade": "True"}, "result": "Nothing"},
    ])
    print(grader.get_tool_calls("grade"))
    #grader.grade(agent)

if __name__ == "__main__":
    main()
