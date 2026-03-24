# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Agent

```bash
# Run the main agent (queries weather and recommends attractions)
python MyAgent.py

# Test the LLM client standalone
python OpenAIClient.py

# Test tools standalone
python tools.py
```

## Required Environment Variables

- `TAVILY_API_KEY` — required by `get_attraction()` in `tools.py` for web search

## Architecture

This is a ReAct-style (Reasoning + Acting) agent loop implemented from scratch:

- **`Config.py`** — LLM endpoint config (model, api_key, base_url) and the `AGENT_SYSTEM_PROMPT` that defines the Thought/Action format
- **`OpenAIClient.py`** — thin wrapper around the OpenAI-compatible SDK; `generate(prompt, system_prompt)` sends the full conversation history as a single user message
- **`tools.py`** — tool implementations (`get_weather`, `get_attraction`) and `available_tools` dict used for dispatch
- **`MyAgent.py`** — the agent loop: runs up to 5 iterations, appends LLM output and observations to `prompt_history`, parses `Action: tool_name(arg="val")` with regex, dispatches to `available_tools`, and breaks on `finish(answer="...")`

**Agent loop flow:** User prompt → LLM generates `Thought:/Action:` → regex parses tool call → tool executes → `Observation:` appended to history → repeat until `finish()` or max iterations.

The LLM is called via ModelScope's OpenAI-compatible API (DeepSeek-V3.2 by default).
