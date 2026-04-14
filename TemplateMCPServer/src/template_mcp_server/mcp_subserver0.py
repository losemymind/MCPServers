from fastmcp import FastMCP
from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool

class SubserverTools(MCPMixin):
    def __init__(self):
        super().__init__()

    @mcp_tool(name="tool_01", description="This is tool 01")
    def tool_01(self)->str:
        return "This is tool 01"
    
    @mcp_tool(name="tool_02", description="This is tool 02")
    def tool_02(self)->str:
        return "This is tool 02"
    

subserver_mcp0 = FastMCP(name="subserver_mcp0")
SubserverTools().register_all(mcp_server=subserver_mcp0)





