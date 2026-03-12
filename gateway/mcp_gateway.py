import requests
import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

REGISTRY_URL = "http://localhost:8000/api/agents/register"

# Start MCP tool process
mcp_process = subprocess.Popen(
    ["python", "web_search_tool.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
)

def register():
    agent_data = {
        "name": "Web Search Agent",
        "description": "Searches the web using MCP",
        "capabilities": ["search"],
        "endpoint_url": "http://localhost:8010/execute"
    }

    try:
        requests.post(REGISTRY_URL, json=agent_data)
        print("MCP Gateway registered")
    except Exception as e:
        print("Registration failed:", e)


def call_mcp_tool(query):

    request_payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "search",
            "arguments": {
                "query": query
            }
        }
    }

    mcp_process.stdin.write(json.dumps(request_payload) + "\n")
    mcp_process.stdin.flush()

    response = mcp_process.stdout.readline()

    return json.loads(response)


@app.route("/execute", methods=["POST"])
def execute():

    data = request.json
    task_id = data.get("task_id")
    query = data.get("input")

    try:
        result = call_mcp_tool(query)

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": result,
            "error": None
        })

    except Exception as e:

        return jsonify({
            "task_id": task_id,
            "status": "failed",
            "result": None,
            "error": str(e)
        })


if __name__ == "__main__":
    register()
    app.run(port=8010)