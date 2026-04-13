from fastmcp.contrib.mcp_mixin import MCPMixin, mcp_tool

class TemplateTools(MCPMixin):
    def __init__(self):
        super().__init__()

    @mcp_tool(name="tool_01", description="This is tool 01")
    def tool_01(self)->str:
        return "This is tool 01"
    

        
