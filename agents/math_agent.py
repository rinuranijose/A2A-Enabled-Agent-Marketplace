from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

REGISTRY_URL = "http://localhost:8000/api/agents/register"

def register():

    agent_data = {
        "name": "Math Helper",
        "description": "Solves math problems",
        "capabilities": ["math"],
        "endpoint_url": "http://localhost:8001/execute"
    }

    requests.post(REGISTRY_URL, json=agent_data)


@app.route("/execute", methods=["POST"])
def execute():

    data = request.json
    task_id = data["task_id"]
    question = data["input"]

    try:
        result = eval(question)

        return jsonify({
            "task_id": task_id,
            "status": "success",
            "result": str(result),
            "error": None
        })

    except Exception as e:

        return jsonify({
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": str(e)
        })


if __name__ == "__main__":
    register()
    app.run(port=8001)