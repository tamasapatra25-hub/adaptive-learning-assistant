from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential

client = AgentsClient(
    endpoint="https://firstproject-resource3.services.ai.azure.com/api/projects/firstproject",
    credential=DefaultAzureCredential(
        exclude_environment_credential=True,
        exclude_managed_identity_credential=True
    )
)

try:
    agent = client.create_agent(model="gpt-4o", name="test", instructions="test")
    print("SUCCESS:", agent.id)
    client.delete_agent(agent.id)
except Exception as e:
    print("ERROR:", e)