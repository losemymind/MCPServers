import asyncio
import tempfile
import asyncclick as click
from pathlib import Path

from fastmcp import FastMCP
from fastmcp.tools import Tool
from fastmcp.tools import FunctionTool
from fastmcp.client.logging import LogMessage

from git import Repo
from typing import Literal
from contextlib import AsyncExitStack

from template_mcp_server.mcp_logging import mcp_logger
from template_mcp_server.mcp_tools import TemplateTools

from template_mcp_server.mcp_subserver0 import subserver_mcp0
from template_mcp_server.mcp_subserver1 import subserver_mcp1

logger = mcp_logger.getChild(__name__)

MCP_TRANSPORT_HELP="""The transport to use for the MCP server. Defaults to stdio.
    - stdio: Use standard input/output for communication. This is the default and is suitable for simple use cases or when running the server locally.
    - sse: Use Server-Sent Events (SSE) for communication. This is suitable for web applications or when you want to stream updates to the client in real-time.
    - http: Use HTTP for communication. This is suitable for web applications or when you want to expose the MCP server as a web service.   
    - streamable-http: Use Streamable HTTP for communication. This is suitable for web applications or when you want to expose the MCP server as a web service and need to stream updates to the client in real-time.
    """

def clone_git_repository(root_git_url: str, directory: str) -> Path:
    """Clone a git repository to a temporary directory."""
    _ = Repo.clone_from(root_git_url, directory, depth=1, single_branch=True)
    return Path(directory)


def function_01():
    return "This is tool 01"

def function_02():
    return "This is tool 02"


@click.command()
@click.option("--root-dir",      type=str, default=None, help="The root directory to use for the MCP server.")
@click.option("--root-git-url",  type=str, default=None, help="The URL of the root git repository to clone.")
@click.option("--mcp-transport", type=click.Choice(["stdio", "sse", "http", "streamable-http"]), default="stdio", help=MCP_TRANSPORT_HELP)
async def cli(root_dir: str | None, root_git_url: str | None, mcp_transport : Literal["stdio", "sse", "http", "streamable-http"]):
    if root_dir and root_git_url:
        msg = "You cannot specify both a root directory and a root git url."
        raise ValueError(msg)

    root_dir_path = Path(root_dir) if root_dir else Path.cwd()

    async with AsyncExitStack() as stack:
        if root_git_url:
            directory = stack.enter_context(tempfile.TemporaryDirectory())

            logger.info("Cloning git repository %s to %s", root_git_url, directory)

            root_dir_path = clone_git_repository(root_git_url, directory)

        mcp: FastMCP[None] = FastMCP(name="Template MCP")

        # Add tools to the MCP server
        _ = mcp.add_tool(tool=FunctionTool.from_function(fn=function_01, name="function_01", description="This is tool 01"))
        _ = mcp.add_tool(Tool.from_function(fn=function_02, name="function_02", description="This is tool 02"))

        # If you have multiple tools, it's better to organize them in a class that inherits from MCPMixin and 
        # use the @mcp_tool decorator to define your tools. Then you can register all the tools in that class 
        # at once with the MCP server.
        TemplateTools().register_all(mcp_server=mcp)
        # or only specific tools:
        #TemplateTools().register_tools(mcp_server=mcp)

        # Mount the FastMCP sub-servers
        mcp.mount("subserver0", subserver_mcp0)
        mcp.mount("subserver1", subserver_mcp1)

        await mcp.run_async(transport=mcp_transport)

        # run_kwargs: dict = {}
        # run_kwargs["transport"] = mcp_transport
        # run_kwargs["host"]      = "127.0.0.1"
        # run_kwargs["port"]      = 9090

        # await mcp.run_async(**run_kwargs)


def run_mcp():
    asyncio.run(cli())

if __name__ == "__main__":
    run_mcp()
