# Remote Graph with Distributed Tracing

This example demonstrates proper implementation of distributed tracing between a supervisor (parent) graph and a subagent (child/remote) graph using LangGraph.

## Overview

**Distributed tracing** allows you to see a unified trace in LangSmith that spans across multiple separate LangGraph deployments. When the supervisor calls the subagent, the subagent's trace appears as a child trace under the supervisor's trace.

## Architecture

```
┌─────────────────┐
│   Supervisor    │  (Parent Graph - Port 2024)
│   - Routes to   │  ✓ RemoteGraph with distributed_tracing=True
│     subagent    │  ✓ Automatically propagates trace context
└────────┬────────┘
         │ HTTP + Trace Headers
         ▼
┌─────────────────┐
│    Subagent     │  (Child Graph - Port 8000)
│   - React Agent │  ✓ Context manager with ls.tracing_context()
│   - Does work   │  ✓ Receives parent trace from config
└─────────────────┘
```

## Key Implementation Details

### Client Side (Supervisor)
The supervisor uses `RemoteGraph` with `distributed_tracing=True`:
```python
subagent_graph = RemoteGraph(
    "agent",
    url="http://localhost:8000",
    distributed_tracing=True  # Enables automatic trace propagation
)
```

### Server Side (Subagent)
The subagent wraps its graph in a context manager to receive the parent trace:
```python
@contextmanager
def graph(config):
    conf = config["configurable"]
    with ls.tracing_context(
        parent=conf.get("langsmith-trace"), 
        project=conf.get("langsmith-project")
    ):
        yield compiled_graph
```

**Important:** The `langgraph.json` must reference the context manager function (`graph`), not the compiled graph directly.

## Prerequisites

- Python 3.11+
- `uv` package manager installed
- LangSmith API key configured in `.env` file at project root
- OpenAI API key configured in `.env` file

## Setup

Both the supervisor and subagent have their own isolated environments managed by `uv`.

### Environment Variables

Copy .env.example to a .env file and fill in values.

### Install Dependencies

```bash
# Install subagent dependencies
cd subagent
uv sync

# Install supervisor dependencies  
cd supervisor
uv sync
```

## Running the Example

You need to run both services in separate terminals.

### Terminal 1: Start the Subagent (Port 8000 without spinning up studio in browser)

```bash
cd subagent
source .venv/bin/activate
langgraph dev --port 8000 --no-browser
```

You should see:
```
🚀 API: http://127.0.0.1:8000
🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8000
```

### Terminal 2: Start the Supervisor (Port 2024)

```bash
cd supervisor
source .venv/bin/activate
uv run langgraph dev
```

You should see:
```
🚀 API: http://127.0.0.1:2024
🎨 Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
```

## Testing Distributed Tracing

### Option 1: Use LangGraph Studio
1. Open the supervisor's Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:2024
2. Send a message to the supervisor
3. Watch it route to the subagent
4. Check LangSmith to see the unified trace

## Option 2: Use test.py in the supervisor folder
1. run 
``` bash
cd supervisor
uv run test.py
``` 
2. Watch it route to the subagent
3. Check LangSmith to see the unified trace

## Verifying Distributed Tracing

1. Go to [LangSmith](https://smith.langchain.com)
2. Navigate to your project
3. Find the trace from the supervisor invocation
4. You should see:
   - **Parent trace**: Supervisor execution
   - **Child trace**: Subagent execution nested within the supervisor trace
   - All spans properly linked in a single trace tree