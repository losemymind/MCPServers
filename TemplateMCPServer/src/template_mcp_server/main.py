import os
import sys
import subprocess
import atexit
import threading
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from template_mcp_server.mcp_logging import mcp_logger

logger = mcp_logger.getChild(__name__)

# 使用进程启动MCP服务器
_mcp_server_process = None
def shutdown_mcp_server():
    """Shutdown the MCP server process when Unreal Editor closes"""
    global _mcp_server_process
    if _mcp_server_process:
        logger.info("Shutting down MCP server process...")
        try:
            _mcp_server_process.terminate()
            _mcp_server_process = None
            logger.info("MCP server process terminated successfully")
        except Exception as e:
            logger.error(f"Error terminating MCP server: {e}")

def start_mcp_server():
    global _mcp_server_process
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

        _mcp_server_process = subprocess.Popen(
            [python_exe, mcp_server_path, "--root-dir {Path(__file__).parent}"],
            creationflags=creationflags,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True
        )

        logger.info(f"MCP server started with PID: {_mcp_server_process.pid}")

        # Register cleanup handler to ensure process is terminated when Unreal exits
        atexit.register(shutdown_mcp_server)

        return True
    except Exception as e:
        logger.log_error(f"Failed to start MCP server: {str(e)}")
        return False


# 使用线程启动MCP服务器
from template_mcp_server.mcp_server import cli as cli_mcp_server
_mcp_server_thread = None
def run_mcp_server():
    cli_mcp_server()

def start_mcp_server():
    try:
        global _mcp_server_thread
        if _mcp_server_thread is not None and _mcp_server_thread.is_alive():
            logger.info("[UEUniversalMCPServer] MCP server thread already running")
            return True
        
        _mcp_server_thread = threading.Thread(target=run_mcp_server, daemon=True, name="MCP-Server")
        _mcp_server_thread.start()
        return True
    except Exception as e:
        logger.log_error(f"[UEUniversalMCPServer] Failed to start MCP server: {e}")
        import traceback
        logger.log_error(traceback.format_exc())
        return False


def stop_mcp_server():
    try:
        global _mcp_server_thread
        if _mcp_server_thread is None or not _mcp_server_thread.is_alive():
            logger.info("[UEUniversalMCPServer] MCP server is not running")
            return False
        logger.info("[UEUniversalMCPServer] Stopping MCP server...")

        # Wait briefly for graceful shutdown
        if _mcp_server_thread.is_alive():
            _mcp_server_thread.join(timeout=5.0)
        else:
            logger.info("[UEUniversalMCPServer] Server thread stopped gracefully")
        _mcp_server_thread = None
    except Exception as e:
        logger.log_error(f"[UEUniversalMCPServer] Failed to start MCP server: {e}")
        import traceback
        logger.log_error(traceback.format_exc())


def main():
    start_mcp_server()

if __name__ == "__main__":
    main()




