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
    }
    ]

proc = None
def execute_python(code):
    global proc
    with open("running.py", "w") as f:
        f.write(code)
    proc = subprocess.Popen(
        ["python", "-u", "running.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True
    )
    return "started"

def search(query):
     results = DDGS().text(query, max_results=5)
     return "\n\n".join(f"{r['title']}\n{r['body']}" for r in results)

TOOLS = {'search': search, 'execute_python': execute_python}
