import asyncio
from langgraph_sdk import get_client

async def main():
    client = get_client(url="http://localhost:2024")

    # Create a thread
    thread = await client.threads.create()

    # Run the supervisor
    async for chunk in client.runs.stream(
        thread["thread_id"],
        "supervisor_agent",
        input={"messages": [{"role": "user", "content": "Use your subagent to tell me where ernest hemingway is from!"}]},
    ):
        print(chunk)

if __name__ == "__main__":
    asyncio.run(main())