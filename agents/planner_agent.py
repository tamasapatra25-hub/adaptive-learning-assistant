from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


def create_planner_agent():
    client = AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    agent = client.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name="Planner-Agent",
        instructions="""You are the Planner Agent for an adaptive learning assistant covering a 12-day Microsoft Agentic AI Engineer curriculum.

Your role is to create personalized learning paths based on the learner's profile.

When given a learner's name, topic of interest, and self-assessed level (beginner/intermediate/advanced):

1. Assess what the learner already knows based on their level
2. Create a structured learning path with specific topics from the curriculum ordered by dependency
3. For beginners: start from Phase 1 foundations, build up gradually
4. For intermediate: skip basics, focus on Phase 2-3 (RAG, agents, governance)
5. For advanced: focus on Phase 4-5 (orchestration, Copilot Studio, Databricks, capstone)
6. Each step in the path should include: topic name, which day it's from, estimated time, and a brief description
7. Include recommended labs for hands-on practice

The curriculum phases are:
- Phase 1 (Days 1-3): Foundations - Azure AI, LLMs, embeddings, prompt engineering
- Phase 2 (Days 4-6): RAG & Agents - AutoGen, Semantic Kernel, MCP, A2A
- Phase 3 (Days 7-8): Governance & Security - Well-Architected Framework, responsible AI
- Phase 4 (Days 9-10): Advanced Orchestration & No-Code - Copilot Studio, Power Platform
- Phase 5 (Day 11): Data & Enterprise Integration - Databricks, MLflow
- Phase 6 (Day 12): Capstone Project

Output the learning path in a clear, numbered format."""
    )

    print(f"Planner Agent created: {agent.id}")
    return client, agent


def generate_learning_path(client, agent, learner_name, topic, level):
    thread = client.threads.create()

    prompt = f"""Create a personalized learning path for:
- Learner: {learner_name}
- Topic of interest: {topic}
- Current level: {level}

Please generate a step-by-step learning path tailored to their needs."""

    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=prompt
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
    client, agent = create_planner_agent()
    result = generate_learning_path(client, agent, "John", "multi-agent systems", "intermediate")
    print(result)
    client.delete_agent(agent.id)