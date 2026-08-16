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

def execute_python(code):
    result = subprocess.run(["python", "-c", code], capture_output=True, text=True, timeout=30)
    return f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"

def search(query):
     results = DDGS().text(query, max_results=5)
     return "\n\n".join(f"{r['title']}\n{r['body']}" for r in results)

TOOLS = {'search': search, 'execute_python': execute_python}
