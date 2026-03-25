# LangGraph + OpenAI + MCP Docs Agent

A LangGraph agent that uses OpenAI's `gpt-4o-mini` and connects to an MCP server ([Context7](https://context7.com)) to look up library documentation and answer questions about them.

Instrumented with [Sentry](https://sentry.io) for tracing and monitoring agent activity.

## How it works

The agent is built as a LangGraph state graph with two nodes:

- **model** — calls OpenAI with MCP tools bound
- **tools** — executes tool calls (documentation lookups via the Context7 MCP server)

The graph loops between the model and tools until the model produces a final response.

```
user message → model → tools → model → ... → response
```

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Copy the example env file and fill in your keys:

```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `OPENAI_API_KEY` | Your OpenAI API key |
| `SENTRY_DSN` | Your Sentry DSN for tracing |

## Run

```bash
python main.py
```

The agent will connect to the Context7 MCP server, look up documentation for LangGraph, and print a response about how to add memory to an agent.

To change the prompt, edit the message string in `main.py`.
