import asyncio
import os

import sentry_sdk
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState, StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

load_dotenv()

sentry_sdk.init(
    dsn=os.environ["SENTRY_DSN"],
    environment="local",
    traces_sample_rate=1.0,
    send_default_pii=True,
)


async def main() -> None:

    client = MultiServerMCPClient(
        {
            "context7": {
                "url": "https://mcp.context7.com/mcp",
                "transport": "streamable_http",
            }
        }
    )
    tools = await client.get_tools()

    model = ChatOpenAI(model="gpt-4o-mini").bind_tools(tools)

    def call_model(state: MessagesState):
        response = model.invoke(state["messages"])
        return {"messages": [response]}

    graph = (
        StateGraph(MessagesState)
        .add_node("model", call_model)
        .add_node("tools", ToolNode(tools))
        .add_edge("__start__", "model")
        .add_conditional_edges("model", tools_condition)
        .add_edge("tools", "model")
        .compile()
    )

    result = await graph.ainvoke(
        {
            "messages": [
                (
                    "user",
                    "Find the docs for the LangGraph Python library and tell me how to add memory to an agent.",
                )
            ]
        }
    )

    print(result["messages"][-1].content)


if __name__ == "__main__":
    with sentry_sdk.start_transaction(name="main"):
        asyncio.run(main())
