from mcp.server.fastmcp import FastMCP

subserver_mcp1 = FastMCP("subserver_mcp1")

@subserver_mcp1.tool(name="tool_01", description="This is tool 01")
def subserver_tool_01():
    return "This is tool 01"

@subserver_mcp1.tool(name="tool_02", description="This is tool 02")
def subserver_tool_02():
    return "This is tool 02"

@subserver_mcp1.tool(name="tool_03", description="This is tool 03")
def subserver_tool_03():
    return "This is tool 03"


