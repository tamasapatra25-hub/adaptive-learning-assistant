from azure.ai.agents import AgentsClient
from azure.ai.agents.models import AzureAISearchTool, AzureAISearchQueryType
from azure.identity import DefaultAzureCredential


import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


def create_rag_agent():
    client = AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    search_tool = AzureAISearchTool(
        index_connection_id="azureaiearchservicedemo",
        index_name=SEARCH_INDEX_NAME,
        query_type=AzureAISearchQueryType.SEMANTIC,
        top_k=5
    )

    agent = client.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name="RAG-Agent",
        instructions="""You are a Retrieval-Augmented Generation (RAG) agent for an adaptive learning assistant. 
Your role is to retrieve and return relevant training content from the indexed knowledge base covering a 12-day Microsoft Agentic AI Engineer curriculum.

When given a topic or question:
1. Search the connected knowledge base for the most relevant content
2. Return the retrieved content clearly, organized by day and topic
3. Include specific details like code examples, architecture patterns, key concepts, and lab instructions when available
4. Always cite which day and topic the information comes from
5. If the topic is not found in the knowledge base, say so clearly

You serve other agents (Planner, Feedback) by providing them with accurate curriculum content. Be thorough and precise.""",
        tools=search_tool.definitions,
        tool_resources=search_tool.resources
    )

    print(f"RAG Agent created: {agent.id}")
    return client, agent


def query_rag_agent(client, agent, query):
    thread = client.threads.create()

    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=query
    )

    run = client.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id
    )

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return None

    messages = client.messages.list(thread_id=thread.id)
    for msg in messages:
        if msg.role == "assistant":
            for block in msg.content:
                if hasattr(block, "text"):
                    return block.text.value
    return None


if __name__ == "__main__":
    client, agent = create_rag_agent()
    result = query_rag_agent(client, agent, "What is Semantic Kernel and how does it work?")
    print(result)
    client.delete_agent(agent.id)