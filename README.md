# Agent-v1

> ⚠️ **DEPRECATED — no longer maintained.**

---

## What this was

A from-scratch, fully local multi-agent AI system built to explore continual skill accumulation and adaptive retrieval. Everything runs on-device through Ollama on Windows.

**Stack**
- LLM: Gemma 4 E4B via Ollama
- Embeddings: EmbeddingGemma (300M)
- Terminal UI: Rich

**Codebase**

| File | Role |
|---|---|
| `main.py` | Entry point |
| `agent.py` | Agent loop and tool-calling |
| `memory.py` | Skill library, embeddings, retrieval |
| `tools.py` | Tools (DDGS web search, subprocess file execution) |
| `display.py` | Streaming output with thinking/answer separation |

## What got built

- **Voyager-style skill library** with semantic retrieval over stored skills
- **AST-based skill indexing and write gate** — skills are parsed and validated before they're allowed into the library
- **FLARE-style mid-generation retrieval** triggered by streaming cosine similarity from an external encoder (`inject_recall`)
- **Post-thinking embedding trigger** with deduplication
- **Subprocess-based tool execution**

The original vision (planner / creator / critic loop → persistent autonomous agent) was not completed in this version.

## Findings worth keeping

- Retrieval scores of **0.27–0.34 were noise**; genuine matches landed around **0.59–0.60**. A threshold near **0.45** separated them cleanly.
- **Ollama tool-call streaming can't be done token-by-token** — tool calls are buffered, so plan around receiving them whole.
- The external-encoder streaming-similarity retrieval trigger doesn't map neatly onto existing adaptive-retrieval approaches (confidence-based, learned classifier, RL policy). Closest prior art found: ReflectiChain.

## Running it anyway

You're on your own. Roughly:

```bash
ollama pull gemma4:e4b  
ollama pull embeddinggemma
pip install ollama rich duckduckgo-search
python main.py
```

Model tags and dependencies are not pinned and may have drifted.

## Status

Archived as a personal research playground. Experiments happen here; nothing here is a promise.
