# LangGraph Academy (uv)

This folder wraps the [langchain-academy](https://github.com/langchain-ai/langchain-academy) course inside a [uv](https://docs.astral.sh/uv/) project. Course notebooks and studio files live in `langchain-academy/`; dependencies are managed here in `pyproject.toml`.

## Setup

From this directory (`PHASE_02/langgraph/`):

```powershell
uv sync
```

That creates `.venv/`, installs all dependencies, and writes `uv.lock` for reproducible installs.

## Working with the environment

`uv sync` does **not** activate the shell for you. Use one of these:

**Option A — prefix commands with `uv run` (recommended):**

```powershell
uv run jupyter notebook langchain-academy/module-0/basics.ipynb
uv run langgraph dev
```

**Option B — activate the venv manually:**

```powershell
.\.venv\Scripts\Activate.ps1
jupyter notebook
```

**Option C — in Cursor/VS Code:** open the Command Palette → **Python: Select Interpreter** → choose `.venv\Scripts\python.exe`.

## Course content

Open notebooks under `langchain-academy/module-*`. See `langchain-academy/README.md` for API keys (OpenAI, LangSmith, Tavily) and Studio setup.

## Updating dependencies

When `langchain-academy/requirements.txt` changes upstream, add or update entries in `pyproject.toml`, then run:

```powershell
uv lock
uv sync
```
