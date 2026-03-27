# Adaptive Learning Assistant — Multi-Agent AI System

A multi-agent adaptive learning system built for the Microsoft Agentic AI Engineer curriculum. The system uses 5 specialized AI agents to deliver personalized learning paths, retrieve curriculum content, evaluate learner knowledge, and track progress across sessions.

## Architecture

The system follows a multi-agent architecture with the following components:

| Agent | Role | Platform |
|-------|------|----------|
| **Intake Agent** | Collects learner profile (name, topic, level) | Copilot Studio |
| **Planner Agent** | Builds personalized learning paths | Azure AI Foundry |
| **RAG Agent** | Retrieves content from indexed training materials | Azure AI Foundry + AI Search |
| **Feedback Agent** | Generates quizzes and evaluates answers | Azure AI Foundry |
| **Progress Tracker Agent** | Maintains learner state and generates reports | Azure AI Foundry |

## Tech Stack

- **Azure AI Foundry** — Agent Service for hosting and orchestrating agents
- **Azure AI Search** — Vector index for semantic retrieval (RAG)
- **GPT-4o** — Primary LLM for reasoning and generation
- **text-embedding-ada-002** — Embedding model for vectorization
- **Copilot Studio** — Front-door conversational interface
- **Python SDK** — `azure-ai-agents`, `azure-ai-projects`, `azure-identity`
- **Semantic Kernel** — Planning and orchestration logic

## Project Structure

```
adaptive-learning-assistant/
├── agents/
│   ├── __init__.py
│   ├── planner_agent.py        # Personalized learning path generation
│   ├── rag_agent.py            # RAG retrieval from AI Search index
│   ├── feedback_agent.py       # Quiz generation and answer evaluation
│   └── progress_tracker.py     # Learner state and progress reports
├── orchestrator.py             # Main orchestrator tying all agents together
├── config.py                   # Configuration and environment variables
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- Azure subscription with access to Azure AI Foundry
- Azure CLI installed and authenticated
- An Azure AI Foundry project with GPT-4o deployed
- An Azure AI Search index with training content

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/tamasapatra25-hub/adaptive-learning-assistant.git
   cd adaptive-learning-assistant
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate       # Windows
   source .venv/bin/activate    # Mac/Linux
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file from the template:
   ```bash
   copy .env.example .env       # Windows
   cp .env.example .env         # Mac/Linux
   ```

5. Fill in your `.env` file with your Azure credentials:
   ```
   PROJECT_ENDPOINT=https://<your-resource>.services.ai.azure.com/api/projects/<your-project>
   MODEL_DEPLOYMENT_NAME=gpt-4o
   SEARCH_ENDPOINT=https://<your-search-service>.search.windows.net
   SEARCH_INDEX_NAME=<your-index-name>
   SEARCH_API_KEY=<your-search-api-key>
   ```

6. Log in to Azure CLI:
   ```bash
   az login
   az account set --subscription "<your-subscription-id>"
   ```

### Running the Application

Run the full orchestrator:
```bash
python orchestrator.py
```

This will:
1. Create all 4 Foundry agents
2. Ask for your name, topic of interest, and level
3. Generate a personalized learning path
4. Provide an interactive menu to learn topics, take quizzes, check answers, and view progress

### Testing Individual Agents

```bash
python agents/rag_agent.py          # Test RAG retrieval
python agents/planner_agent.py      # Test learning path generation
python agents/feedback_agent.py     # Test quiz generation
python agents/progress_tracker.py   # Test progress tracking
```

## How It Works

1. **Onboarding**: The learner provides their name, topic of interest, and current level
2. **Planning**: The Planner Agent creates a personalized learning path based on the 12-day curriculum
3. **Learning**: The RAG Agent retrieves relevant content from the indexed training materials using semantic search
4. **Assessment**: The Feedback Agent generates quizzes and evaluates answers with detailed feedback
5. **Tracking**: The Progress Tracker Agent maintains scores and generates progress reports with recommendations

## Training Data

The knowledge base consists of summarized notes from a 12-day Microsoft Agentic AI Engineer training program covering:

- **Phase 1 (Days 1–3)**: Azure AI fundamentals, LLMs, embeddings, prompt engineering
- **Phase 2 (Days 4–6)**: RAG, agents, AutoGen, Semantic Kernel, MCP, A2A
- **Phase 3 (Days 7–8)**: Governance, security, responsible AI
- **Phase 4 (Days 9–10)**: Copilot Studio, Power Platform, orchestration
- **Phase 5 (Day 11)**: Databricks, MLflow, enterprise integration
- **Phase 6 (Day 12)**: Capstone project
