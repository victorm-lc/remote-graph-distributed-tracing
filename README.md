# Supervisor with Distributed Tracing

This supervisor graph demonstrates how to use `RemoteGraph` with distributed tracing enabled.

## Key Implementation Details

The supervisor:
- Uses `RemoteGraph` with `distributed_tracing=True` parameter
- Automatically propagates trace context to child graphs
- Creates a unified trace view in LangSmith

## Running the Supervisor

First, make sure the subagent is running on `http://localhost:8000`, then:

```bash
cd supervisor
uv sync
langgraph dev 
```

The supervisor will start on `http://localhost:8001` and will call the subagent with distributed tracing enabled.

