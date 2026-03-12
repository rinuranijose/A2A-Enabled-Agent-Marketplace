@echo off
echo Starting ...

REM Start Redis
start cmd /k "cd /d C:\Users\USER && redis-server"

REM Start Ollama
start cmd /k "ollama run phi3"

REM Start Django Backend
start cmd /k "cd /d %cd%\registry_service && python manage.py runserver"

REM Start MCP Gateway
start cmd /k "cd /d %cd%\gateway && python mcp_gateway.py"

REM Start Agents
start cmd /k "cd /d %cd%\agents && python summarizer_agent.py"
start cmd /k "cd /d %cd%\agents && python math_agent.py"

REM Start Streamlit UI
start cmd /k "cd /d %cd%\ui && streamlit run streamlit_app.py"

echo All services are starting...
pause