import time
import os
import sys

# Ensure the current directory is in the python path
sys.path.append(os.getcwd())

from zmb.memory import setup_memory
from zmb.state import State
from zmb.tools.file_ops import read_file, write_file

def main():
    logger = setup_memory()
    logger.info("ZMB Kernel Initializing...")
    
    state = State()
    logger.info(f"Current Phase: {state.data['phase']}")
    
    # Autonomous Documentation Update
    update_status_file(state)
    
    logger.info("Entering Main Loop...")
    # For now, just a single pass to verify IOC
    logger.info("Heartbeat: System Active.")
    
    # Example of self-reflection (reading own code)
    try:
        own_code = read_file(__file__)
        logger.info(f"Successfully read own kernel code ({len(own_code)} bytes).")
    except Exception as e:
        logger.error(f"Failed to read own code: {e}")

def update_status_file(state):
    status_content = f"""# ZMB STATUS
**Current Phase:** {state.data['phase']}
**Last Updated:** {time.ctime()}
**Active Tasks:** {state.data['active_tasks']}

## Recent Logs
- Kernel Heartbeat: {time.ctime()}
"""
    write_file('STATUS.md', status_content)

if __name__ == "__main__":
    main()
