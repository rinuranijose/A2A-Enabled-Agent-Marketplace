
from fastmcp import FastMCP

mcp = FastMCP("Web Search MCP")

@mcp.tool()
def web_search(query: str):
    """Search the web and return results"""

    results = [
        {
            "title": "Agentic AI Explained",
            "snippet": "Agentic AI refers to AI systems that can autonomously plan and execute tasks using tools."
        },
        {
            "title": "Future of AI Agents",
            "snippet": "AI agents will collaborate, reason, and automate workflows across systems."
        }
    ]

    return results


if __name__ == "__main__":
    mcp.run()