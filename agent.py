from langgraph_supervisor import create_supervisor
from langchain_openai import ChatOpenAI
from langgraph.pregel.remote import RemoteGraph

subagent_graph = RemoteGraph(
    "agent",  # assistant_id as positional argument
    url="http://localhost:8000",
    distributed_tracing=True
)
model = ChatOpenAI(model="gpt-4o")
supervisor_graph = create_supervisor([subagent_graph], model=model)

graph = supervisor_graph.compile()