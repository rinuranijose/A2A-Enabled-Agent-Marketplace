from flask import Flask, request, jsonify
import requests
import ollama

app = Flask(__name__)

REGISTRY_URL = "http://localhost:8000/api/agents/register"


def register():

    agent_data = {
        "name": "Text Summarizer",
        "description": "Summarizes text",
        "capabilities": ["summarization"],
        "endpoint_url": "http://localhost:8002/execute"
    }

    requests.post(REGISTRY_URL, json=agent_data)


@app.route("/execute", methods=["POST"])
def execute():

    data = request.json
    task_id = data["task_id"]
    text = data["input"]

    response = ollama.chat(
        model="phi3",
        messages=[
            {"role": "user", "content": f"Summarize this text:\n{text}"}
        ]
    )

    summary = response["message"]["content"]

    return jsonify({
        "task_id": task_id,
        "status": "success",
        "result": summary,
        "error": None
    })


if __name__ == "__main__":
    register()
    app.run(port=8002)