import asyncio
from langsmith import aevaluate
from langgraph_sdk import get_client
from langsmith import Client
from openevals import create_llm_as_judge
from openevals.prompts import CORRECTNESS_PROMPT
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

client = Client()
supervisor_client = get_client(url="http://localhost:2024")

examples = [{
    "input": "What is the capital of France?",
    "output": "Paris"
},
{
    "input": "What is the capital of Germany?",
    "output": "Berlin"
},
{
    "input": "What is the capital of Italy?",
    "output": "Rome"
},
{
    "input": "What is the capital of Spain?",
    "output": "Madrid"
}]

dataset_name = "Remote Graph distributed tracing eval"

if not client.has_dataset(dataset_name=dataset_name):
    dataset = client.create_dataset(dataset_name=dataset_name)
    client.create_examples(
        inputs=[{"messages": [{ "role" : "user", "content": ex["input"]}]} for ex in examples],
        outputs=[{"messages": [{ "role" : "ai", "content": ex["output"]}]} for ex in examples],
        dataset_id=dataset.id
    )


async def run_graph(inputs: dict):
    """Run graph and track the final response."""
    # Create a thread for this run
    thread = await supervisor_client.threads.create()
    
    # Use wait() to get the final result (streaming happens internally in the graph)
    result = await supervisor_client.runs.wait(
        thread["thread_id"],
        "supervisor_agent",
        input=inputs
    )
    
    # Extract and return the final output
    output = result["messages"][-1]["content"]
    return {"messages": [{"role": "ai", "content": output}]}


def correctness_evaluator(inputs: dict, outputs: dict, reference_outputs: dict):
    evaluator = create_llm_as_judge(
        prompt=CORRECTNESS_PROMPT,
        model="openai:gpt-4o",
        feedback_key="correctness",
    )
    eval_result = evaluator(
        inputs=inputs,
        outputs=outputs,
        reference_outputs=reference_outputs
    )
    return eval_result

async def main():
    results = await aevaluate(
        run_graph,
        data="Remote Graph distributed tracing eval",
        evaluators=[correctness_evaluator],
        experiment_prefix="testing",
        max_concurrency=2
    )

if __name__ == "__main__":
    asyncio.run(main())