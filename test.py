import memory

memory.index_all()
print(memory.search("Make a calculator for me", memory.script_embeddings))
print(memory.search("Make a calculator Script for me", memory.script_embeddings))
print(memory.search("Make a script to make money for me", memory.script_embeddings))
