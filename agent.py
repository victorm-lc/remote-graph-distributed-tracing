from contextlib import contextmanager
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import langsmith as ls

model = ChatOpenAI(model="gpt-4o")

tools = []

compiled_graph = create_react_agent(model, tools)

@contextmanager
def graph(config):
    """Context manager that enables distributed tracing by passing parent trace context."""
    conf = config["configurable"]
    with ls.tracing_context(
        parent=conf.get("langsmith-trace"), 
        project=conf.get("langsmith-project")
    ):
        yield compiled_graph