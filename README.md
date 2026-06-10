# AI Agent — Vibe Coding & Understanding with Gemini API

A functional AI coding agent built in Python using the Gemini API. The agent can autonomously explore a codebase, read files, run Python scripts, and write/fix code — all driven by natural language prompts.

Built as part of the [Boot.dev AI Agent course](https://www.boot.dev), with hands-on experimentation using Google's Gemini API.

---

## Features

- **List files** in any directory within the working scope
- **Read file contents** with automatic truncation for large files
- **Write and overwrite files** with automatic parent directory creation
- **Execute Python files** with optional arguments and timeout protection
- **Agent loop** — iterates up to 20 turns, calling tools until a final response is produced
- **Path traversal protection** — all tools validate paths against the working directory

---

## Project Structure

```
AI-AGENT/
├── main.py                  # Entry point — agent loop
├── call_function.py         # Dispatcher + available function declarations
├── prompts.py               # System prompt
├── calculator/              # Sample project for the agent to work on
│   ├── main.py
│   ├── tests.py
│   └── pkg/
│       ├── calculator.py
│       └── render.py
├── functions/
│   ├── get_files_info.py    # Tool: list directory contents
│   ├── get_file_content.py  # Tool: read file contents
│   ├── run_python_file.py   # Tool: execute Python files
│   └── write_file.py        # Tool: write/overwrite files
├── test_get_files_info.py
├── test_get_file_content.py
└── test_write_file.py
```

---

## Setup

**Requirements:** Python 3.11+, [uv](https://github.com/astral-sh/uv)

```bash
git clone https://github.com/DrakyNeUwU/AI-Agent-Vibe-Coding-Understanding-with-Gemini-API.git
cd AI-Agent-Vibe-Coding-Understanding-with-Gemini-API

uv sync
```

Create a `.env` file:

```
GEMINI_API_KEY=your_api_key_here
```

---

## Usage

```bash
# Basic usage
uv run main.py "how does the calculator render results to the console?"

# With verbose output (shows tool calls and results)
uv run main.py "fix the bug: 3 + 7 * 2 shouldn't be 20." --verbose
```

**Example output:**
```
 - Calling function: get_files_info
 - Calling function: get_file_content
Final response:
The calculator renders results using format_json_output() from pkg/render.py...
```

---

## How It Works

```
User Prompt
    ↓
Agent Loop (max 20 iterations)
    ↓
LLM decides which tool to call
    ↓
Tool executes → returns result string
    ↓
Result appended to conversation history
    ↓
LLM reads result → decides next step
    ↓
(repeat until no more tool calls)
    ↓
Final Response printed
```

The agent never sees outside the `./calculator` working directory — all tools enforce path validation to prevent unauthorized file access.

---

## Tech Stack

- **Python 3.11+**
- **[google-genai](https://pypi.org/project/google-genai/)** — Gemini API SDK
- **[uv](https://github.com/astral-sh/uv)** — Python package manager
- **python-dotenv** — environment variable management

---

## License

MIT