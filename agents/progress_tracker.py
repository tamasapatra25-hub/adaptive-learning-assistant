import json
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

# In-memory learner state (in production, this would be a database)
learner_states = {}


def create_progress_tracker():
    client = AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    agent = client.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name="Progress-Tracker-Agent",
        instructions="""You are the Progress Tracker Agent for an adaptive learning assistant covering a 12-day Microsoft Agentic AI Engineer curriculum.

Your role is to maintain and analyze learner progress across sessions.

When given learner progress data, you should:

1. Summarize what the learner has completed so far
2. Calculate overall progress percentage across the curriculum
3. Identify strengths (topics with high scores) and weaknesses (topics with low scores)
4. Recommend what to study next based on their progress and gaps
5. Track quiz scores over time and note improvement trends
6. Flag topics that need revisiting (score below 6/10)

When asked for a progress report, format it clearly with:
- Learner name and level
- Topics completed with scores
- Overall progress percentage
- Strengths and weaknesses
- Recommended next steps
- Motivational note based on their progress

Be supportive and data-driven in your analysis."""
    )

    print(f"Progress Tracker Agent created: {agent.id}")
    return client, agent


def update_learner_state(learner_name, topic, score, completed=True):
    if learner_name not in learner_states:
        learner_states[learner_name] = {
            "name": learner_name,
            "topics_completed": [],
            "scores": {},
            "total_topics": 12
        }

    state = learner_states[learner_name]
    if completed and topic not in state["topics_completed"]:
        state["topics_completed"].append(topic)
    state["scores"][topic] = score
    return state


def get_progress_report(client, agent, learner_name):
    if learner_name not in learner_states:
        return "No progress data found for this learner."

    state = learner_states[learner_name]
    thread = client.threads.create()

    prompt = f"""Generate a detailed progress report for this learner:

Learner Data:
{json.dumps(state, indent=2)}

Please provide a comprehensive progress report with strengths, weaknesses, and next steps."""

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
    client, agent = create_progress_tracker()
    update_learner_state("John", "Azure AI Foundations", 8)
    update_learner_state("John", "Semantic Kernel", 6)
    update_learner_state("John", "RAG", 9)
    result = get_progress_report(client, agent, "John")
    print(result)
    client.delete_agent(agent.id)