# Agent Marketplace – A2A + MCP Architecture

## Overview

This project implements a **multi-agent marketplace system** where users can send tasks and the system routes them to the appropriate agent based on capability.

The system demonstrates:

* **Agent-to-Agent (A2A) communication**
* **Agent discovery via a registry**
* **Capability-based task routing**
* **Integration with MCP tools through a gateway**

Agents can dynamically **register themselves** with a central registry service.

---

# System Architecture

The system consists of five main components:

```
User (Streamlit UI)
        │
        ▼
Registry Service (Django REST)
        │
        ▼
Task Orchestrator
        │
 ┌──────┼─────────────┐
 ▼      ▼             ▼
Math Agent   Summarizer Agent   MCP Gateway Agent
                                    │
                                    ▼
                              MCP Tool (Web Search)
```

---

# Project Structure

```
A2A/
│
├── agents/
│   ├── math_agent.py
│   └── summarizer_agent.py
│
├── gateway/
│   ├── mcp_gateway.py
│   └── web_search_tool.py
│
├── registry_service/
│   ├── manage.py
│   ├── registry/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   └── urls.py
│
├── ui/
│   └── streamlit_app.py
│
└── App_exe.bat
```

---

# Components

## 1. Registry Service (Django)

Responsible for:

* Maintaining **agent directory**
* Registering agents
* Routing tasks to the correct agent

API endpoints:

```
POST /api/agents/register
GET  /api/agents/list
GET  /api/agents/search
POST /api/task
```

---

## 2. Math Agent

Capability:

```
math
```

Example task:

```
2 + 5 * 10
```

The agent receives the task and evaluates the expression.

---

## 3. Summarizer Agent

Capability:

```
summarization
```

This agent receives a text input and returns a summarized version.

---

## 4. MCP Gateway Agent

Capability:

```
search
```

Responsibilities:

* Registers itself as an agent
* Receives A2A requests
* Calls MCP tools internally
* Returns results in A2A format

The gateway connects HTTP-based A2A agents with **MCP stdio tools**.

---

## 5. MCP Tool (Web Search)

Implemented using **FastMCP**.

Transport:

```
STDIO
```

The gateway communicates with the MCP tool using:

```
stdin
stdout
```

---

# How Agents Register Themselves

Each agent registers by calling:

```
POST /api/agents/register
```

Example registration payload:

```
{
 "name": "Math Helper",
 "description": "Solves math expressions",
 "endpoint_url": "http://localhost:9001/task",
 "capabilities": ["math"]
}
```

Registration occurs automatically when the agent starts.

---

# How to Start Each Component

Start services **in the below order**.

---

## 1. Start Registry Service

```
cd registry_service
python manage.py runserver
```

Server runs at:

```
http://localhost:8000
```

---

## 2. Start Agents

Open another terminal.

```
cd agents
python math_agent.py
python summarizer_agent.py
```

---

## 3. Start MCP Gateway

```
cd gateway
python mcp_gateway.py
```

---

## 4. Start UI

```
cd ui
streamlit run streamlit_app.py
```

UI will be available at:

```
http://localhost:8501
```

---
A bat file, ##App_exe.bat is created to execute all these commands so instead of running above services separately, run the bat file.

# Example Task Flow

```
User submits task in Streamlit
        │
        ▼
Streamlit sends POST /task
        │
        ▼
Registry Service receives request
        │
        ▼
Orchestrator finds matching capability
        │
        ▼
Agent executes task
        │
        ▼
Result returned to UI
```

---

# Example Requests

## Math Task

Request

```
POST /api/task
```

```
{
 "capability": "math",
 "input": "10 * (5 + 2)"
}
```

Response

```
{
 "result": 70
}
```

---

## Summarization Task

Request

```
{
 "capability": "summarization",
 "input": "Artificial intelligence is transforming industries..."
}
```

Response

```
{
 "summary": "AI is transforming industries."
}
```

---

## Web Search Task

Request

```
{
 "capability": "search",
 "input": "Future of AI Agents"
}
```

Response

```
{
 "results": [
   "AI agents will collaborate, reason, and automate workflows across systems...."
 ]
}
```

---


