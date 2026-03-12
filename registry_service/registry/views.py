from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Agent
from .serializers import AgentSerializer
import requests
import uuid


@api_view(["POST"])
def register_agent(request):

    data = request.data

    agent, created = Agent.objects.update_or_create(
        name=data["name"],
        defaults={
            "description": data["description"],
            "capabilities": data["capabilities"],
            "endpoint_url": data["endpoint_url"],
            "status": "active"
        }
    )

    return Response({
        "message": "Agent registered",
        "created": created
    })


@api_view(['GET'])
def list_agents(request):
    agents = Agent.objects.all()
    serializer = AgentSerializer(agents, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def search_agents(request):
    capability = request.GET.get("capability")

    agents = Agent.objects.filter(capabilities__contains=[capability])
    serializer = AgentSerializer(agents, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def orchestrate_task(request):

    capability = request.data.get("capability")
    task_input = request.data.get("input")

    agents = Agent.objects.filter(capabilities__contains=[capability])

    if not agents:
        return Response({"error": "No agent found"})

    agent = agents.first()

    task = {
        "task_id": str(uuid.uuid4()),
        "capability": capability,
        "input": task_input,
        "context": {}
    }

    try:
        response = requests.post(agent.endpoint_url, json=task, timeout=10)
        return Response(response.json())
    except requests.exceptions.RequestException:
        return Response({"error": "Agent not reachable"})
