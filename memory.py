import ollama
import numpy as np
import glob
import ast
import os
import json
import hashlib

script_embeddings = []
meta_data = {}
META_FILE = 'scripts/_meta.json'

def file_hash(file_name) -> str:
    with open(f"scripts/{file_name}", "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def compare_file_hash(file_name: str) -> bool:
    hash = file_hash(file_name)
    if hash == meta_data[file_name]['hash']:
        return True
    else:
        return False

def load_meta_data() -> None:
    try:
        with open(META_FILE, "r") as f:
            meta_data.update(json.load(f))
    except (json.JSONDecodeError):
        pass

def _save_meta_data() -> None:
    with open(META_FILE, "w") as f:
        json.dump(meta_data, f, indent=2)

def set_grade(file_name: str, grade: str) -> None:
    meta_data[file_name] = {"grade": grade, "hash": file_hash(file_name)}
    _save_meta_data()

def get_grade(file_name: str) -> str:
    """pass, fail, or untested. Stale hashes are untested."""
    entry = meta_data.get(file_name)
    if entry is None:
        return "untested"
    try:
        if entry["hash"] != file_hash(file_name):
            return "untested"
    except (FileNotFoundError, KeyError):
        return "untested"
    return entry["grade"]

def embed(text) -> np.ndarray:
    return np.array(ollama.embed(model='embeddinggemma', input=text)['embeddings'][0])

def similarity(a, b) -> float:
    return a @ b / (np.linalg.norm(a) * np.linalg.norm(b))

def search(query, store, k=3) -> list:
    '''Searches store for k most similar to query.'''
    q = embed(query)
    scored = [(similarity(q, r['embedding']), r, query) for r in store]
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

def index_all_scripts() -> str:
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
            'functions': extract_functions(tree),
            'grade': get_grade(os.path.basename(path))
        })
    return f"indexed {len(script_embeddings)} scripts"

load_meta_data()
if __name__ == "__main__":
    load_meta_data()
    print(meta_data)


