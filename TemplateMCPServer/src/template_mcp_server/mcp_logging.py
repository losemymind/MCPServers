from fastmcp.utilities.logging import get_logger

mcp_logger = get_logger("template_mcp_server")


# import sys
# import logging

# # Configure logging with more detailed format
# logging.basicConfig(
#     level=logging.DEBUG,  # Change to DEBUG level for more details
#     format='%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s',
#     handlers=[
#         logging.FileHandler('unreal_mcp_server.log'), # Log to a file for persistent logging
#         logging.StreamHandler(sys.stdout) # Also log to console for real-time feedback
#     ]
# )

# mcp_logger = logging.getLogger(__name__)