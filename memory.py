import ollama
import numpy as np
import glob
import ast
import os

script_embeddings = []

def embed(text) -> np.ndarray:
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

def similarity(a, b) -> float:
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, store, k=3) -> list:
    '''Searches store for k most similar to query.'''
    q = embed(query)
    scored = [(similarity(q, r['embedding']), r) for r in store]
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:k]

def extract_functions(tree) -> list:
    """Return name, args, and docstring for each top-level function in tree."""
    functions = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            args = [ast.unparse(a) for a in node.args.args]
            returns = ast.unparse(node.returns)
            functions.append({
                'name': node.name,
                'args': args,
                'returns': returns,
                'doc': ast.get_docstring(node)
            })
    return functions

def index_all() -> str:
    script_embeddings.clear()
    for path in glob.glob('scripts/*.py'):
        with open(path, encoding="utf-8") as f:
            text = f.read()
        try:
            tree = ast.parse(text)
            docstring = ast.get_docstring(tree)
        except SyntaxError:
            docstring = None
        if docstring is None:
            print(f"skipped {path}: no docstring")
            continue
        script_embeddings.append({
            'file_name': os.path.basename(path),
            'docstring': docstring,
            'embedding': embed(docstring),
            'functions': extract_functions(tree)
        })
    return f"indexed {len(script_embeddings)} scripts"

if __name__ == "__main__":
    index_all()
    print(search(input("Enter Input: "), script_embeddings))
