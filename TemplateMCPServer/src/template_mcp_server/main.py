import os
import sys
import subprocess
import atexit
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from template_mcp_server.mcp_logging import mcp_logger

logger = mcp_logger.getChild(__name__)

mcp_server_process = None
def shutdown_mcp_server():
    """Shutdown the MCP server process when Unreal Editor closes"""
    global mcp_server_process
    if mcp_server_process:
        logger.info("Shutting down MCP server process...")
        try:
            mcp_server_process.terminate()
            mcp_server_process = None
            logger.info("MCP server process terminated successfully")
        except Exception as e:
            logger.error(f"Error terminating MCP server: {e}")

def start_mcp_server():
    global mcp_server_process
    try:
        mcp_server_path = Path(__file__).parent / "mcp_server.py"
        if not os.path.exists(mcp_server_path):
            logger.error(f"MCP server script not found at: {mcp_server_path}")
            return False

        # Start the MCP server as a separate process
        python_exe = sys.executable
        logger.info(f"Starting MCP server using Python: {python_exe}")
        logger.info(f"MCP server script path: {mcp_server_path}")

        # Create a detached process that will continue running
        # even if Unreal crashes (we'll handle proper shutdown with atexit)
        creationflags = 0
        if sys.platform == 'win32':
            creationflags = subprocess.CREATE_NEW_PROCESS_GROUP

        mcp_server_process = subprocess.Popen(
            [python_exe, mcp_server_path],
            creationflags=creationflags,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        logger.info(f"MCP server started with PID: {mcp_server_process.pid}")

        # Register cleanup handler to ensure process is terminated when Unreal exits
        atexit.register(shutdown_mcp_server)

        return True
    except Exception as e:
        logger.log_error(f"Failed to start MCP server: {str(e)}")
        return False


def main():
    start_mcp_server()

if __name__ == "__main__":
    main()




