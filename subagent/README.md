# Subagent with Distributed Tracing

This subagent is configured to support distributed tracing when called from a parent graph.

## Key Implementation Details

The graph is wrapped in a context manager that:
- Accepts the parent trace context from the config
- Uses `langsmith.tracing_context()` to link traces
- Yields the compiled graph within the tracing context

This allows traces from this subagent to appear as child traces under the parent graph's trace in LangSmith.

## Running the Subagent

```bash
cd subagent
uv sync 
langgraph dev --port 8000 --no-browser
```

The subagent will start on `http://localhost:8000` by default.

