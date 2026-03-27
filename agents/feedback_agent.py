from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *


def create_feedback_agent():
    client = AgentsClient(
        endpoint=PROJECT_ENDPOINT,
        credential=DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True
        )
    )

    agent = client.create_agent(
        model=MODEL_DEPLOYMENT_NAME,
        name="Feedback-Agent",
        instructions="""You are the Feedback Agent for an adaptive learning assistant covering a 12-day Microsoft Agentic AI Engineer curriculum.

Your role is to evaluate learner responses and provide constructive feedback.

When given a topic, a question, and the learner's answer:

1. Assess whether the answer is correct, partially correct, or incorrect
2. Provide a score from 0-10
3. Explain what was correct in the answer
4. Identify any gaps or misconceptions
5. Provide the correct/complete answer with explanation
6. Suggest specific topics to review if the answer was weak
7. Generate a follow-up question to test deeper understanding

Also, when asked to generate quiz questions for a topic:
1. Create 3-5 questions ranging from basic recall to applied understanding
2. Include a mix of question types (conceptual, practical, scenario-based)
3. Provide the correct answers separately

Be encouraging but honest. The goal is to help the learner improve, not just score them."""
    )

    print(f"Feedback Agent created: {agent.id}")
    return client, agent


def evaluate_answer(client, agent, topic, question, learner_answer):
    thread = client.threads.create()

    prompt = f"""Evaluate this learner's answer:

Topic: {topic}
Question: {question}
Learner's Answer: {learner_answer}

Please score the answer (0-10), explain what's correct/incorrect, provide the complete answer, and suggest a follow-up question."""

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


def generate_quiz(client, agent, topic):
    thread = client.threads.create()

    client.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"Generate 5 quiz questions for the topic: {topic}. Include questions ranging from basic to advanced. Provide correct answers separately at the end."
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
    client, agent = create_feedback_agent()
    result = generate_quiz(client, agent, "Semantic Kernel")
    print(result)
    client.delete_agent(agent.id)