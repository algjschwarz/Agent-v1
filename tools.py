import os
from ddgs import DDGS
import subprocess
import queue
import threading
from time import sleep
import memory
import ast

tools = [
    {
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
    },
    {
        'type': 'function',
        'function': {
            'name': 'write_to_file',
            'description': 'Write text to a file. Overwrites if it already exists.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {'type': 'string'},
                    'description': {'type': 'string', 'description': 'One sentence describing what problem this script solves, phrased the way someone would ask for it.'},
                    'text': {'type': 'string'}
                },
                'required': ['file_name', 'description', 'text']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'read_file',
            'description': 'Read the contents of a file',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {'type': 'string'}
                },
                'required': ['file_name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'list_files',
            'description': 'List all files',
            'parameters': {
                'type': 'object',
                'properties': {}
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'execute_file',
            'description': 'Run a Python file in the background. Returns immediately without output. Use observe_program to see what it prints.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'file_name': {'type': 'string'}
                },
                'required': ['file_name']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'observe_program',
            'description': 'Wait a number of seconds, then return whatever the running program has printed and whether it is still running.',
            'parameters': {
                'type': 'object',
                'properties': {
                    'interval': {'type': 'integer'}
                },
                'required': ['interval']
            }
        }
    },
    {
        'type': 'function',
        'function': {
            'name': 'send_input',
            'description': 'Send input through stdin to program',
            'parameters': {
                'type': 'object',
                'properties': {
                    'text': {'type': 'string'}
                },
                'required': ['text']
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
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def list_files():
    files = os.listdir("scripts")
    if not files:
        return "no files yet"
    return "\n".join(files)

def write_to_file(file_name, description, text):
    if file_name.endswith('.py'):
        text = f'"""{description}"""\n\n' + text

        try:
            tree = ast.parse(text)
        except SyntaxError as e:
            return f"REJECTED, file not written. Syntax error: {e}. Fix the code and call write_to_file again."

        docstring = ast.get_docstring(tree)
        if docstring is None:
            return "REJECTED, file not written. Could not extract a docstring."

        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                if ast.get_docstring(node) is None:
                    return f"REJECTED, file not written. Function {node.name} has no docstring."
                if node.returns is None:
                    return f"REJECTED, file not written. Function {node.name} has no return type specified, add a return type to {node.name} and call write_to_file again."
                    
        embedding = memory.embed(docstring)
        memory.script_embeddings.append({'file_name': file_name, 'embedding': embedding, 'docstring': docstring, 'functions': memory.extract_functions(tree)})

    with open(f"scripts/{file_name}", "w", encoding="utf-8") as f:
        f.write(text)
    return f"wrote to {file_name}"

def execute_file(file_name):
    global proc
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.Popen(
        ["python", "-u", f"scripts/{file_name}"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        stdin=subprocess.PIPE,
        text=True,
        env=env,
        encoding="utf-8"
    )
    threading.Thread(target=read_output, args=(proc,), daemon=True).start()
    return "started. The program is now running in the background. Call observe_program to see its output. Do not describe the program's behavior until you have observed it."

def send_input(text):
    proc.stdin.write(text.rstrip('\n') + "\n")
    proc.stdin.flush()
    return f"sent: {text}"

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
         'write_to_file': write_to_file, 'list_files': list_files,
         'send_input': send_input}
