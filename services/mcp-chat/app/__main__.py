import asyncio
from .mcp_server import mcp

if __name__ == "__main__":
    # Run the MCP server over stdio
    asyncio.run(mcp.run_stdio())
