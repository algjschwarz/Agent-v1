import os
from ddgs import DDGS
import subprocess
import queue
import threading
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
            'description': 'Start a Python program in the background. Returns immediately without output. Use observe_program to see what it prints.',
            'parameters': {
                'type': 'object',
                'properties': {'code': {'type': 'string'}},
                'required': ['code']
            }
        }
    },{
        'type': 'function',
        'function': {
            'name': 'observe_program',
            'description': 'Observe currently executing program in x seconds',
            'parameters': {
                'type': 'object',
                'properties': {'interval': {'type': 'integer'}},
                'required': ['interval']
            }
        }
    }
    ]

proc = None
q = queue.Queue()
def read_output(proc):
    for line in proc.stdout:
        q.put(line)

def read_file(file_name):
    path = f"scripts/{file_name}"
    if not os.path.exists(path):
        return f"no file named {file_name}. Use list_files to see what exists."
    with open(path, "r") as f:
        return f.read()

def list_files():
    files = os.listdir("scripts")
    if not files:
        return "no files yet"
    return "\n".join(files)

def write_to_file(file_name, text):
    with open(f"scripts/{file_name}", "w") as f:
        f.write(text)
        return f"wrote to {file_name}"

def execute_file(file_name, code):
    global proc
    proc = subprocess.Popen(
        ["python", "-u", f"scripts/{file_name}.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    threading.Thread(target=read_output, args=(proc,), daemon=True).start()
    return "started. The program is now running in the background. Call observe_program to see its output. Do not describe the program's behavior until you have observed it."

def observe_program(interval):
    sleep(interval)
    lines = []
    while not q.empty():
        lines.append(q.get())
    output = "".join(lines)
    status = "still running" if proc.poll() is None else f"exited with code {proc.returncode}"
    return f"status: {status}\noutput:\n{output}"

def search(query):
     results = DDGS().text(query, max_results=5)
     return "\n\n".join(f"{r['title']}\n{r['body']}" for r in results)

TOOLS = {'search': search, 'execute_file': execute_file,
         'observe_program': observe_program, 'read_file': read_file,
         'write_to_file': write_to_file}
